import json
from pathlib import Path
from typing import Any


def load_json_file(filename: str) -> Any:
    """Загружает JSON-файл из /data и возвращает в Python-oбъект.
    :param filename - имя файла, например player.json
    """
    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError(f"JSON не найден: {path}")

    with path.open('r', encoding='utf-8') as f:
        return json.load(f)
