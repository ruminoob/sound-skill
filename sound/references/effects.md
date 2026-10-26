# Effects

How an effect goes from its brief to a finished file. Every function named here is in `scripts/dsp.py`. No values are given on purpose: frequencies, decays, levels and rooms come from the brief — the object's material and size, the listener's distance, the space — and from checking the result.

## Stages and layers

Read the brief's stages as separate events placed in time: whatever touches before it presses, strikes before it rings, approaches before it passes, lands before it settles. The gap between stages is part of the sound's identity: too short and they fuse, too long and they become two sounds.

Each stage is built from the layers it needs:

- **Transient** — the contact itself, a few milliseconds: noise shaped by the surface, or the edge of the excitation pulse.
- **Body** — the object that rings: resonators tuned to its modes.
- **Weight** — the low end, when the object is heavy or the action is firm: a short falling sine, a low mode, a punch.
- **Air and texture** — the medium and the debris: filtered noise, grains, rumble.
- **Tail** — the space.

Give each layer its own envelope and its own level, decided against the brief, then normalise the layers (`norm`) before mixing them so the mix levels mean something.

## Struck, plucked and rubbed objects

Excite, don't sum. `contact(n, sec, rng, rough)` is the force of the strike, a half-sine pulse; `resonate(x, freqs, t60s, gains)` is the object, one two-pole resonator per mode. The pulse's length is the mallet: a long contact (felt, yarn, a fingertip, a soft hand) can only excite low modes, a short one (stone, metal, a hard stick) reaches the top. A louder strike is also a harder one, so shorten the contact as velocity rises. `rough` adds the surface's grain to the pulse.

Choosing modes:
- Size sets the fundamental; material sets the pattern of overtones and how fast they die. Wood, stone, glass, plates and bells are inharmonic; strings and tuned bars sit close to whole-number ratios (a tuned bar's overtones are tuned on purpose; an untuned bar's are not). Look up the mode ratios of the object type rather than inventing them.
- Higher modes decay faster. Metal and glass ring long; wood and stone die quickly; felt and rubber damp everything.
- A metal or glass mode doubled with a hair of detune beats slowly and shimmers. Tuning the left and right channels a fraction of a cent apart gives a tonal sound width without moving it off-centre.
- A resonator tube, a body cavity or a room mode under the fundamental blooms in after the strike: a resonator on the fundamental with a slow attack.

Plucked strings: `pluck(freq, sec, rng, soften, damping)` (Karplus-Strong as one IIR). `soften` is the finger or pick.

## Moving things

Anything that travels changes four things at once, all from one motion model: level (distance), brightness (closer is brighter), pitch (approach raises, departure lowers — exaggerate the doppler for style, it is rarely audible at real speeds) and position (pan follows the path). Write the path as a function of time — closest distance, speed, pass time — and derive every curve from it.

- Arriving and leaving differ: the build is longer than the fall, and the departure is duller and fades faster.
- Moving air is filtered noise: `sweep(x, "bp", curve, q)` for the band that follows the motion, a lower band for the body of the air under the hiss, a narrow band for the edge tone of a thin object, and flutter (fast amplitude modulation) when a light object passes closest.
- Pan with a per-sample equal-power curve.

## Impacts

An impact is built from layers that each do one job; use the ones the brief calls for:
- **Punch**: a short pitch-falling sine, saturated, carrying the hit in the chest in the first few tens of milliseconds.
- **Sub**: a slower falling sine, saturated so small speakers hear its harmonics, and shorter than instinct says — a long sub drones instead of landing.
- **Material**: the struck object's modes through resonators, excited by a hard contact, so the listener hears what hit.
- **Crack**: bright noise for a few milliseconds, decorrelated left and right.
- **Debris**: short filtered grains whose density thins out over time, panned at random.
- **Rumble and tail**: low noise under a large, dark space; the reverb return is high-passed and low-passed.

Mix the punch and sub dry and centred, send the rest to the space, then add a heavily compressed copy of the sum underneath the original (parallel compression) for weight, and limit last.

## Tonal UI sounds

Confirms, notifications and errors are played on an instrument that could exist — bars, bells, glass, plucked strings, a struck body — through `contact` and `resonate`, not on bare oscillators. The interval and its direction carry the meaning (a rising, resolving figure reads as done; a falling or unresolved one as dismissal or error). Keep the figure as short as its meaning allows, and the tail short enough for how often the sound will be heard.

Even sounds meant to feel digital are designed: FM pairs with moving index envelopes, band-limited oscillators (`saw`, `square`) through moving filters, pitch envelopes, a space. A static waveform with a decay is the rejected shortcut whatever it is called.

## Life

- Sounds that repeat (taps, steps, clicks, hats) get several rendered variants that rotate at playback, each with small random changes in tuning, level, timing between stages and noise.
- Seed every random generator so a render is reproducible; vary the seed per variant.

## Space

`space(t60, predelay, damping, width, seed)` builds a stereo impulse response: sparse early reflections, then a diffuse tail whose highs die faster than its lows. Choose it from the brief: a dry small room for close UI sounds, a hall for a film's big moments. `reverb(x, ir, wet_db, hp, lp)` sends a mono sum into it and filters the return. Low layers stay out of the reverb and in the centre.

## Finishing chain

In this order, on the cue's bus:
1. High-pass below the lowest layer's job; `dc_block` after any asymmetric processing.
2. Colour: `drive` (tanh, oversampled) on layers that need harmonics or glue.
3. Dynamics: `compress` for glue, parallel compression for weight, `limit` last.
4. `fade` both ends so the file starts and ends at silence. Size the buffer so the tail decays inside it; a fade is not a substitute for a tail that was cut.

## Second pass

Go through every cue again before anyone hears it:
- **A summed-sine object** → excitation through resonators.
- **The stage the first pass skipped** — what happens after contact: a second impact, a bloom, a rebound, a settle.
- **Symmetric motion** → a slower arrival and a duller, faster departure.
- **A low end without a job** → a short punch and a shorter sub, or none.
- **A spiky transient carrying the whole sound** → more body, less spike (compare crest factor).
- **A tonal sound that sits dead centre** → a fraction of a cent between the channels.
- **A bright, hissy tail** → a darker space with filtered returns.
- **Identical repeats** → variants.

Then check against the first pass. A refinement can overshoot: lengthening contact pulses can make a whole sound dull, and more weight can turn into boom. Compare centroid, tilt and crest with the first pass and with the brief, and correct before showing.

## Traps already paid for

- **pedalboard's `Limiter` is a maximiser**: it adds make-up gain equal to minus its threshold and hard-clips samples at 0 dBFS, so inter-sample peaks still land above 0 dBTP. Treat its threshold as how hard you push into the ceiling, then lower the level until `true_peak_db` reads under −1 (`listen.py page` does this for auditions; shipped files need it too).
- **Naive square and saw waves alias** into inharmonic whistles; FM sidebands above Nyquist fold back too. Use `saw` / `square` (PolyBLEP), render FM at twice the rate and downsample, and saturate through `drive` (oversampled).
- **A moving average is not a filter**: it combs the spectrum with deep notches.
- **Cutting a sound off clicks**, and so does butting two tones end to end; both show as vertical lines on the spectrogram.
- **A contact pulse much longer than the period of the modes** leaves them barely excited and the sound dull; when a resonator sound measures darker than intended, shorten the contact before raising gains.
- **Per-sample Python loops are slow**: Karplus-Strong is one IIR (`lfilter`), each resonator is a biquad, and time-varying filters run block-wise with carried state (`sweep`).
