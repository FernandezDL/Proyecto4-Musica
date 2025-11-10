from music import *

# Inspiración Estudio de Caso: Kepler — “Harmonices Mundi”
# Masas planetarias (Mercurio, Venus, Tierra, Marte, Júpiter, Saturno, Urano, Neptuno — en 10²⁴ kg)

# ----------------- CONFIGURACIÓN -----------------
planetValues = [0.330, 4.87, 5.97, 0.642, 1898, 568, 86.8, 102]


minV, maxV = min(planetValues), max(planetValues)


planetPitches   = [ mapScale(v, minV, maxV, C1, C6, PENTATONIC_SCALE) for v in planetValues ]
planetDurations = [ EN ] * len(planetPitches)


melody1 = Phrase(0.0)
melody1.addNoteList(planetPitches, planetDurations)

melody2 = melody1.copy()
melody2.setStartTime(10.0)  
Mod.elongate(melody2, 2.0)  

melody3 = melody1.copy()
melody3.setStartTime(20.0)  
Mod.elongate(melody3, 4.0)  


Mod.repeat(melody1, 16)  
Mod.repeat(melody2, 7)   
Mod.repeat(melody3, 3)   


part1 = Part("EN",    89,   0); part1.addPhrase(melody1)   
part2 = Part("QN x2", 92,   1); part2.addPhrase(melody2)   
part3 = Part("HN x4", 95,   3); part3.addPhrase(melody3)   

score = Score("Exploration", 120)
for p in (part1, part2, part3):
    score.addPart(p)

# ----------------- RUN -----------------
Play.midi(score)
Write.midi(score, "Exploration.mid")