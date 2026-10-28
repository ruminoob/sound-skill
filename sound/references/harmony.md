# Harmony

The knowledge harmony is made from, across the languages a brief can ask for. None of it is a default and none of it is a rule: the brief's idiom chooses the language, and the reasons below are there so a convention can be used on purpose or broken on purpose. Read it before writing the notes of any piece or tonal cue.

## Contents
- Why intervals sound the way they do
- Tuning
- Pitch material
- Chords and voicing
- How chords connect
- Colour, surprise and modulation
- Other harmonic languages
- Melody and harmony together
- Harmony across a whole piece
- Short tonal cues
- Working in code

## Why intervals sound the way they do

- **The overtone series.** A pitched sound with a harmonic timbre carries partials at whole-number multiples of its fundamental: the octave, then the fifth above it, the fourth, a major third, a minor third, and ever closer intervals upward. Two notes sound smooth when many of their partials coincide (simple frequency ratios: octave 2:1, fifth 3:2, fourth 4:3) and rough when partials land close but not together, because close partials beat.
- **Roughness depends on register.** The span over which two partials beat is wide in the bass and narrow in the treble, so an interval that is clear high up turns to mud low down. This is why voicings spread out at the bottom and close up at the top, mirroring the overtone series, and why thirds and seconds deep in the bass blur.
- **Timbre and consonance belong together.** The usual consonances hold for harmonic timbres. Inharmonic timbres (bells, bars, plates, metal) have partials at other ratios, so intervals that are smooth on strings can clash on bells and the reverse. Synthesis can choose: tune a chord to the instrument's partials, shape the partials to suit the chord, or let the clash be the colour.
- **Dissonance is tension, not error.** A dissonance pulls toward a resolution; how strongly depends on the interval, the register, the timbre and what the listener expects next. Harmony is the management of that pull over time.

## Tuning

- Twelve-tone equal temperament divides the octave into twelve equal semitones of 100 cents. Every key sounds alike and modulation is free; the price is thirds that beat noticeably against their pure ratios. It is the shared default of most modern music, not a law of harmony.
- **Just intonation** tunes intervals to simple ratios: thirds and sixths become still and sweet, but a fixed tuning only works around one centre and drifts as harmony moves. Code can retune each chord to its own root, which no fixed instrument can.
- Other systems are equally available in code: other equal divisions of the octave, the tunings of traditions that never used twelve tones, expressive inflections (a blue third bent between minor and major, a leading tone sharpened toward its goal), slow detuning between voices for chorus.
- Frequency from any tuning is one formula: a reference frequency times 2 to the power of (cents / 1200), or times a ratio. Keep the tuning in one function so a whole piece can be retuned at once.

## Pitch material

- **Tonal centre.** A pitch the music returns to and rests on, established by repetition, the bass, metric weight and cadences. It can be firm, ambiguous, shifting or absent.
- **Scales and modes as colour.** Each mode is defined by its characteristic notes against the major or minor it resembles: Dorian's raised sixth, Phrygian's lowered second, Lydian's raised fourth, Mixolydian's lowered seventh, Locrian's lowered fifth. Harmonic minor brings a leading tone and an augmented second; melodic minor smooths its upper half. A mode sounds like itself only when its characteristic note is heard, in the melody or the chords.
- **Pentatonic scales** have no semitones and therefore no strong tendencies: open, stable, easy to layer.
- **Symmetric scales** (whole-tone, octatonic, chromatic) repeat at intervals smaller than the octave, so no note sounds like home: floating, suspended, uneasy.
- **Blues** sits between major and minor: the third and seventh are inflected, and dominant-seventh chords serve as stable chords rather than as tension.

## Chords and voicing

- **Construction.** Stacked thirds give triads and seventh chords, and further thirds give ninths, elevenths and thirteenths. Other stacks give other sounds: fourths and fifths (quartal and quintal chords — open, modern, without a clear root), seconds (clusters), a root and fifth alone (power chords — no major or minor), suspensions (the third replaced by a second or fourth — unresolved, waiting), added tones, a chord over a bass that isn't its root (slash chords), two chords at once (polychords).
- **Where tension lives.** The tritone inside a dominant seventh is the engine of tonal pull: its two notes want to move by step in opposite directions. A minor ninth between any chord note and a note above it is the harshest colour; this is why some extensions are avoided over some chords (the natural eleventh over a major chord sits a minor ninth above the third).
- **What can be left out.** In a dense chord the fifth goes first, then the root when the bass or the context supplies it; the third and seventh define the chord's quality and stay.
- **Voicing.** Spread low and close high. Choose doublings by what each note has to do: doubling a note that must resolve forces two voices into the same motion. The inversion is a choice about the bass line, not the chord. The top note is the one listeners follow; voicings are chosen for the line they make on top as much as for their colour. Instruments voice differently: what a hand can reach, what a section can sustain, what a synthesizer can stack without mud.

## How chords connect

- **Function in tonal music.** Chords group by role: tonic (rest), predominant (moving away), dominant (wanting home). Root motion by fifth carries the strongest pull; by step it moves along; by third it shifts colour while holding common tones.
- **Cadences are punctuation** of different weights: dominant to tonic is a full stop, a pause on the dominant is a comma, the subdominant to tonic is a softer close, and dominant to an unexpected chord (deceptive) keeps the sentence going.
- **Voice leading.** Hold common tones, move the other voices by the smallest step available, move against the bass where possible. Tendency tones have directions: a leading tone rises, a chordal seventh falls. Parallel fifths and octaves fuse two voices into one, which is why independent-voice writing avoids them and why idioms that want a block sound (power chords, planing, organum) embrace them.
- **Harmonic rhythm.** How often the chord changes is its own rhythm: changes that quicken toward a cadence create drive; a slow or static harmonic rhythm lets melody, timbre and groove carry the interest.
- **Pedal points and ostinato.** Harmony can move over a held bass (tension builds against what doesn't move), or a fixed pattern can repeat while the harmony changes around it.

## Colour, surprise and modulation

- **Tonicization**: a dominant aimed at a chord other than the tonic (a secondary dominant) borrows that chord's pull for a moment.
- **Modal mixture**: chords borrowed from the parallel mode, such as a minor subdominant or the flat sixth and seventh in a major key, darken or warm a progression without leaving the key.
- **Chromatic colour**: the Neapolitan (a major chord on the lowered second), augmented sixth chords (two notes expanding outward onto the dominant), tritone substitution (a dominant replaced by the dominant a tritone away, sharing its tritone), chromatic mediants (chords a third apart with one or no common tone — vivid, cinematic shifts with no functional logic).
- **Planing** moves one chord shape in parallel as colour rather than function.
- **Reharmonisation**: the same melody note under a different chord changes its meaning — a root sounds settled, a ninth wistful, a sharp eleventh bright and floating.
- **Modulation** moves the tonal centre: through a pivot chord both keys share, through a common tone held while everything moves around it, through a sequence, or directly. A direct jump is a known lift and reads as one. Decide what a modulation is for (a new section, a lift, a darkening, a return) and where the listener should feel it.

## Other harmonic languages

- **Modal harmony** keeps the mode's colour by avoiding the dominant-to-tonic pull: vamps on one or two chords that feature the characteristic note, cadences that arrive by step or by the mode's own chords.
- **Quartal and pentatonic harmony**: no leading tones, so nothing has to resolve; harmony floats and layers freely.
- **Static and drone harmony**: one centre held; interest moves into melody, timbre, rhythm and the overtones rising and falling inside the sound.
- **Textural and atonal writing**: register, density, clusters and the shape of the sound do the structural work that keys do elsewhere.
- **Traditions with their own systems** (maqam with intervals between the semitones, raga with its ascending and descending shapes over a drone, gamelan's slendro and pelog tunings, and many more) carry their own tuning, melodic rules and sense of rest. Work in their terms and their tuning rather than mapping them onto major and minor; code makes their intervals exact.

## Melody and harmony together

- **Chord tones and non-chord tones.** Chord tones tend to fall on strong beats; notes outside the chord give a line motion and expression: passing and neighbour notes move between chord tones, a suspension holds a note over a chord change and resolves down, an appoggiatura leans on the beat and resolves, an anticipation arrives early. Dissonance on a strong beat resolving by step is one of the most expressive moves harmony has.
- **The outer voices first.** Melody and bass are the two lines the ear follows; write them as a pair, check their intervals and motion against each other, then fill the middle.
- **Contour and peak.** A line has a shape and usually one high point; place it where the harmony is most charged or most released, on purpose.
- **Counterpoint** is the craft of independent lines: different rhythms, contrary motion, consonance where the lines meet on strong beats. Even a pad and a bass are two lines.

## Harmony across a whole piece

- A piece has a tension curve: home, departure, return, or a deliberate refusal to return. Plan where the strongest arrival is and what is withheld before it.
- Sections can be told apart by harmonic means: a new centre, a new mode, a new harmonic rhythm, a new density of chords.
- What harmony means to a listener is learned and cultural. Major and minor do not reliably mean happy and sad; brightness is better thought of as a scale (from Lydian down to Locrian) than as two moods. Choose from the feeling the brief describes and confirm it with the listener on the audition page.

## Short tonal cues

- Two or three pitches imply a chord, a key and a tension. A cue that lands on the tonic sounds finished; on the fifth or second, open; on the leading tone or a tritone, unresolved.
- Cues that live beside music are written in its key and mode so they sound like part of it, and can be voiced differently each time from that key's notes.
- The timbre changes the interval: on a bell-like voice the partials, not the fundamentals, decide whether a pair of notes is sweet or sour (see *Why intervals sound the way they do*).

## Working in code

- Represent pitch as numbers (note numbers, scale degrees or cents) and convert to frequency in one tuning function. Spell chords as intervals above a root and scales as interval sets, and derive every voicing from them instead of typing note numbers by hand: hand-typed numbers drift by a semitone or an octave without notice.
- Voice-lead by computation: for each new chord, move each voice to the nearest note of the chord that keeps the spacing and range rules the voicing needs, then check the result.
- Print the progression as note names before rendering anything, and read it as a musician would: the bass line, the top line, the tendency tones and where each goes.
- Render the harmony alone, without percussion, and read its review sheet: close intervals low in the spectrum show as thick, beating bands; a chord change shows as a shift in the stack of lines. Fix register and spacing before balancing the mix.
