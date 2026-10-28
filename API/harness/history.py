
import json
from pathlib import Path


class ConversationHistory:
    """Persist conversation messages between program runs."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.messages = self.load()

    def load(self) -> list[dict]:
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            return data if isinstance(data, list) else []

        except (json.JSONDecodeError, OSError):
            return []

    def add_message(self, role: str, content: str) -> None:
        if role not in {"user", "assistant"}:
            raise ValueError("role must be 'user' or 'assistant'")

        self.messages.append({
            "role": role,
            "content": content,
        })
        self.save()

    def save(self) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(
                self.messages,
                file,
                ensure_ascii=False,
                indent=2,
            )

    def clear(self) -> None:
        self.messages = []
        self.save()

    def get_messages(self) -> list[dict]:
        return list(self.messages)
