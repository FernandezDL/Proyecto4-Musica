from jm.music.data import *
from jm.JMC import *
from jm.util import Write

TEMPO = 60.0           # 1 beat = 1 s
CHORD_DUR = 5.0        # 4 x 5 s = 20 s
score = Score("descanso"); score.setTempo(TEMPO)

# Armonía en D mayor
D6add9 = [D4, FS4, A4, E5]
Gadd2  = [G3, B3, D4, A4]
Bm7add4= [B3, D4, FS4, G4]
prog   = [D6add9, Gadd2, Bm7add4, D6add9]

# Partes
pads = Part("Pads", WARM_PAD, 0)
gtr  = Part("GtrArp", NYLON_GUITAR, 1)
vox  = Part("Oohs", VOICE, 2)
sub  = Part("Sub", SYNTH_BASS_2, 3)

# --- Pads (colchón lento) ---
pPads = Phrase(0.0)
for ch in prog:
    pPads.addChord(ch, CHORD_DUR)
pads.addPhrase(pPads)

# --- Sub grave (pedal suave en D) ---
pSub = Phrase(0.0)
nSub = Note(D2, CHORD_DUR * len(prog)); nSub.setDynamic(34)
pSub.addNote(nSub)
sub.addPhrase(pSub)

# --- Arpegio de guitarra (suave, 0.5 s por nota) ---
pGtr = Phrase(0.0)
vel_seq = [40, 44, 42, 46, 40, 44, 42, 46, 40, 44]
for ch in prog:
    a, b, c, d = ch[0], ch[1], ch[2], ch[3]
    pattern = [a, c, b, d]  # quebrado suave
    for i in range(10):     # 10 * 0.5 = 5 s por acorde
        pit = pattern[i % 4]
        n = Note(pit, 0.5); n.setDynamic(vel_seq[i])
        pGtr.addNote(n)
gtr.addPhrase(pGtr)

# --- Melodía "ooohs" muy tenue (1–2 notas por acorde) ---
pVox = Phrase(0.0)
vox_notes = [
    (A4, 3.0), (D5, 2.0),      # sobre D6add9
    (B4, 3.0), (A4, 2.0),      # sobre Gadd2
    (FS4,3.0), (E4, 2.0),      # sobre Bm7add4
    (A4, 2.0), (D5, 3.0),      # vuelve y cierra en D (empalma con el inicio)
]
for pit, dur in vox_notes:
    n = Note(pit, dur); n.setDynamic(38)
    pVox.addNote(n)
vox.addPhrase(pVox)

# Ensamble y exportación
score.addPart(pads)
score.addPart(sub)
score.addPart(gtr)
score.addPart(vox)
Write.midi(score, "descanso.mid")
