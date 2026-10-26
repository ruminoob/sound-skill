# sound

A Claude skill for making sound in code: sound effects, UI sounds, notification tones, impacts, whooshes, ambiences, jingles and music loops, synthesized offline in Python.

Claude can't hear what it makes, so this skill gives it a method instead of guesses. Each sound starts as a physical event written in words: the object, its material, its stages, where the listener is, what the sound means. It is built from layers that each have their own envelope. Struck and plucked objects are excited through banks of resonators, so a mallet's contact time sets the brightness. Moving sounds change level, brightness, pitch and position from one motion model. Every sound gets a space and a finishing chain, then a second pass. The result is checked as evidence: spectrogram sheets, loudness, true peak, edge clicks and brightness curves. Finally it goes to a loudness-matched audition page where a person listens and picks.

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
| `sound/references/effects.md` | Stages and layers, excitation and resonators, motion, impacts, tonal UI sounds, space, the finishing chain |
| `sound/references/music.md` | The music brief, composition, arrangement, instruments by family, performance, balance, master |
| `sound/references/listening.md` | Reading review sheets and metrics, loudness matching, the audition manifest |
| `sound/scripts/dsp.py` | The DSP toolkit: band-limited oscillators, contact and resonators, Karplus-Strong, time-varying filters, oversampled saturation, generated rooms, reverb, tape wow, reverse swells, dynamics, loudness levelling |
| `sound/scripts/listen.py` | `check` and `page` |
| `sound/scripts/audition.html` | The audition page template |

## License

MIT
