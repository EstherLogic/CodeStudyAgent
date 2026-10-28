
import json
from pathlib import Path
from typing import Any


class JsonStorage:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self, default: Any = None) -> Any:
        if not self.file_path.exists():
            return default if default is not None else {}

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return default if default is not None else {}

    def save(self, data: Any) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
