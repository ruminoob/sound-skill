# Music in code

Music is built the way a composer and a producer build a piece: a brief, composition, arrangement, instruments, performance, space and balance, master. Each stage is its own pass with its own check; skipping any of them gives the rejected result (a grid of oscillators). Nothing here assumes a genre, an ensemble, a tempo, a harmonic language or a level: all of them come from the brief, and the brief comes from what the music is for: a product, a film or page it serves, or a piece or song that stands on its own.

## The brief

Before any notes, write into `sound/CUES.md`:
- **The job**: what the music does — for a product or film (carries a reveal, sits under narration, loops behind an interface, opens or closes) or on its own, as a piece or a song to be listened to — its length, and how its energy moves over that length.
- **The form**: the shape it takes — a cue cut to a film's grid, a loop, a song with its sections, a through-composed piece, variations, a single evolving texture — written as sections with their lengths and what changes in each.
- **The idiom**: the ensemble (acoustic, electronic, orchestral, a single instrument, percussion alone, a hybrid), the harmonic language (functional, modal, static and drone-based, textural), the time feel (a steady pulse, a played and breathing tempo, free time) and the texture. Chosen from the product's world, or for a piece that stands alone from what the user asks for and what it should feel like; not carried over from the last piece.

The idiom decides which tools below apply. A convention belongs to an idiom: use it when the brief's idiom calls for it, never as a default.

## Composition

- **Harmony** in the brief's language, with voicings spaced the way the chosen instruments would actually play them. Where voices move independently, each moves to the nearest note it can. Parallel motion is something an idiom chooses (power chords, chord stabs, planed harmony); when the idiom doesn't, chords that jump as one block sound generated.
- **Rhythm** that is performed, not printed: the feel the idiom asks for (tight, pushed, laid back, swung, rubato), accents that shape the bar, rests that let it breathe. One velocity on every beat is a metronome.
- **Material** the piece is built from — a motif, a riff, a hook, a progression, a texture — and a plan for how it changes over the piece. Where the idiom lives on repetition (a groove, a loop, minimalism), the change lives in details around the material rather than in the material itself.
- **Form and length** follow the brief: a film's length in whole bars where it is cut to a grid, a loop that returns cleanly to its start, a phrase that ends where the scene does, a song's sections in the order and proportions the song wants.
- **In a song**, the lead line carries it: give it the phrasing of a sung line — breaths, held notes, phrase ends, a contour that leads to the part meant to be remembered — whatever plays it, and arrange around it.

Write the timing in the project's build script — bar and beat to seconds, plus whatever deviation the time feel needs — and place every event into its part's buffer with `place`.

## Arrangement

- Plan density and register over time: what enters, what leaves, where the piece is thinnest and fullest, where it is high and low.
- **Section changes** are shaped on purpose, in the piece's own vocabulary: marked (a breath, a pickup, a swell, a fill, a change of register, key or texture) or blurred where the piece should flow without seams.
- **An ending chosen for the piece**: a resolution that rings out, a fade, an open or unresolved stop, a hard cut. The rejected ending is the one nobody chose — music that simply stops where the render did. A loop's end joins its start without a seam.

## Instruments

Design each instrument like an effect — its own excitation, body, stages and space — by family:
- **Struck** (drums, mallets, bells, piano): a `contact` pulse through `resonate` modes. Membranes and bells are strongly inharmonic; a tighter drumhead drops in pitch as it settles; a piano is struck strings, slightly inharmonic, several strings per note a hair apart.
- **Plucked** (strings, harps, guitars): `pluck`, then the instrument's body as resonators after the string.
- **Bowed and blown**: a continuous excitation — band-limited friction for a bow, breath noise plus a harmonic source for wind — through resonators or moving formant bands (`sweep`), with vibrato that arrives after the onset and a breath or bow-noise layer.
- **Voice-like**: a harmonic source through formant bands that move between vowels.
- **Electronic**: band-limited oscillators, FM pairs with index envelopes rendered at twice the rate, filters with their own envelopes. Electronic instruments are idiomatic when the brief is electronic; they are still designed, never a static waveform.
- **Texture**: filtered or granular noise and resonant drones shaped over time.

For every family, how hard a note is played changes both its level and its timbre, and every note has its own attack, sustain and release character. `dsp.py` covers struck, plucked and electronic sources directly; bowed, blown and voice-like sources are built from its parts.

## Performance

Play every part as a player would in that idiom: timing that deviates in the idiom's way (tight where a machine plays, loose where a hand does), dynamics that shape phrases rather than single notes, articulation, chords spread where the instrument spreads them, the beat that matters accented. Nothing quantized or identical unless the idiom is literally mechanical.

## Space and balance

Without ears, the balance is set by measurement and checked by measurement:
- **Spaces**: the ensemble sits in the space the brief names — a room, a hall, an imagined space — with the parts sharing it through the same impulse response, wetter and darker for what sits further back, unless the piece sets spaces against each other on purpose.
- **Roles**: decide each part's loudness relative to the others from its role (lead, support, bed, pulse) and set it with `level(part, target)`.
- **Registers**: each part owns a range; filter away what a part doesn't need there. One part owns the low end at any moment.
- **Placement**: positions follow the ensemble's own logic (where players would stand, or where a production would put them); low parts usually sit centred.
- **Movement** on sustained parts by the idiom's own means: vibrato, bow and breath swells, tremolo, filter motion, tape movement.
- Production conventions — ducking parts under a pulse (`duck`), tape `wow`, reverse swells (`swell`), drops, a swing grid — are tools of particular idioms: reach for them when the brief's idiom uses them.

Check the sum with `listen.py check`: tilt, side energy and crest against the previous pass, and against a reference recording if the user gives one (measure it with the same command).

## Master

Keep the dynamics the idiom needs — wide for acoustic and cinematic music, denser for music driven by a pulse — then light glue where it helps, `limit` last, and the destination's loudness with a true-peak margin. The final level for an audition is set by `listen.py page`.

## Second pass

Ask of every piece, whatever its idiom:
- Are the section changes and the ending shaped the way the brief chose — marked or blurred, resolved or left open?
- Who owns the low end at each moment, and where do two parts fight for one register?
- Does anything hold perfectly still that a player would move — level, timbre, pitch, timing?
- Does each instrument's timbre change with how hard it is played?
- Is anything identical or quantized where the idiom wants a player?
- Do the spaces sound chosen — one shared place, or contrast on purpose?

Then compare tilt, side energy and crest with the first pass before showing.
