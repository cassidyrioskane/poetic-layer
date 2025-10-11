import random, re

def temporal_distortion(motif, params=None):
    text = motif.get("content", "")
    time_phrases = ["once", "again", "not yet", "already", "never", "soon", "long ago"]
    sentences = re.split(r'(?<=[.!?]) +', text)
    new = []
    for s in sentences:
        s = f"{random.choice(time_phrases).capitalize()}, {s.strip()}"
        new.append(s)
    return " ".join(new)
