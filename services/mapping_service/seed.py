# services/mapping_service/seed.py
"""
Poetic Layer Seed Script
------------------------
Seeds the backend with poetic text motifs and demo image motifs
("River Texture", "Mirror Study", "Forest Glow") on startup if the
database (in-memory store) is empty.
"""

import os
import uuid
import base64
import time
import requests
from PIL import Image  # ensures Pillow is present

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# ---- Base Text Motifs ----
motifs = [
    {
        "name": "The River Beneath the City",
        "text": (
            "Beneath the concrete avenues, a river still remembers the forest. "
            "It murmurs to itself in the dark, tracing forgotten roots and swallowed valleys. "
            "When the rain comes, the city trembles, unsure whether it belongs to the water or the dust. "
            "The people above rarely listen, but sometimes their dreams run wet and green."
        ),
    },
    {
        "name": "Mirror Logic",
        "text": (
            "Every reflection lies a little, bending the world toward its own hunger for symmetry. "
            "I see myself, then a version that thinks it understands. "
            "Truth fractures into polite repetitions, and somewhere between them, "
            "I begin to forget which face started the conversation."
        ),
    },
    {
        "name": "The Archive of Possible Suns",
        "text": (
            "In a vault beneath the observatory, there are shelves of light that never rose. "
            "Each jar holds the dawn of an unchosen world, sealed in the amber of mathematics. "
            "The astronomers say they keep them for study, but sometimes at dusk, "
            "they open one just to feel the heat of what could have been."
        ),
    },
    {
        "name": "City of Roots",
        "text": (
            "The trees beneath the pavement have not died; they have adapted. "
            "Their roots curl around pipes and cables, listening to the hum of traffic like wind through leaves. "
            "Each red light is a kind of blossom, each horn a mourning bird. "
            "At night, they dream of open sky and rain unfiltered by glass."
        ),
    },
    {
        "name": "Parliament of Mirrors",
        "text": (
            "Every hall is a committee of reflections, debating which image deserves to be real. "
            "The floor shines with indecision, while the walls vote silently for repetition. "
            "When you speak, your words return improved, eloquent, and empty."
        ),
    },
    {
        "name": "Museum of Future Light",
        "text": (
            "The curators wander in twilight, cataloging every photon that has not yet arrived. "
            "Some rays are shy, others violent with color. "
            "Visitors walk among the exhibits, leaving behind faint shadows of things that will someday cast them."
        ),
    },
]

# ---- Helper for image encoding ----
def _img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def seed_if_empty():
    from services.mapping_service.app import MOTIFS, _ensure_motif_dict

    try:
        # check if motifs already exist
        if MOTIFS:
            print("[seed] Motifs already loaded; skipping seeding.")
            return

        print("[seed] No motifs detected — seeding defaults...")

        # --- Add text motifs directly into memory ---
        for m in motifs:
            motif_obj = _ensure_motif_dict(m)
            MOTIFS[motif_obj["id"]] = motif_obj
            print(f"[seed] Seeded: {motif_obj['name']}")

        # --- Add image motifs directly into memory ---
        img_dir = os.path.join(os.path.dirname(__file__), "seed_images")
        img_files = [
            ("River Texture", "river_texture.png"),
            ("Mirror Study", "mirror_study.png"),
            ("Forest Glow", "forest_glow.png"),
        ]

        for name, fname in img_files:
            path = os.path.join(img_dir, fname)
            if os.path.exists(path):
                b64_data = _img_to_b64(path)
                motif_obj = _ensure_motif_dict({
                    "name": name,
                    "type": "image",
                    "content": b64_data,
                })
                MOTIFS[motif_obj["id"]] = motif_obj
                print(f"[seed] Seeded image motif: {name}")

        print("[seed] Seeding complete.")

    except Exception as e:
        print(f"[seed] Exception during seeding: {e}")

