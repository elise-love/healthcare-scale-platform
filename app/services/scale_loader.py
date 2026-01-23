#scale_loader.py
import json
from pathlib import Path

SCALE_DIR = Path("scales") #./scales

def load_scale(scale_id: str):
    path = SCALE_DIR / f"{scale_id}.json"

    if not path.exists():
        return None

    scale = json.loads(path.read_text(encoding="utf-8"))
    return scale