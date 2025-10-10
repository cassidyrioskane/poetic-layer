# services/mapping_service/seed.py
import requests
import os

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

motifs = [
    {"name": "The River Beneath the City", "text": (
        "Beneath the concrete avenues, a river still remembers the forest. "
        "It murmurs to itself in the dark, tracing forgotten roots and swallowed valleys. "
        "When the rain comes, the city trembles, unsure whether it belongs to the water or the dust. "
        "The people above rarely listen, but sometimes their dreams run wet and green."
    )},
    {"name": "Mirror Logic", "text": (
        "Every reflection lies a little, bending the world toward its own hunger for symmetry. "
        "I see myself, then a version that thinks it understands. "
        "Truth fractures into polite repetitions, and somewhere between them, "
        "I begin to forget which face started the conversation."
    )},
    {"name": "The Archive of Possible Suns", "text": (
        "In a vault beneath the observatory, there are shelves of light that never rose. "
        "Each jar holds the dawn of an unchosen world, sealed in the amber of mathematics. "
        "The astronomers say they keep them for study, but sometimes at dusk, "
        "they open one just to feel the heat of what could have been."
    )},
    {"name": "City of Roots", "text": (
        "The trees beneath the pavement have not died; they have adapted. "
        "Their roots curl around pipes and cables, listening to the hum of traffic like wind through leaves. "
        "Each red light is a kind of blossom, each horn a mourning bird. "
        "At night, they dream of open sky and rain unfiltered by glass."
    )},
    {"name": "Parliament of Mirrors", "text": (
        "Every hall is a committee of reflections, debating which image deserves to be real. "
        "The floor shines with indecision, while the walls vote silently for repetition. "
        "When you speak, your words return improved, eloquent, and empty."
    )},
    {"name": "Museum of Future Light", "text": (
        "The curators wander in twilight, cataloging every photon that has not yet arrived. "
        "Some rays are shy, others violent with color. "
        "Visitors walk among the exhibits, leaving behind faint shadows of things that will someday cast them."
    )},
]

def seed_if_empty():
    try:
        r = requests.get(f"{BASE_URL}/motifs")
        if r.status_code != 200:
            print(f"[seed] Unable to query motifs: {r.status_code}")
            return
        if r.json():
            print("[seed] Motifs already exist; skipping seeding.")
            return

        print("[seed] No motifs detected — seeding defaults...")
        for m in motifs:
            res = requests.post(f"{BASE_URL}/motifs", json=m)
            if res.status_code == 200:
                print(f"[seed] Seeded: {m['name']}")
            else:
                print(f"[seed] Failed ({res.status_code}): {res.text}")
        print("[seed] Seeding complete.")
    except Exception as e:
        print(f"[seed] Exception during seeding: {e}")
