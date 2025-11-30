import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


def load_json_file(filename: str) -> Any:
    """Загружает JSON-файл из /data и возвращает в Python-oбъект.
    :param filename - имя файла, например player.json
    """
    filename = filename.lstrip("/\\")
    path = DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"JSON не найден: {path}")

    with path.open('r', encoding='utf-8') as f:
        return json.load(f)
