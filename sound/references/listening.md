# Listening without ears

Evidence stands in for ears on defects and on whether the design made it into the sound. Taste is the user's: they listen on the audition page.

## `listen.py check`

```bash
python <skill>/scripts/listen.py check <out-dir> a.wav b.wav ... [--curve]
```

Writes `<out-dir>/review.png`: for each file, its waveform (both channels) above a log-frequency spectrogram, all on one time axis so length differences are real. Prints one line of metrics per file and writes them to `<out-dir>/metrics.json`. Long files get a longer analysis window. Open the sheet as an image and read it.

### What the sheet shows

- **A vertical line across all frequencies at the end** — the sound was cut off: a click.
- **A vertical line between two notes** — two tones butted end to end, or a discontinuity at a splice.
- **Lines falling or mirroring at odd angles above a bright tone** — aliasing from a naive waveform or un-oversampled FM or saturation.
- **Horizontal lines that never change** — a static oscillator; unless the brief asks for a steady tone, nothing in the sound is alive.
- **Noise filling the frame evenly with no shape** — hiss nobody shaped. Unless the brief wants a steady texture, a noise layer has a band that moves with the event. The display range can hide a sweep, so confirm motion with `--curve`.
- **A low band that outlasts the event** — a sub or rumble that drones instead of landing.
- **A few short, dry, inharmonic lines in the low kilohertz that die within tens of milliseconds** — a wood knock. Unless the brief is wood, the default has crept in.
- Where the brief has **stages**, they show as separate onsets; in a resonating object, **higher modes** fade before lower ones; **tails** fade into the black instead of stopping.

### The metrics

| Metric | What it tells |
|---|---|
| `lufs` | Integrated loudness (short blocks for short files). Only meaningful between takes of one cue. |
| `true_peak_db` | Peak after 4× oversampling. Anything above −1 dBTP will clip after encoding. |
| `crest_db` | Peak to RMS. A very high crest on a short sound means one spike carries it; a very low one means it is squashed. |
| `first_sample_db`, `last_2ms_db` | The edges, relative to the peak. A start near the peak level clicks on; an end above about −40 dB clicks off. |
| `centroid_hz` | Brightness. Compare with the brief and with the previous pass; a large move either way deserves a look. |
| `tilt_db_oct` | Slope of the long-term spectrum from 100 Hz to 10 kHz. Steeper is darker. Useful for music against a reference, and for comparing passes. |
| `side_db` | Side energy relative to mid. Very low is mono; near zero is very wide or out of phase. |

### `--curve`

Prints the spectral centroid and the level relative to the loudest moment every 50 ms (about 60 points for long files). Use it whenever the brief claims motion — brightness rising into a pass and falling after, a bloom, stages — and check that the numbers draw that shape.

## Loudness matching

Any comparison between takes is loudness-matched first; otherwise the louder take wins regardless of quality. `listen.py page` matches every take of a cue to one loudness, lowered if needed so every take stays under −1 dBTP. A set of variants (rotating taps) is measured on its first file and moved together, keeping their natural differences.

## `listen.py page`

```bash
python <skill>/scripts/listen.py page <manifest.json> <out-dir> [--artifact]
```

The manifest, with paths relative to it:

```json
{
  "title": "Name of the page",
  "intro": "One or two sentences on what is being compared.",
  "cues": [
    {
      "id": "short-id",
      "name": "Cue name",
      "brief": "The cue's brief from CUES.md.",
      "takes": [
        { "label": "Short label", "note": "How this take is built, in one line.", "files": ["renders/cue_take.wav"] },
        { "label": "Short label", "note": "…", "files": ["renders/cue_v-0.wav", "renders/cue_v-1.wav"] }
      ]
    }
  ]
}
```

A take with several files is a variant set: the page rotates through them and offers an "× 8" button that plays the take eight times in quick succession, which is where identical repeats give themselves away.

It writes `<out-dir>/audio/` (WAV for short takes, mp3 for anything over 8 s), `img/` (spectrogram strips), `review/` (a sheet per cue, for you), `metrics.json` and `index.html`, and prints the list of files the page needs. The page fetches its audio, so it has to be served over http: run `python -m http.server` in `<out-dir>` and open the printed address, or publish the page and its files wherever the user can open them. For Claude's Artifact tool, build it with `--artifact` and publish `file_path` `<out-dir>/index.html`, `root` `<out-dir>`, `files` the printed list. Sound in the page starts on a click; each take shows its spectrogram with a playhead, its length and whether its edges click.

Labels are what the user will say back: keep them short and distinct. When the comparison is pass against pass, say so in the notes.
