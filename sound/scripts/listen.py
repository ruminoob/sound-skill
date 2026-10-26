"""Evidence for sound you can't hear.

  python listen.py check <out-dir> a.wav b.wav ... [--curve]
      One review sheet (waveform + log spectrogram per file, shared time axis),
      metrics per file, and with --curve brightness and level every 50 ms.

  python listen.py page <manifest.json> <out-dir> [--artifact]
      A loudness-matched audition page (index.html + audio/ + img/) and a review
      sheet per cue. Serve the folder over http to open it. --artifact leaves out the
      document wrapper, for publishing with Claude's Artifact tool.
"""
import argparse
import html
import io
import json
import subprocess
from pathlib import Path

import matplotlib
import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import resample_poly, stft, welch

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).parent
SHORT = 2.0   # seconds: shorter files are measured with short loudness blocks
LONG = 8.0    # seconds: longer takes are published as mp3


def read(path):
    try:
        x, sr = sf.read(str(path), always_2d=True)
    except Exception:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "wav",
                              "-acodec", "pcm_f32le", "-"], capture_output=True, check=True).stdout
        x, sr = sf.read(io.BytesIO(raw), always_2d=True)
    x = x.T[:2]
    if x.shape[0] == 1:
        x = np.vstack([x, x])
    return x, sr


def dur(x, sr):
    return x.shape[1] / sr


def lufs(x, sr):
    y = np.pad(x, ((0, 0), (0, max(0, sr - x.shape[1]))))
    block = 0.1 if dur(x, sr) < SHORT else 0.4
    return pyln.Meter(sr, block_size=block).integrated_loudness(y.T)


def true_peak(x):
    return 20 * np.log10(np.abs(resample_poly(x, 4, 1, axis=-1)).max() + 1e-12)


def metrics(x, sr):
    m = x.mean(0)
    peak = np.abs(x).max() + 1e-12
    rms = np.sqrt((x ** 2).mean()) + 1e-12
    edge = int(0.002 * sr)
    f, _, Z = stft(m, sr, nperseg=2048)
    p = (np.abs(Z) ** 2).sum(1)
    fw, pw = welch(m, sr, nperseg=min(8192, len(m)))
    keep = (fw >= 100) & (fw <= 10000)
    side = (x[0] - x[1]) / 2
    return {
        "sec": round(dur(x, sr), 3),
        "lufs": round(lufs(x, sr), 1),
        "true_peak_db": round(true_peak(x), 1),
        "crest_db": round(20 * np.log10(peak / rms), 1),
        "first_sample_db": round(20 * np.log10(np.abs(x[:, 0]).max() / peak + 1e-12), 1),
        "last_2ms_db": round(20 * np.log10(np.abs(x[:, -edge:]).max() / peak + 1e-12), 1),
        "centroid_hz": int((f * p).sum() / (p.sum() + 1e-20)),
        "tilt_db_oct": round(float(np.polyfit(np.log2(fw[keep]),
                                              10 * np.log10(pw[keep] + 1e-20), 1)[0]), 2),
        "side_db": round(10 * np.log10((side ** 2).mean() / ((m ** 2).mean() + 1e-20) + 1e-12), 1),
    }


def curve(x, sr):
    """Centroid and level over time: every 50 ms, or about 60 points for long files."""
    m = x.mean(0)
    hop = int(max(0.05, dur(x, sr) / 60) * sr)
    f, t, Z = stft(m, sr, nperseg=hop * 4, noverlap=hop * 3)
    P = np.abs(Z) ** 2
    level = 10 * np.log10(P.sum(0) + 1e-20)
    level -= level.max()
    cen = (f[:, None] * P).sum(0) / (P.sum(0) + 1e-20)
    return [(round(float(a), 2), int(c), round(float(lv), 1))
            for a, c, lv in zip(t, cen, level) if lv > -60]


def spectrogram(ax, x, sr, span):
    m = x.mean(0)
    nper = 1024 if dur(x, sr) < SHORT else 4096
    f, t, Z = stft(m, sr, nperseg=nper, noverlap=nper - nper // 8)
    S = 20 * np.log10(np.abs(Z) + 1e-9)
    top = S.max()
    keep = (f >= 30) & (f <= min(20000, sr / 2))
    ax.pcolormesh(t, f[keep], S[keep], vmin=top - 70, vmax=top, cmap="magma", shading="auto")
    ax.set_yscale("log")
    ax.set_ylim(30, min(20000, sr / 2))
    ax.set_xlim(0, span)


def strip(path, x, sr, span):
    fig = plt.figure(figsize=(12, 2.6), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("black")
    spectrogram(ax, x, sr, span)
    ax.axis("off")
    fig.savefig(path, facecolor="black")
    plt.close(fig)


def sheet(path, takes, span):
    """takes: list of (label, x, sr)."""
    fig, axes = plt.subplots(2 * len(takes), 1, figsize=(12, 4.2 * len(takes)), dpi=80,
                             sharex=True, gridspec_kw={"height_ratios": [1, 2] * len(takes)},
                             squeeze=False)
    axes = axes[:, 0]
    for i, (label, x, sr) in enumerate(takes):
        t = np.arange(x.shape[1]) / sr
        axes[2 * i].plot(t, x[0], lw=0.5, color="tab:blue")
        axes[2 * i].plot(t, x[1], lw=0.5, color="tab:orange", alpha=0.6)
        axes[2 * i].set_ylim(-1, 1)
        axes[2 * i].set_title(label, loc="left")
        spectrogram(axes[2 * i + 1], x, sr, span)
    axes[-1].set_xlabel("seconds")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def check(out, files, show_curve):
    out.mkdir(parents=True, exist_ok=True)
    takes = [(Path(f).name, *read(f)) for f in files]
    span = max(dur(x, sr) for _, x, sr in takes)
    sheet(out / "review.png", takes, span)
    table = {}
    for label, x, sr in takes:
        table[label] = metrics(x, sr)
        print(label, json.dumps(table[label]))
        if show_curve:
            print("  t, centroid Hz, level dB:", "  ".join(f"{a}:{c}:{lv}" for a, c, lv in curve(x, sr)))
    (out / "metrics.json").write_text(json.dumps(table, indent=2))
    print(f"review sheet: {out / 'review.png'}")


def page(manifest_path, out, artifact=False):
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    base = Path(manifest_path).parent
    for d in ("audio", "img", "review"):
        (out / d).mkdir(parents=True, exist_ok=True)
    published, cues, table = [], [], {}
    for cue in manifest["cues"]:
        cid = cue["id"]
        loaded = [[read(base / f) for f in take["files"]] for take in cue["takes"]]
        firsts = [xs[0] for xs in loaded]
        longest = max(dur(x, sr) for x, sr in firsts)

        # one loudness for every take of the cue, every take under -1 dBTP
        target = -16.0 if longest > LONG else -18.0
        for x, sr in firsts:
            target = min(target, lufs(x, sr) + (-1.0 - true_peak(x)))

        takes = []
        for k, (take, xs) in enumerate(zip(cue["takes"], loaded), 1):
            gain = 10 ** ((target - lufs(*xs[0])) / 20)
            names = []
            for i, (x, sr) in enumerate(xs):
                stem = f"{cid}_{k}" + (f"-{i}" if len(xs) > 1 else "")
                wav = out / "audio" / f"{stem}.wav"
                sf.write(str(wav), (x * gain).T, sr, subtype="PCM_16")
                if dur(x, sr) > LONG:
                    mp3 = wav.with_suffix(".mp3")
                    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(wav), "-b:a", "256k",
                                    str(mp3)], check=True)
                    wav.unlink()
                    names.append(f"audio/{mp3.name}")
                else:
                    names.append(f"audio/{wav.name}")
            x0, sr0 = xs[0]
            strip(out / "img" / f"{cid}_{k}.png", x0 * gain, sr0, longest)
            m = metrics(x0 * gain, sr0)
            table.setdefault(cid, {})[take["label"]] = m
            takes.append({"label": take["label"], "note": take.get("note", ""), "files": names,
                          "img": f"img/{cid}_{k}.png",
                          "m": {k2: m[k2] for k2 in ("sec", "first_sample_db", "last_2ms_db")}})
            published += names + [f"img/{cid}_{k}.png"]
        sheet(out / "review" / f"{cid}.png",
              [(t["label"], xs[0][0] * 10 ** ((target - lufs(*xs[0])) / 20), xs[0][1])
               for t, xs in zip(cue["takes"], loaded)], longest)
        cues.append({"id": cid, "name": cue["name"], "brief": cue.get("brief", ""),
                     "lufs": round(target, 1), "span": longest, "takes": takes})
        print(cid, json.dumps(table[cid]))

    data = {"title": manifest["title"], "intro": manifest.get("intro", ""), "cues": cues}
    tpl = (HERE / "audition.html").read_text(encoding="utf-8")
    page_html = (tpl.replace("__TITLE__", html.escape(manifest["title"]))
                 .replace("__DATA__", json.dumps(data).replace("</", "<\\/")))
    if not artifact:
        page_html = ('<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n'
                     '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                     + page_html)
    (out / "index.html").write_text(page_html, encoding="utf-8")
    (out / "metrics.json").write_text(json.dumps(table, indent=2))
    print(f"page: {out / 'index.html'}  review sheets: {out / 'review'}")
    print("page files:", json.dumps(published))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("out", type=Path)
    c.add_argument("files", nargs="+")
    c.add_argument("--curve", action="store_true")
    p = sub.add_parser("page")
    p.add_argument("manifest", type=Path)
    p.add_argument("out", type=Path)
    p.add_argument("--artifact", action="store_true")
    a = ap.parse_args()
    if a.cmd == "check":
        check(a.out, a.files, a.curve)
    else:
        page(a.manifest, a.out, a.artifact)
