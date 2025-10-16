# services/mapping_service/seed.py
import os
import base64
import uuid
import requests
import json
from pathlib import Path

# Where to post motifs (used if running remotely)
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# Data persistence folder (matches app.py)
DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)
MOTIFS_PATH = DATA_DIR / "motifs.json"

# ---------- Text Seed Motifs ----------
TEXT_MOTIFS = [
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

# ---------- Image Seed Motifs ----------
IMG_SEEDS = [
    ("River Texture", "river_texture.png"),
    ("Mirror Study", "mirror_study.png"),
    ("Forest Glow", "forest_glow.png"),
]

IMG_DIR = Path(__file__).resolve().parent / "seed_images"


def _img_to_b64(path: Path) -> str:
    """Convert image to base64 string."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def seed_if_empty():
    """
    Seeds both text and image motifs if no motifs exist in persistent storage.
    Writes directly to motifs.json and posts to API if running live.
    """
    if MOTIFS_PATH.exists():
        try:
            with open(MOTIFS_PATH, "r", encoding="utf-8") as f:
                motifs = json.load(f)
                if motifs:
                    print(f"[seed] Motifs already exist ({len(motifs)} found). Skipping seeding.")
                    return
        except json.JSONDecodeError:
            print("[seed] Corrupt motifs.json, re-seeding from scratch.")

    print("[seed] No motifs detected — seeding defaults...")

    seeded = []

    # --- Seed text motifs ---
    for m in TEXT_MOTIFS:
        motif = {
            "id": str(uuid.uuid4()),
            "name": m["name"],
            "type": "text",
            "text": m["text"],
            "tags": ["seed"],
            "version": "1.0",
            "provenance": {"who": "seed", "when": int(uuid.uuid1().time)},
        }
        seeded.append(motif)
        print(f"[seed] Seeded: {m['name']}")

    # --- Seed image motifs ---
    for name, fname in IMG_SEEDS:
        path = IMG_DIR / fname
        if not path.exists():
            print(f"[seed] ⚠️ Missing seed image: {fname}")
            continue
        try:
            b64 = _img_to_b64(path)
            motif = {
                "id": str(uuid.uuid4()),
                "name": name,
                "type": "image",
                "content": b64,
                "tags": ["seed", "image"],
                "version": "1.0",
                "provenance": {"who": "seed", "when": int(uuid.uuid1().time)},
            }
            seeded.append(motif)
            print(f"[seed] Seeded image motif: {name}")
        except Exception as e:
            print(f"[seed] ⚠️ Failed to seed {fname}: {e}")

    # --- Save locally for persistence ---
    try:
        with open(MOTIFS_PATH, "w", encoding="utf-8") as f:
            json.dump({m["id"]: m for m in seeded}, f, ensure_ascii=False, indent=2)
        print("[seed] Saved motifs to motifs.json.")
    except Exception as e:
        print(f"[seed] ⚠️ Failed to save motifs.json: {e}")

    # --- Also try POSTing to API if online ---
    try:
        for m in seeded:
            res = requests.post(f"{BASE_URL}/motifs", json=m, timeout=5)
            if res.status_code == 200:
                print(f"[seed] Posted to API: {m['name']}")
            else:
                print(f"[seed] ⚠️ Failed to POST {m['name']}: {res.status_code}")
    except Exception as e:
        print(f"[seed] ⚠️ Skipping remote POST (likely offline): {e}")

    print("[seed] Seeding complete.")
