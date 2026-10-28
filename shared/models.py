
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional
import uuid


@dataclass
class Task:
    title: str
    description: str = ""
    completed: bool = False
    task_id: str = ""
    created_at: str = ""

    def __post_init__(self):
        if not self.task_id:
            self.task_id = str(uuid.uuid4())

        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(**data)


@dataclass
class Preference:
    key: str
    value: str
    updated_at: str = ""

    def __post_init__(self):
        if not self.updated_at:
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Preference":
        return cls(**data)
