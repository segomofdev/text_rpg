import json
import pathlib
from typing import Dict


def load_json_file(path: str) -> Dict:
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Файл {path} не найден")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)
