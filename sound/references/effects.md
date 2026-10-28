# Effects

How an effect goes from its brief to a finished file. Every function named here is in `scripts/dsp.py`. No values are given on purpose: frequencies, decays, levels and rooms come from the brief — the source, its material or voice, the listener's distance, the space — and from checking the result. Nothing here is a structure every sound must have; each section applies when the brief's source calls for it. What makes the result pleasant, cheap or tiring to hear is in `ear.md`.

## Stages and layers

When the source has stages, read them as separate events placed in time: whatever touches before it presses, strikes before it rings, approaches before it passes, lands before it settles. The gap between stages is part of the sound's identity: too short and they fuse, too long and they become two sounds.

A sound that has parts is built from the layers it needs, such as:

- **Transient** — the contact itself, a few milliseconds: noise shaped by the surface, or the edge of the excitation pulse.
- **Body** — the object that rings: resonators tuned to its modes.
- **Weight** — the low end, when the object is heavy or the action is firm: a short falling sine, a low mode, a punch.
- **Air and texture** — the medium and the debris: filtered noise, grains, rumble.
- **Tail** — the space.

Give each layer its own envelope and its own level, decided against the brief, then normalise the layers (`norm`) before mixing them so the mix levels mean something. One designed voice with no other layer is also a whole sound.

## Struck, plucked and rubbed objects

For sources the brief names as an object being struck, plucked or rubbed. Excite, don't sum. `contact(n, sec, rng, rough)` is the force of the strike, a half-sine pulse; `resonate(x, freqs, t60s, gains)` is the object, one two-pole resonator per mode. The pulse's length is the mallet: a long contact (felt, yarn, a fingertip, a soft hand) can only excite low modes, a short one (stone, metal, a hard stick) reaches the top. A louder strike is also a harder one, so shorten the contact as velocity rises. `rough` adds the surface's grain to the pulse.

Choosing modes:
- Size sets the fundamental; material sets the pattern of overtones and how fast they die. Wood, stone, glass, plates and bells are inharmonic; strings and tuned bars sit close to whole-number ratios (a tuned bar's overtones are tuned on purpose; an untuned bar's are not). Look up the mode ratios of the object type rather than inventing them.
- Higher modes decay faster. Metal and glass ring long; wood and stone die quickly; felt and rubber damp everything.
- A metal or glass mode doubled with a hair of detune beats slowly and shimmers. Tuning the left and right channels a fraction of a cent apart gives a tonal sound width without moving it off-centre.
- A resonator tube, a body cavity or a room mode under the fundamental blooms in after the strike: a resonator on the fundamental with a slow attack.
- Short, dry, inharmonic modes are a wood block whatever they were meant to be, and wood knocks as a default are a sound this skill rules out. When the brief isn't wood, change what makes it wood: decays that ring (metal, glass), a near-harmonic pattern (tuned bars, bell partials), more space — or a synthetic source.

Plucked strings: `pluck(freq, sec, rng, soften, damping)` (Karplus-Strong as one IIR). `soften` is the finger or pick.

## Moving things

Anything that travels changes four things at once, all from one motion model: level (distance), brightness (closer is brighter), pitch (approach raises, departure lowers; at real speeds the shift is small, so exaggerate it only when the brief wants the stylised version) and position (pan follows the path). Write the path as a function of time — closest distance, speed, pass time — and derive every curve from it.

- Arriving and leaving aren't mirror images: distance and air dull what is leaving, and how fast each half moves comes from the motion in the brief.
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

Mix the low layers dry and centred and send the rest to the space. When the brief wants more weight, add a heavily compressed copy of the sum underneath the original (parallel compression); limit last.

## UI sounds

Clicks, confirms, notifications and errors speak in the voice the product's world would have, and a set of them can use several families by meaning (in no order of preference):
- **Synthetic**: FM pairs with moving index envelopes, band-limited oscillators (`saw`, `square`) through filters with their own envelopes, pitch glides, chorus or detune for width, a space.
- **Ringing**: glass, metal, bells and tuned bars through `contact` and `resonate`, with the long decays those materials have.
- **Air, liquid, electricity, texture**: shaped noise through moving bands, drops and bubbles from fast pitch-falling sines, crackle from grains.
- **Struck bodies** when the brief's world is made of them.

A static waveform with one decay is the rejected shortcut in every family. For tonal cues the interval and its direction say something; decide what — the common reading (rising resolves, falling dismisses) is one vocabulary, not a rule (`harmony.md`, *Short tonal cues*). Length follows how often the cue is heard and how much it has to say.

## Life

- Sounds that fire in quick succession (taps, steps, clicks, hats) get several rendered variants that rotate at playback, each with small random changes in tuning, level, timing between stages and noise. A signature sound meant to be recognised can stay identical.
- Seed every random generator so a render is reproducible; vary the seed per variant.

## Space

`space(t60, predelay, damping, width, seed)` builds a stereo impulse response: sparse early reflections, then a diffuse tail whose highs die faster than its lows. Choose it from the brief, or none. `reverb(x, ir, wet_db, hp, lp)` sends a mono sum into it and filters the return. Low layers stay out of the reverb and in the centre.

## Finishing chain

In this order, with only the steps the sound needs between the first and the last:
1. High-pass below the lowest layer's job; `dc_block` after any asymmetric processing.
2. Colour, if wanted: `drive` (tanh, oversampled) on layers that need harmonics or glue.
3. Dynamics, if wanted: `compress` for glue, parallel compression for weight, `limit` last.
4. `fade` both ends so the file starts and ends at silence. Size the buffer so the tail decays inside it; a fade is not a substitute for a tail that was cut.

## Second pass

Go through every cue again before anyone hears it, against its brief:
- **Source**: is it built the way the brief's source is — an object excited through resonators rather than summed sines, a synthetic voice that moves rather than a static waveform?
- **Stages**: is a stage the brief names missing, or one there that it doesn't name?
- **Hardness, brightness, length**: do they match the brief, or only what the first pass happened to produce? Compare crest and centroid against what the brief describes.
- **Low end**: does it have a job, or should there be none?
- **Width and space**: are they what the brief asked for?
- **Repeats**: do cues that fire in succession vary, and does a signature cue stay recognisable?
- **The set**: do cues that mean different things sound different, and has the set collapsed into one default voice — knocks, beeps, swooshes?

Then check against the first pass. A refinement can overshoot in any direction — duller or harsher, boomier or thinner, wider or smaller. Compare centroid, tilt, crest and side energy with the first pass and with the brief, and correct before showing.

## Traps already paid for

- **pedalboard's `Limiter` is a maximiser**: it adds make-up gain equal to minus its threshold and hard-clips samples at 0 dBFS, so inter-sample peaks still land above 0 dBTP. Treat its threshold as how hard you push into the ceiling, then lower the level until `true_peak_db` reads under −1 (`listen.py page` does this for auditions; shipped files need it too). It also runs a fixed first stage that compresses 4:1 above −10 dBFS whatever the threshold, so it flattens a master's loudness and blunts its biggest hits well below the ceiling; when a piece's dynamics and its one hardest hit must survive the master, write a true-peak limiter of your own instead.
- **Naive square and saw waves alias** into inharmonic whistles; FM sidebands above Nyquist fold back too. Use `saw` / `square` (PolyBLEP), render FM at twice the rate and downsample, and saturate through `drive` (oversampled).
- **A moving average is not a filter**: it combs the spectrum with deep notches.
- **Cutting a sound off clicks**, and so does butting two tones end to end; both show as vertical lines on the spectrogram.
- **A contact pulse much longer than the period of the modes** leaves them barely excited and the sound dull; when a resonator sound measures darker than intended, shorten the contact before raising gains.
- **A soft contact thumps at DC**: `resonate`'s resonators pass some of a long contact pulse's low-frequency energy, so every soft strike carries a low thump that is none of the object's modes. High-pass the excitation just below the lowest mode before it reaches the resonators.
- **Per-sample Python loops are slow**: Karplus-Strong is one IIR (`lfilter`), each resonator is a biquad, and time-varying filters run block-wise with carried state (`sweep`).
- **`pluck` is out of tune in the upper register**: its loop is a whole number of samples plus the averaging filter's half sample, so a string above a few hundred hertz can sit up to about twenty cents off, and no sheet or metric shows it. For tuned music, resample each rendered note by its error (`f * (L + 0.5) / SR`, with `L` the loop length `pluck` chose); the same read-position curve can carry a pitch bend.
- **`filt` and `sweep` clamp at 10 Hz**: a biquad "lowpass" at a fraction of a hertz meant for slow drift is really a 10 Hz flutter. Draw slow wander as smoothed random keys over time instead.
