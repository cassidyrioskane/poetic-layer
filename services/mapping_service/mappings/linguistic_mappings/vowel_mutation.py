import re, random
from services.mapping_service.mappings import get_text

def vowel_mutation(motif, params=None):
    """Alters the internal sound pattern of words to evoke organic linguistic evolution."""

    text = get_text(motif)
    vowels = "aeiou"
    mutated = []
    for ch in text:
        if ch.lower() in vowels and random.random() < 0.3:
            mutated.append(random.choice(vowels))
        else:
            mutated.append(ch)
    return "".join(mutated)
