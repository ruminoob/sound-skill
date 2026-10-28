# The ear: what makes a sound pleasant

What a listener feels as pleasant, rich, cheap, harsh or tiring, and why. This is the ground every brief stands on: the techniques in `effects.md` and `music.md` are how a sound is made, this is what the ear does with it. Pleasant is not always the goal — an error, a warning, a horror cue may want roughness on purpose — so read it as knowledge for choosing, not a target. Harmony has its own file (`harmony.md`); this one covers everything around it.

## Contents
- The shape of pleasantness
- Spectrum and timbre
- Time and envelope
- Beating and roughness
- Loudness and dynamics
- Life
- Space and width
- Expectation and resolution
- Context, repetition and fatigue
- Reading pleasantness from the evidence

## The shape of pleasantness

Psychoacoustics describes sensory pleasantness with a few dimensions: it falls as a sound gets **sharper** (more weight high in the spectrum), **rougher** (fast beating, buzz), and **louder** than its situation needs, and it rises with **tonality** (clear pitch rather than noise). On top of the senses sit learned layers: whether the sound fits what the listener sees, whether it resolves what it set up, how familiar it is, how often it has been heard today. A pleasant sound is not a bland one: interest needs some tension, some edge, some surprise, held in balance with these.

## Spectrum and timbre

- **The presence band.** The ear canal resonates in the low kilohertz, a few octaves above middle C, so hearing is most sensitive there. Energy in that band reads as clarity and presence; too much, or a narrow peak in it, reads as harsh, nasal or fatiguing. An unpleasant synthesized sound most often has its problem here.
- **Air and sheen.** Smooth, gently falling energy above the presence band reads as air and expense. Broadband, static energy up there reads as hiss.
- **Warmth and mud.** Fullness in the low mids reads as warmth; several sounds piling up there read as mud. Low end without definition reads as boom.
- **Slope.** Natural sounds lose energy as frequency rises, and the ear treats that falling tilt as natural. A flat or rising spectrum reads as synthetic, bright to the point of harsh, or small.
- **Harmonics.** Partials at whole-number multiples fuse into one rich tone. Low even harmonics (octaves, the fifth above) blend and sound warm and full; odd harmonics sound hollow or reedy; many high harmonics of equal strength sound buzzy. This is the difference between kinds of saturation: asymmetric drive adds even harmonics, symmetric drive adds odd ones.
- **A little inharmonicity, a little noise.** Slight stretching of partials (as in a piano), slight detuning between voices, a thread of breath or bow noise make a tone feel physical and alive. A lot becomes metallic, sour or hissy.
- **Digital junk.** Aliasing, clipping and quantisation add partials unrelated to the pitch. The ear reads them instantly as cheap, even when it can't name them.

## Time and envelope

- **Attacks** carry information: what struck, how hard, where. An attack that is only a broadband spike startles and tires; one softened slightly reads refined; one softened too far reads mushy and late. The attack should belong to the source.
- **Decays** in nature are roughly exponential, and higher partials die before lower ones, so a sound darkens as it fades. Everything decaying together, or decaying in a straight line, reads synthetic.
- **Endings** that fade into silence or into a space feel finished; a sound that stops mid-decay feels broken.
- **Length** has to fit the job: a cue that outstays its action feels slow, one shorter than its action feels thin.

## Beating and roughness

- Two close frequencies beat at their difference. Slow beating (a few times a second) is shimmer and chorus — the life in a detuned pad, a pair of bell partials, an ensemble. Fast beating (tens of times a second) is roughness: buzz, grit, unease. Close intervals deep in the bass sit in that rough zone, which is why they turn to mud (`harmony.md`, *Why intervals sound the way they do*).
- Slow modulation of level (tremolo) or pitch (vibrato) draws attention and adds life at musical rates and depths; too deep or too fast, it reads as wobble or warble.
- Comb filtering — a sound mixed with a slightly delayed copy of itself — hollows the tone and makes it sound phasey and cheap unless it is the effect being made.

## Loudness and dynamics

- Beyond what the situation needs, louder stops sounding better and starts sounding aggressive, and loud bright sounds tire fastest. A sound only has to be as loud as its message.
- Contrast between quiet and loud is where much of the interest lives; squeezing it out (heavy compression and limiting) makes sound tiring as well as flat.
- The ear's balance shifts with level: at low playback volume bass and the extreme top fall away. A sound that only works loud will sound thin when played quietly, and many sounds are played quietly.

## Life

- Nothing in nature repeats exactly. Small variations in pitch, timing, level and timbre between repeats, and slow drift inside a sustained sound, read as alive; perfect repetition reads as a machine. When the brief is a machine, that is the point.
- Sustained sounds that never move tire the ear; slow movement in filter, pitch, level or width keeps them breathing.
- Performance belongs to sound effects too: a hand presses differently each time, an object never lands twice the same way.

## Space and width

- A space tells the listener where the sound is: early reflections give size and distance, the tail gives the room. Air absorbs highs, so natural tails are darker than their sources; a tail as bright as the dry sound reads artificial, which can be the aim. Too much space makes a sound distant and washy; none makes it close and intimate — both are choices.
- Width from small differences between the ears (decorrelation, slight detune, reflections) feels enveloping. Low frequencies carry no useful direction and feel solid when centred. Two channels that cancel when summed sound hollow and vanish on mono speakers.

## Expectation and resolution

- Listeners predict constantly. Pleasure comes from predictions that are met, and from small, well-placed surprises that are then made sense of; constant predictability is dull, constant surprise is noise.
- Tension and release is the same mechanism at every scale: a dissonance resolving, a rising figure landing, a build arriving, a whoosh ending on its impact. A sound that sets something up and doesn't pay it off feels wrong unless leaving it open is the meaning.

## Context, repetition and fatigue

- **Fit.** A sound that matches what the listener sees and touches — its weight, its material, its speed — feels right before it is judged beautiful. A beautiful sound that doesn't fit its action feels wrong.
- **Repetition.** Pleasantness falls with every hearing. The more often a sound plays, the shorter, softer and gentler it usually needs to be, and the more it gains from variation; a sound heard once can afford size and detail, and a signature meant to be recognised keeps its identity.
- **Familiarity.** Known gestures are easy to like and quickly become cliché; a sound that borrows a familiar shape and gives it its own material lands between the two.
- **Culture and taste.** What sounds sweet, sad, cheap or premium is partly learned. The user's ear on the audition page is the final judge.

## Reading pleasantness from the evidence

The metrics in `listening.md` are proxies, not verdicts:
- **Sharpness**: `centroid_hz` and `tilt_db_oct`. A high centroid or a flat tilt for a sound meant to feel warm or soft says it is too sharp.
- **Harsh peaks**: on the review sheet, a bright band sitting in the low kilohertz for the whole sound.
- **Spikes**: a very high `crest_db` on a short sound says the attack carries everything.
- **Roughness**: thick, flickering bands low in the spectrogram where notes or partials sit close.
- **Digital junk**: lines in the spectrogram that are not multiples of the pitch and move against it.
- **Life**: horizontal lines that never change, repeats with identical sheets.
- **Width**: `side_db` — near silence is mono, very high warns of a sound that will cancel on mono speakers.
