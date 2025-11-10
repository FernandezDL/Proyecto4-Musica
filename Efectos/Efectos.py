from jm.music.data import *
from jm.JMC import *
from jm.util import Write

# Ajustes globales
TEMPO = 480.0  

def save(score, name):
    score.setTempo(TEMPO)
    Write.midi(score, name)

def stepped_gliss(p_start, p_end, steps, step_beats, dyn_a=72, dyn_b=36):
    ph = Phrase(0.0)
    if steps < 1: steps = 1
    for i in range(steps):
        t = float(i) / float(steps - 1 if steps > 1 else 1)
        pit = int(round(p_start + t * (p_end - p_start)))
        dur = step_beats
        dyn = int(round(dyn_a + t * (dyn_b - dyn_a)))
        n = Note(pit, dur); n.setDynamic(dyn)
        ph.addNote(n)
    return ph

# 1) LASER ZAP 
def sfx_laser_zap():
    sc = Score("sfx_laser_zap")
    lead = Part("laser", SQUARE, 0)

    gl = stepped_gliss(p_start=D7, p_end=G5, steps=14, step_beats=0.25,
                       dyn_a=86, dyn_b=34)
    lead.addPhrase(gl)

    tail = Phrase(gl.getEndTime())
    end = Note(D3, 0.5); end.setDynamic(28)
    tail.addNote(end)
    lead.addPhrase(tail)

    sc.addPart(lead)
    save(sc, "sfx_laser_zap.mid")

# 2) ENERGY IMPACT 
def sfx_energy_impact():
    sc = Score("sfx_energy_impact")

    hit  = Part("hit",  SYNTH_DRUM, 2)   # cuerpo del golpe
    fizz = Part("fizz", CELESTA,    3)   # chispas metálicas
    ring = Part("ring", VIBRAPHONE, 4)   # anillo corto

    # Golpe: dos capas graves muy cortas
    ph_hit = Phrase(0.0)
    n1 = Note(D2, 0.25); n1.setDynamic(90)
    n2 = Note(A1, 0.25); n2.setDynamic(72)
    ph_hit.addNote(n1); ph_hit.addNote(n2)
    hit.addPhrase(ph_hit)

    # Anillo: pequeño cluster que cae un poco
    ph_ring = Phrase(0.0)
    cluster = [(D5, 0.25), (FS5, 0.25), (A5, 0.25)]
    for p, d in cluster:
        nn = Note(p, d); nn.setDynamic(58)
        ph_ring.addNote(nn)
    
    nn2 = Note(C5, 0.5); nn2.setDynamic(42)
    ph_ring.addNote(nn2)
    ring.addPhrase(ph_ring)

    # Chispas: tres destellos breves arriba
    ph_fizz = Phrase(0.05) 
    for p in (D6, A6, FS6):
        n = Note(p, 0.2); n.setDynamic(56)
        ph_fizz.addNote(n)
    fizz.addPhrase(ph_fizz)

    sc.addPart(hit); sc.addPart(ring); sc.addPart(fizz)
    save(sc, "sfx_energy_impact.mid")

# 3) Pieza hallada
def sfx_found_piece():
    sc = Score("sfx_found_piece")

    arp   = Part("arp", CELESTA,     0)
    ring  = Part("ring", VIBRAPHONE, 1)
    sprk  = Part("sprk", CELESTA,    2)

    pArp = Phrase(0.0)
    seq = [D5, E5, FS5, A5, B5, D6]
    dyn = 52
    for i, p in enumerate(seq):
        n = Note(p, 0.25)      
        n.setDynamic(dyn + i*4)
        pArp.addNote(n)
    arp.addPhrase(pArp)

    pRing = Phrase(pArp.getEndTime() - 0.125) 
    n1 = Note(D6, 0.5);  n1.setDynamic(70)
    n2 = Note(A5, 0.375); n2.setDynamic(62)
    pRing.addNote(n1); pRing.addNote(n2)
    ring.addPhrase(pRing)

    # Sparkles
    pSprk = Phrase(pRing.getStartTime() + 0.125)
    for p in (FS6, B6, D7):
        s = Note(p, 0.25); s.setDynamic(60)
        pSprk.addNote(s)
    sprk.addPhrase(pSprk)

    sc.addPart(arp); sc.addPart(ring); sc.addPart(sprk)
    save(sc, "sfx_found_piece.mid")

# ---- Generar todo ----
sfx_found_piece()
sfx_laser_zap()
sfx_energy_impact()
