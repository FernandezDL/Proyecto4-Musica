from jm.music.data import *
from jm.JMC import *
from jm.util import Write 
from random import choice, uniform
from music import *

# ----------------- CONFIGURACIÓN -----------------
TEMPO = 60.0
CHORD_DUR = 5.0      
MELO_VEL = 70

# Progresión (D Lydian color)
Dmaj7 = [D4, FS4, A4, CS5]
Aadd9 = [A3, CS4, E4, B4]
Gmaj7 = [G3, B3, D4, FS4]
Em9   = [E3, G3, B3, D4, FS4]

# --- Score y Parts ---
score = Score("Tema_principal")
score.setTempo(TEMPO)

pads  = Part("Pads", SYNTH_STRINGS_1, 0)    
stars = Part("Stars", CELESTA,        2)    
echo  = Part("StarsEcho", CELESTA,    3)     

# --- Pads ---
pPads = Phrase(0.0)
for chord in [Dmaj7, Aadd9, Gmaj7, Em9]:
    pPads.addChord(chord, CHORD_DUR)
pads.addPhrase(pPads)

# --- Melodía  ---
pLead = Phrase(0.0)
mel = [
    (D5,  2.5),
    (E5,  2.5),
    (FS5, 2.5),
    (A5,  2.5),
    (B4,  2.5),
    (A4,  1.5),
    (FS4, 2.0),
    (D5,  3.0),
]
for pit, dur in mel:
    n = Note(pit, dur)
    n.setDynamic(MELO_VEL)
    pLead.addNote(n)

# --- Estrellas  ---
LOOP_LEN = 20.0
N_TWINKLES = 16
TWINKLE_PITCHES = [D6, E6, FS6, GS6, A6, B6, CS7, D7]  


events = []
for _ in range(N_TWINKLES):
    start = uniform(0.0, LOOP_LEN - 0.35)
    pit   = choice(TWINKLE_PITCHES)
    dur   = uniform(0.18, 0.40)
    vel   = int(uniform(46, 72))
    n = Note(pit, dur); n.setDynamic(vel)

    ph = Phrase(start)
    ph.addNote(n)
    stars.addPhrase(ph)

    events.append((start, pit, dur, vel))

for start, pit, dur, vel in events:
    e = Note(pit, dur * 0.9)
    e.setDynamic(int(vel * 0.55))
    phE = Phrase(start + 0.2)
    phE.addNote(e)
    echo.addPhrase(phE)

# --- RUN ---
score.addPart(pads)
score.addPart(stars)
score.addPart(echo)

Play.midi(score)
Write.midi(score, "tema_principal.mid")