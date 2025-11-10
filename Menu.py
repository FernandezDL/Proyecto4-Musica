from jm.music.data import *
from jm.JMC import *
from jm.util import Write

# Tiempo y duraciones
TEMPO = 60.0          
CHORD_DUR = 4.0            
score = Score("MenuLoop"); score.setTempo(TEMPO)

# Armonía (D mayor / color brillante)
D6add9 = [D4, FS4, A4, E5]     # I(6/9)
Gadd2  = [G3, B3, D4, A4]      # IV(add2)
Aadd9  = [A3, CS4, E4, B4]     # V(add9)
Dmaj9  = [D4, FS4, A4, E5]     # I(maj9) cierre

# Partes
pads = Part("Pads", WARM_PAD,        0)
mar  = Part("Ostinato", MARIMBA,     1)
bass = Part("Bass",   ACOUSTIC_BASS, 2)
vib  = Part("Hook",   VIBRAPHONE,    3)

# --- Pads (sostenidos, suaves) ---
pPads = Phrase(0.0)
for ch in [D6add9, Gadd2, Aadd9, Dmaj9]:
    pPads.addChord(ch, CHORD_DUR)
pads.addPhrase(pPads)

# --- Ostinato alegre (marimba, corcheas) ---
pent_D = [D5, E5, FS5, A5, B5]  # pentatónica mayor
pMar = Phrase(0.0)
vel_ost = [46, 50, 48, 52, 46, 50, 48, 54]

start = 0.0
for _ in range(4):  # 4 acordes
    for i in range(8):
        pit = pent_D[i % len(pent_D)]
        n = Note(pit, 0.5)
        n.setDynamic(vel_ost[i % len(vel_ost)])
        pMar.addNote(n)
    start += CHORD_DUR
mar.addPhrase(pMar)

# --- Bajo caminante ligero ---
walks = [
    [D2, FS2, A2, D3],   # I
    [G2, B2, D3, G2],    # IV
    [A2, E2, A2, CS3],   # V
    [D2, A2, B2, D3],    # I (con 6/9)
]
pBass = Phrase(0.0)
for bar in walks:
    for pit in bar:
        nb = Note(pit, 1.0); nb.setDynamic(42)
        pBass.addNote(nb)
bass.addPhrase(pBass)

# --- Hook de vibráfono ---
pVib = Phrase(0.0)
motifs = [
    [(A5, 0.5), (B5, 0.5), (A5, 0.5), (FS5, 0.5)],  # sobre I
    [(B5, 0.5), (A5, 0.5), (FS5, 0.5), (E5, 0.5)],  # sobre IV
    [(A5, 0.5), (CS6,0.5), (B5, 0.5), (A5, 0.5)],   # sobre V
    [(A5, 0.5), (FS5,0.5), (E5, 0.5), (D5, 0.5)],   # cierre a I
]
t = 0.5
for motif in motifs:
    ph = Phrase(t)
    for pit, dur in motif:
        nv = Note(pit, dur); nv.setDynamic(48)
        ph.addNote(nv)
    vib.addPhrase(ph)
    t += CHORD_DUR

# Ensamble y export
score.addPart(pads)
score.addPart(mar)
score.addPart(bass)
score.addPart(vib)
Write.midi(score, "menu.mid")
