import re, random

def vowel_mutation(motif, params=None):
    text = motif.get("content", "")
    vowels = "aeiou"
    mutated = []
    for ch in text:
        if ch.lower() in vowels and random.random() < 0.3:
            mutated.append(random.choice(vowels))
        else:
            mutated.append(ch)
    return "".join(mutated)
