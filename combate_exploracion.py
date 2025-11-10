from music import *

# ----------------- CONFIGURACIÓN -----------------
TITLE        = "Combate exploracion"
TEMPO_BPM    = 124
OUTPUT_MIDI  = "combate_exploracion.mid"

LOOP_BARS = 10

STRUCTURE = [("loop", LOOP_BARS)]

TRACKS = {
    "PIANO": (ELECTRIC_PIANO, 0),   
    "BASS":  (FINGERED_BASS, 1),
    "DRUMS": (0, 9),                
}

# ----------------- PITCH -----------------
_NOTE_TO_SEMITONE = {
    "C":0, "C#":1, "Db":1, "D":2, "D#":3, "Eb":3, "E":4,
    "F":5, "F#":6, "Gb":6, "G":7, "G#":8, "Ab":8, "A":9,
    "A#":10, "Bb":10, "B":11
}

def to_midi(p):
    if isinstance(p, (int, long)): return int(p)
    note, octv = p[:-1].strip(), int(p[-1])
    return (octv + 1) * 12 + _NOTE_TO_SEMITONE[note]

def add_notes(phrase, notes):
    for p, d in notes:
        phrase.addNote(Note(p if p==REST else to_midi(p), d))

def add_chord_stab(phrase, chord_pitches, dur):
    for p in chord_pitches:
        phrase.addNote(Note(to_midi(p), dur))

# ----------------- PROGRESIÓN -----------------

PROG = [
    (["F3","Ab3","C4"], "F2"),
    (["Db3","F3","Ab3"], "Db2"),
]

# ----------------- DRUMS -----------------
def make_drum_layer(pitch, hit_positions, bars, slots_per_bar=16):
    ph = Phrase(0.0)
    for _ in range(bars):
        for s in range(slots_per_bar):
            ph.addNote(Note(pitch if s in hit_positions else REST, SN))
    return ph

def house_kick(bars):
    hits = {0,4,8,12}
    return make_drum_layer(36, hits, bars)

def house_clap(bars):
    hits = {4,12}
    return make_drum_layer(39, hits, bars)

def hat_offbeat(bars):
    hits = {2,6,10,14}
    return make_drum_layer(46, hits, bars)

def hat_closed_16(bars):
    hits = {1,3,5,7,9,11,13,15}
    return make_drum_layer(42, hits, bars)

def shaker_16(bars):
    hits = set(range(16))
    return make_drum_layer(70, hits, bars)

# ----------------- PATTERNS -----------------
def piano_loop(bars):
    ph = Phrase(0.0)
    prog_len = len(PROG)
    for i in range(bars):
        chords, _ = PROG[i % prog_len]
        

        for beat in range(4):
            add_chord_stab(ph, [p.replace("3","4") for p in chords], SN)
            add_notes(ph, [(REST, EN - SN)])
    return ph

def bass_loop(bars):
    ph = Phrase(0.0)
    prog_len = len(PROG)
    for i in range(bars):
        _, root = PROG[i % prog_len]
        low = root
        high = root[0]+str(int(root[1])+1) if len(root)==2 else "F3"
        

        add_notes(ph, [(low, EN)])
        add_notes(ph, [(REST, SN)])
        add_notes(ph, [(high, SN)])
        add_notes(ph, [(REST, QN)])
        add_notes(ph, [(low, EN)])
        add_notes(ph, [(REST, SN)])
        add_notes(ph, [(high, SN)])
        add_notes(ph, [(REST, QN)])
    return ph

# ----------------- SECCIÓN LOOP -----------------
def sec_loop(bars=10):
    """
    Loop perfecto sin intro ni outro - todos los elementos presentes
    desde el inicio para que el loop sea transparente
    """
    piano = piano_loop(bars)
    bass  = bass_loop(bars)
    kick  = house_kick(bars)
    clap  = house_clap(bars)
    ohh   = hat_offbeat(bars)
    hh    = hat_closed_16(bars)
    shkr  = shaker_16(bars)
    
    return {
        "PIANO": [piano], 
        "BASS": [bass], 
        "DRUMS": [kick, clap, ohh, hh, shkr]
    }, bars

SECTIONS = {"loop": sec_loop}

# ----------------- MOTOR -----------------
def make_parts(tracks):
    return {n: Part(n, prog, ch) for n,(prog, ch) in tracks.items()}

def build_score(structure, sections, tracks, title, tempo):
    score = Score(title)
    score.setTempo(tempo)
    parts = make_parts(tracks)
    t = 0.0
    
    for tok in structure:
        name, bars = tok if isinstance(tok, tuple) else (tok, LOOP_BARS)
        name = name.strip().lower()
        section_dict, bars = sections[name](bars)
        
        for track, value in section_dict.items():
            phs = value if isinstance(value, list) else [value]
            for ph in phs:
                ph.setStartTime(t)
                parts[track].addPhrase(ph)
        t += bars * WN
    
    for p in parts.values():
        score.addPart(p)
    return score

# ----------------- RUN -----------------
if __name__ == "__main__":
    sc = build_score(STRUCTURE, SECTIONS, TRACKS, TITLE, TEMPO_BPM)
    Play.midi(sc)
    Write.midi(sc, OUTPUT_MIDI)
    print("   MIDI exportado:", OUTPUT_MIDI)