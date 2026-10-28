---
name: sound
description: Make sound in code - sound effects, UI sounds, notification and confirm tones, impacts, whooshes, ambiences, jingles, music loops and beds, standalone pieces and songs - synthesized offline in Python from a source described in words (a physical event or a synthetic voice), built with the techniques that source calls for, then given a second pass, checked as evidence (spectrogram sheets, loudness, edges, brightness curves) and auditioned by the user on a loudness-matched page. Use whenever a task makes or changes any sound - SFX for a film, site, app or game, UI clicks and chimes, a jingle, a music loop or bed, a song or piece in code (효과음, 사운드, 소리 만들어줘, UI 사운드, 알림음, 클릭음, 임팩트, 휙 소리, 트랜지션 사운드, 배경음, 음악 만들어줘, 노래 만들어줘, 곡 만들어줘, 루프, 징글, 사운드 디자인, 소리 다듬어줘). Not for editing or cutting a recording the user supplies, or for prompting an AI music service.
compatibility: Python 3 with numpy, scipy, soundfile, matplotlib, pyloudnorm and pedalboard (scripts/requirements.txt); ffmpeg for mp3.
---

# Sound

**This skill builds sound in code.** Good effects and good music can be synthesized; what fails is the shortcut — one oscillator, one decay, written in a single pass and never checked. Stay with synthesis rather than switching to samples, sound libraries or AI audio services unless the user asks for them.

Claude can't hear, so the work can't rest on taste in the moment. Every sound here is designed in words before code, built in layers that each answer to that design, given a second pass, checked as evidence, and — when it is a deliverable — judged by the user's ears on an audition page. The second pass is part of the job, not polish for later: in side-by-side listening it beat the first designed version.

`<skill>` is the folder this SKILL.md is in (in Claude Code usually `~/.claude/skills/sound`). The scripts need Python 3 with the packages in `<skill>/scripts/requirements.txt` (`python -m pip install -r <skill>/scripts/requirements.txt` if an import fails) and ffmpeg for mp3.

## Flow

| Step | Leaves in the project | Stops? |
|---|---|---|
| 1. Brief each sound in words | `sound/CUES.md` | — |
| 2. Build the first pass | `sound/*.py`, renders | — |
| 3. Check it | review sheets, metrics | — |
| 4. Second pass, check again | updated code and renders | — |
| 5. Audition | a loudness-matched page | **when the sound is a deliverable or the direction is open: the user listens** |
| 6. Ship | final files, levels, playback code | — |

Keep the sound work in a `sound/` folder in the project (or beside the film or page it belongs to): the cue sheet, the build scripts and a render command, so any sound can be regenerated and changed later. Copy `<skill>/scripts/dsp.py` into it and import from there; the project keeps working if this skill changes.

## 1. Brief each sound in words

One or two sentences per cue, written into `sound/CUES.md` before any code:

- **The source**: what makes the sound — a physical event (the object, its material and size, what strikes, rubs, blows or moves it) or a synthetic voice the product's world speaks in, described by its character and how it moves.
- **Its shape over time**: the stages a physical event goes through (contact then settling, approach then pass then departure, a strike then a bloom), how a synthetic voice moves, or that it holds still on purpose.
- **The listener**: distance and the space around them.
- **The meaning**: what the sound says in the product (done, arrived, landed, gone, wrong) and how often it will be heard.

For music the brief is its job, its form and its idiom instead (`references/music.md`, *The brief*).

Abstract sounds — a UI confirm, a digital transition — still get a described source the layers are built from, but it need not be a struck object: a synthetic voice is an equally valid source. The source comes from the product's own world (its design materials, the film's storyboard, what the product is made of), not a default set of sounds carried from project to project. Read the cue sheet as a set before building: when most cues have come out as knocks and taps on wood whatever the product is, the briefs have fallen back to a default. The brief is what every layer answers to and what review checks against.

When the project rebuilds or follows a reference site or product, carry over its sound language too, rather than inventing a world beside it. Ask before downloading the reference's sound files, keep them for analysis only (never shipped, sampled or published), measure them — `listen.py check` with `--curve`, the strongest partials, envelope shape, width, and the music's tempo and density — and brief each cue from those traits, rebuilt in code.

## 2. Build the first pass

`references/effects.md` holds the techniques for effects, `references/music.md` for music. Every sound gets a design, not a fixed structure; the techniques follow the source in the brief:

- **The source's own technique.** A struck, plucked or rubbed object is excited, not summed: a contact pulse drives a bank of resonators (`contact` → `resonate`), so contact time sets hardness and brightness by itself. A synthetic voice is FM pairs with moving index envelopes, band-limited oscillators through filters, pitch and level that move. Air, liquid and texture are shaped noise and grains.
- **Layers when the source has parts**, each with its own envelope and level. One designed voice can be the whole sound; what this skill rules out is a static waveform under one decay.
- **Stages as events in time** when the source has stages, and **motion from one model** when it moves: level, brightness, pitch and position derived together.
- **Repetition decided by use**: cues that fire in quick succession get rotating variants or small variation; a signature sound meant to be recognised can stay identical.
- **Space from the brief**, including none.
- **Hygiene on every sound**: a high-pass below its lowest job, no DC, starts and ends at silence, true peak under −1 dBTP. Colour (oversampled saturation) and dynamics (compression, parallel compression, a limiter) only where the sound needs them.
- **No digital shortcuts**: band-limited oscillators, oversampled FM and saturation, no hard cuts, no moving-average "filters".

## 3. Check it

```bash
python <skill>/scripts/listen.py check <out-dir> take1.wav take2.wav ... [--curve]
```

Writes one review sheet (waveform and log spectrogram per take on a shared time axis) and prints metrics: loudness, true peak, crest, start and end edges, spectral centroid, long-term tilt, side energy. `--curve` prints brightness and level over time, for any design that claims motion. Read every sheet and every number; `references/listening.md` says what each one shows and which defects look like what. A design claim that the numbers don't show (a sweep, a stage, a decay) isn't in the sound yet.

## 4. Second pass

Before anyone hears it, go through each cue again against its brief with the questions in `references/effects.md` *Second pass* (and `music.md` *Second pass* for music): source, stages, hardness, brightness, length, low end, width, space, repeats, and whether the set has collapsed into one default voice. Then check again and compare with the first pass: a refinement can overshoot in any direction. Keep the first pass's renders so the two can be compared, by numbers and, if the user wants, by ear.

## 5. Audition

When the sound is a deliverable, or the direction is still open, the user listens before it ships:

```bash
python <skill>/scripts/listen.py page <manifest.json> <out-dir> [--artifact]
```

It loudness-matches every take of a cue (a louder take wins any comparison, so this is never skipped), renders spectrograms and writes a self-contained page: `index.html` beside `audio/` and `img/`. The page fetches its audio, so serve the folder (`python -m http.server` inside it) rather than opening the file directly, or publish the folder wherever pages can be shared. With Claude's Artifact tool, add `--artifact` (it leaves out the document wrapper the tool adds) and publish `file_path` = `<out-dir>/index.html`, `root` = `<out-dir>`, `files` = the printed list. Takes are real alternatives — directions, the previous pass beside this one, variant sets — each with a one-line note on how it is built. The manifest format is in `references/listening.md`.

Write the user's verdict into `sound/CUES.md`. When the user rejects a quality of sound (not one cue's tuning, a kind of sound), add it to *Ruled out* below so later work avoids it.

## 6. Ship

- **Files**: WAV for effects (48 kHz), mp3 or ogg for long beds on the web; mono or stereo as the brief's width asks.
- **Levels** are relative to where the sound plays and what it sits beside; effects under music are set against the music's level, not in absolute terms, with a limiter on the sum.
- **On the web**: decode each file once into an `AudioBuffer` (`fetch` + `decodeAudioData`), create or resume the `AudioContext` on the first user gesture, play with `AudioBufferSourceNode` (exact timing, overlaps allowed), rotate variants, give the visitor a mute control that is remembered, never autoplay sound. Which actions sound, and how often, is decided with the product; the more often a cue fires, the more its length and level have to allow for it.

## Ruled out

The kinds of sound this skill exists to replace:

- The one-pass shortcut: a lone sine or square beep with one exponential decay; a raw noise burst standing in for an impact or a whoosh; two tones butted end to end; sounds that stop by being cut off (a click) instead of decaying; the same file repeated identically.
- Wooden knocks as the default answer: woodblock- or moktak-like taps (short, dry, inharmonic clicks) used for UI sounds and cues whatever the product's world is.
- Music as a rigid grid of oscillator block chords and a square-wave melody on every beat, with no performance, no balance and an ending that just stops.

## Files

- `references/effects.md` — staging and layering, excitation and resonators, motion, impacts, UI sounds from synthetic and ringing voices, life, space, the finishing chain, the second pass, traps already paid for
- `references/music.md` — the music brief (job, form and idiom), composition, arrangement, instruments by family, performance, space and balance, master, the second pass; genre conventions as tools of their idiom, never defaults
- `references/listening.md` — what the review sheet and each metric show, defect signatures, brightness curves, loudness matching, the audition manifest and page
- `scripts/dsp.py` — the toolkit: envelopes, band-limited oscillators, contact and resonators, Karplus-Strong, biquads and time-varying filters, oversampled saturation, generated rooms, reverb, chorus, ping-pong, tape wow, reverse swells, compression, limiting, sidechain, loudness levelling
- `scripts/listen.py` — `check` (review sheet, metrics, curves) and `page` (loudness-matched audition page)
- `scripts/requirements.txt` — the Python packages the scripts need
- `scripts/audition.html` — the audition page template `listen.py page` fills
