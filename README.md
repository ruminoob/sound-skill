# sound

A Claude skill for making sound in code: sound effects, UI sounds, notification tones, impacts, whooshes, ambiences, jingles, music loops, standalone pieces and songs, synthesized offline in Python.

Claude can't hear what it makes, so this skill gives it a foundation and a method instead of guesses. The foundation is what the ear hears as pleasant, rich, cheap or tiring — spectrum and timbre, envelope, roughness, loudness, life, space, expectation, fatigue — and the harmony behind any harmonic language, each with the reasons behind it. Each sound starts as a source written in words: a physical event (an object, its material, what strikes or moves it) or a synthetic voice described by its character and movement, plus where the listener is and what the sound means. The techniques follow that source: struck and plucked objects are excited through banks of resonators, synthetic voices are built from moving FM and filters, moving sounds derive level, brightness, pitch and position from one motion model. Layers, space and processing are used when the brief calls for them. Music starts from its job, its form and its idiom, with no genre assumed. Every sound gets a second pass against its brief, is checked as evidence (spectrogram sheets, loudness, true peak, edge clicks, brightness curves) and goes to a loudness-matched audition page where a person listens and picks.

## Install

**Claude Code**: copy the `sound` folder into your skills folder.

```bash
git clone https://github.com/ruminoob/sound-skill.git
cp -r sound-skill/sound ~/.claude/skills/sound
```

**Claude apps**: zip the `sound` folder and upload it as a skill in Claude's settings.

The scripts need Python 3 and ffmpeg:

```bash
python -m pip install -r ~/.claude/skills/sound/scripts/requirements.txt
```

## Use

Ask Claude for a sound: "make a confirm sound for the checkout button", "add an impact for the logo reveal", "score this 30-second film in code". The skill loads on its own for sound work.

The two scripts also run by hand:

```bash
# review sheet (waveform + spectrogram per file) and metrics; --curve prints brightness over time
python sound/scripts/listen.py check out/ take-a.wav take-b.wav --curve

# loudness-matched audition page from a manifest of cues and takes
python sound/scripts/listen.py page manifest.json audition/
cd audition && python -m http.server
```

The manifest format is in `sound/references/listening.md`.

## Files

| Path | Contents |
|---|---|
| `sound/SKILL.md` | The method: brief, build, check, second pass, audition, ship |
| `sound/references/ear.md` | What the ear hears as pleasant, rich, cheap or tiring, and how to read it from spectrograms and metrics |
| `sound/references/harmony.md` | Intervals and the overtone series, tuning, pitch material, chords and voicing, voice leading, colour and modulation, other harmonic languages, melody against harmony, short tonal cues |
| `sound/references/effects.md` | Stages and layers, excitation and resonators, motion, impacts, UI sounds from synthetic and ringing voices, space, the finishing chain, the second pass |
| `sound/references/music.md` | The music brief (job, form, idiom), composition, arrangement, instruments by family, performance, balance, master |
| `sound/references/listening.md` | Reading review sheets and metrics, loudness matching, the audition manifest |
| `sound/scripts/dsp.py` | The DSP toolkit: band-limited oscillators, contact and resonators, Karplus-Strong, time-varying filters, oversampled saturation, generated rooms, reverb, tape wow, reverse swells, dynamics, loudness levelling |
| `sound/scripts/listen.py` | `check` and `page` |
| `sound/scripts/audition.html` | The audition page template |

## License

MIT
