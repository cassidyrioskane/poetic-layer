import random

def motif_merge(motif, params=None):
    """Interweaves two motifs at the word level, forming a hybrid text that merges their semantic DNA."""

    other = params.get("other_text", "")
    a = motif.get("content", "").split()
    b = other.split()
    merged = []
    while a or b:
        if random.random() < 0.5 and a:
            merged.append(a.pop(0))
        elif b:
            merged.append(b.pop(0))
    return " ".join(merged)
