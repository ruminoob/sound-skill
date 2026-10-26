"""Offline DSP toolkit for building sound in code.

Mono signals are 1-D arrays, stereo signals are (2, n). Everything runs at SR.
Parameters that decide a sound's character have no defaults: they come from the
sound's brief. Defaults are left only on technical knobs.
"""
import numpy as np
from scipy.signal import lfilter, fftconvolve, resample_poly
from pedalboard import Pedalboard, Compressor, Limiter

SR = 48000


def n_of(sec):
    return int(round(sec * SR))


def t_of(sec):
    return np.arange(n_of(sec)) / SR


def silence(sec, stereo=True):
    return np.zeros((2, n_of(sec)) if stereo else n_of(sec))


def place(bus, x, at):
    """Mix x into bus in place, starting at `at` seconds. Mono x lands on both channels."""
    s = n_of(at)
    if s >= bus.shape[-1] or s + x.shape[-1] <= 0:
        return
    xs = max(0, -s)
    s = max(0, s)
    e = min(bus.shape[-1], s + x.shape[-1] - xs)
    bus[..., s:e] += x[..., xs:xs + e - s]


def db(x):
    return 10 ** (x / 20)


def norm(x):
    return x / (np.abs(x).max() + 1e-12)


# --- envelopes --------------------------------------------------------------

def decay(n, t60, start=0.0):
    """Exponential decay that falls 60 dB over t60 seconds."""
    t = np.arange(n) / SR - start
    return np.exp(-6.907755 * np.maximum(t, 0) / t60)


def attack(n, sec):
    """Raised-cosine rise over `sec`, then flat."""
    k = max(1, n_of(sec))
    e = np.ones(n)
    m = min(k, n)
    e[:m] = 0.5 - 0.5 * np.cos(np.pi * np.arange(m) / k)
    return e


def release(n, at, sec):
    """Flat until `at` seconds, then a 60 dB fall over `sec`."""
    t = np.arange(n) / SR - at
    return np.where(t < 0, 1.0, np.exp(-6.907755 * np.maximum(t, 0) / sec))


def fade(x, fin=0.0, fout=0.0):
    x = x.copy()
    n = x.shape[-1]
    if fin > 0:
        k = min(n, n_of(fin))
        x[..., :k] *= 0.5 - 0.5 * np.cos(np.pi * np.arange(k) / k)
    if fout > 0:
        k = min(n, n_of(fout))
        x[..., n - k:] *= 0.5 + 0.5 * np.cos(np.pi * np.arange(k) / k)
    return x


def glide(n, f_from, f_to, tau):
    """Exponential pitch glide from f_from toward f_to with time constant tau."""
    t = np.arange(n) / SR
    return f_to + (f_from - f_to) * np.exp(-t / tau)


# --- sources ----------------------------------------------------------------

def _phase(freq, n):
    if np.isscalar(freq):
        return freq * np.arange(n) / SR, np.full(n, freq / SR)
    return np.cumsum(freq) / SR, np.asarray(freq) / SR


def sine(freq, n=None, ph0=0.0):
    """Sine at a constant frequency (give n) or along a per-sample frequency curve."""
    n = n if n is not None else len(freq)
    ph, _ = _phase(freq, n)
    return np.sin(2 * np.pi * (ph + ph0))


def _blep(t, dt):
    y = np.zeros_like(t)
    m = t < dt
    x = t[m] / dt[m]
    y[m] = x + x - x * x - 1
    m = t > 1 - dt
    x = (t[m] - 1) / dt[m]
    y[m] = x * x + x + x + 1
    return y


def saw(freq, n=None, ph0=0.0):
    """Band-limited sawtooth (PolyBLEP)."""
    n = n if n is not None else len(freq)
    ph, dt = _phase(freq, n)
    t = (ph + ph0) % 1.0
    return 2 * t - 1 - _blep(t, dt)


def square(freq, n=None, ph0=0.0):
    """Band-limited square (PolyBLEP)."""
    n = n if n is not None else len(freq)
    ph, dt = _phase(freq, n)
    t = (ph + ph0) % 1.0
    return np.where(t < 0.5, 1.0, -1.0) + _blep(t, dt) - _blep((t + 0.5) % 1.0, dt)


def noise(n, rng):
    return rng.standard_normal(n)


def contact(n, sec, rng=None, rough=0.0):
    """The force of a strike: a half-sine pulse lasting `sec`. A soft mallet stays in
    contact longer, which by itself limits the highs it can excite; `rough` adds
    surface grain."""
    k = max(2, n_of(sec))
    x = np.zeros(n)
    x[:k] = np.sin(np.pi * np.arange(k) / k)
    if rough and rng is not None:
        x[:k] += rough * rng.standard_normal(k) * x[:k]
    return x


def resonate(x, freqs, t60s, gains):
    """Bank of two-pole resonators, one per mode. Each rings as a damped sine, shaped
    by whatever excites it."""
    out = np.zeros_like(x)
    for f, d, g in zip(freqs, t60s, gains):
        if f >= SR * 0.45:
            continue
        w = 2 * np.pi * f / SR
        r = np.exp(-6.907755 / (d * SR))
        out += g * lfilter([np.sin(w)], [1, -2 * r * np.cos(w), r * r], x)
    return out


def pluck(freq, sec, rng, soften, damping):
    """Karplus-Strong string as one IIR filter. `soften` darkens the excitation (near 0
    a pick, toward 1 a fingertip); `damping` just below 1 sets how long it rings."""
    n = n_of(sec)
    L = max(2, int(round(SR / freq - 0.5)))
    burst = rng.uniform(-1, 1, L)
    burst = lfilter([1 - soften], [1, -soften], burst)
    x = np.zeros(n)
    x[:L] = burst - burst.mean()
    a = np.zeros(L + 2)
    a[0] = 1.0
    a[L] = a[L + 1] = -damping / 2
    return lfilter([1.0], a, x)


# --- filters (RBJ biquads) --------------------------------------------------

def biquad(kind, f, q=0.707, gain_db=0.0):
    f = float(np.clip(f, 10.0, SR * 0.45))
    w = 2 * np.pi * f / SR
    cw, sw = np.cos(w), np.sin(w)
    al = sw / (2 * q)
    A = 10 ** (gain_db / 40)
    if kind == "lp":
        b, a = [(1 - cw) / 2, 1 - cw, (1 - cw) / 2], [1 + al, -2 * cw, 1 - al]
    elif kind == "hp":
        b, a = [(1 + cw) / 2, -(1 + cw), (1 + cw) / 2], [1 + al, -2 * cw, 1 - al]
    elif kind == "bp":
        b, a = [al, 0.0, -al], [1 + al, -2 * cw, 1 - al]
    elif kind == "peak":
        b, a = [1 + al * A, -2 * cw, 1 - al * A], [1 + al / A, -2 * cw, 1 - al / A]
    elif kind in ("lowshelf", "highshelf"):
        sq = 2 * np.sqrt(A) * al
        s = 1 if kind == "lowshelf" else -1
        b = [A * ((A + 1) - s * (A - 1) * cw + sq),
             s * 2 * A * ((A - 1) - s * (A + 1) * cw),
             A * ((A + 1) - s * (A - 1) * cw - sq)]
        a = [(A + 1) + s * (A - 1) * cw + sq,
             -s * 2 * ((A - 1) + s * (A + 1) * cw),
             (A + 1) + s * (A - 1) * cw - sq]
    else:
        raise ValueError(kind)
    return np.array(b) / a[0], np.array(a) / a[0]


def filt(x, kind, f, q=0.707, gain_db=0.0):
    """Static biquad: lp, hp, bp, peak, lowshelf, highshelf."""
    b, a = biquad(kind, f, q, gain_db)
    return lfilter(b, a, x, axis=-1)


def sweep(x, kind, f, q=0.707, block=64):
    """Time-varying biquad; f and q may be per-sample curves. Runs block-wise with the
    filter state carried across blocks."""
    n = x.shape[-1]
    f = np.broadcast_to(f, (n,))
    q = np.broadcast_to(q, (n,))
    out = np.empty_like(x)
    zi = np.zeros(x.shape[:-1] + (2,))
    for s in range(0, n, block):
        e = min(n, s + block)
        m = (s + e) // 2
        b, a = biquad(kind, f[m], q[m])
        out[..., s:e], zi = lfilter(b, a, x[..., s:e], axis=-1, zi=zi)
    return out


def dc_block(x):
    return filt(x, "hp", 15.0)


# --- colour -----------------------------------------------------------------

def drive(x, amount, os=4):
    """tanh saturation, oversampled so the harmonics it adds don't alias."""
    up = resample_poly(x, os, 1, axis=-1)
    y = np.tanh(amount * up) / np.tanh(amount)
    return resample_poly(y, 1, os, axis=-1)[..., : x.shape[-1]]


# --- space ------------------------------------------------------------------

def pan(x, p):
    """Equal-power pan of a mono signal, p in [-1, 1]; p may be a per-sample curve."""
    th = (np.clip(p, -1, 1) + 1) * np.pi / 4
    return np.stack([x * np.cos(th), x * np.sin(th)])


def stereo(x):
    return x if x.ndim == 2 else np.stack([x, x]) * 0.7071


def space(t60, predelay, damping, width=1.0, seed=1):
    """Stereo impulse response: sparse early reflections, then a diffuse tail whose
    highs die faster than its lows. `damping` in [0, 1) shortens the highs."""
    r = np.random.default_rng(seed)
    n = n_of(predelay + t60 * 1.1)
    ir = np.zeros((2, n))
    p = n_of(predelay)
    tail_len = n - p
    for ch in range(2):
        nz = r.standard_normal(tail_len)
        lo = filt(nz, "lp", 450)
        hi = filt(nz, "hp", 3500)
        mid = nz - lo - hi
        tail = (lo * decay(tail_len, t60 * 1.15)
                + mid * decay(tail_len, t60)
                + hi * decay(tail_len, max(0.05, t60 * (1 - damping))))
        tail *= attack(tail_len, min(0.04, t60 * 0.08))
        ir[ch, p:] = tail
        for _ in range(9):
            at = p + n_of(r.uniform(0.001, 0.045))
            ir[ch, at] += r.choice([-1, 1]) * r.uniform(0.3, 1.0) * np.sqrt(SR / 2000)
    m = ir.mean(0)
    ir = m + width * (ir - m)
    ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
    return ir


def reverb(x, ir, wet_db, hp=200.0, lp=9000.0):
    """Mono-summed send into a stereo IR, return filtered; stereo out, same length."""
    send = stereo(x).sum(0)
    n = send.shape[-1]
    w = np.stack([fftconvolve(send, ir[0])[:n], fftconvolve(send, ir[1])[:n]])
    w = filt(filt(w, "hp", hp), "lp", lp)
    return stereo(x) + w * db(wet_db)


def swell(x, ir, length):
    """Reverse reverb: x's reverb, reversed, rising over `length` seconds. Place it so
    it ends where x starts."""
    send = stereo(x).sum(0)
    k = n_of(length)
    w = np.stack([fftconvolve(send, ir[0])[:k], fftconvolve(send, ir[1])[:k]])
    w = filt(w, "hp", 200)[..., ::-1]
    return fade(w, length * 0.6, 0.01)


def chorus(x, rate, depth, base, mix):
    """Two modulated delays in quadrature, one per channel. depth and base in seconds."""
    src = stereo(x)
    n = src.shape[-1]
    t = np.arange(n) / SR
    idx = np.arange(n, dtype=float)
    out = np.empty_like(src)
    for ch, ph in enumerate((0.0, np.pi / 2)):
        d = (base + depth * np.sin(2 * np.pi * rate * t + ph)) * SR
        out[ch] = np.interp(idx - d, idx, src[ch], left=0.0)
    return src * (1 - mix) + out * mix


def pingpong(x, time, feedback, mix_db, taps=6, lp=3500.0):
    """Echoes alternating left and right, each darker than the last."""
    m = stereo(x).sum(0) * 0.5
    out = np.zeros((2, m.shape[-1]))
    tap = m * db(mix_db)
    for k in range(1, taps + 1):
        tap = filt(tap, "lp", lp) * (feedback if k > 1 else 1.0)
        place(out[k % 2], tap, time * k)
    return stereo(x) + out


def autopan(x, rate, depth):
    src = stereo(x)
    t = np.arange(src.shape[-1]) / SR
    lfo = np.sin(2 * np.pi * rate * t)
    return np.stack([src[0] * (1 - depth * lfo), src[1] * (1 + depth * lfo)])


def wow(x, depth, rate, flutter, flutter_rate):
    """Tape wow and flutter: a wandering delay (depths in seconds), so pitch drifts."""
    src = stereo(x)
    n = src.shape[-1]
    t = np.arange(n) / SR
    d = (depth + flutter + 0.001 + depth * np.sin(2 * np.pi * rate * t)
         + flutter * np.sin(2 * np.pi * flutter_rate * t)) * SR
    idx = np.arange(n, dtype=float)
    return np.stack([np.interp(idx - d, idx, ch, left=0.0) for ch in src])


# --- dynamics and level -----------------------------------------------------

def _board(x, *plugins):
    y = Pedalboard(list(plugins))(stereo(x).astype(np.float32), SR)
    return y.astype(float)


def compress(x, threshold, ratio, attack_ms, release_ms):
    return _board(x, Compressor(threshold_db=threshold, ratio=ratio,
                                attack_ms=attack_ms, release_ms=release_ms))


def limit(x, threshold, release_ms=80.0):
    """pedalboard's Limiter is a maximiser: it adds make-up gain of -threshold and
    hard-clips at 0 dBFS. Set the final level after it."""
    return _board(x, Limiter(threshold_db=threshold, release_ms=release_ms))


def duck(n, hits, depth, recover, rise=0.004):
    """Sidechain gain curve: dips by `depth` at each hit time and recovers."""
    g = np.ones(n)
    span = n_of(recover * 5)
    for h in hits:
        s = n_of(h)
        if s >= n:
            continue
        e = min(n, s + span)
        t = np.arange(e - s) / SR
        dip = depth * np.minimum(1.0, t / rise) * np.exp(-t / recover)
        g[s:e] = np.minimum(g[s:e], 1 - dip)
    return g


def loudness(x):
    """Integrated loudness in LUFS (needs at least 0.4 s; pad short sounds)."""
    import pyloudnorm as pyln
    return pyln.Meter(SR).integrated_loudness(stereo(x).T)


def level(x, target):
    """Set a stem to a target integrated loudness: mixing by numbers."""
    return x * db(target - loudness(x))
