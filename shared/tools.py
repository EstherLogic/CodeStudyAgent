
from pathlib import Path

from shared.models import Task, Preference
from shared.storage import JsonStorage


DATA_DIR = Path(__file__).resolve().parent.parent / "data"

tasks_storage = JsonStorage(str(DATA_DIR / "tasks.json"))
preferences_storage = JsonStorage(str(DATA_DIR / "preferences.json"))


def list_tasks() -> list[dict]:
    """Return all saved study tasks."""
    return tasks_storage.load(default=[])


def add_task(title: str, description: str = "") -> dict:
    """Create and persist a new study task."""
    tasks = list_tasks()
    task = Task(title=title, description=description)
    tasks.append(task.to_dict())
    tasks_storage.save(tasks)
    return task.to_dict()


def complete_task(task_id: str) -> dict:
    """Mark a task as completed."""
    tasks = list_tasks()

    for task in tasks:
        if task["task_id"] == task_id:
            task["completed"] = True
            tasks_storage.save(tasks)
            return task

    return {"error": f"Task not found: {task_id}"}


def save_preference(key: str, value: str) -> dict:
    """Save or update a user preference."""
    preferences = preferences_storage.load(default={})
    preference = Preference(key=key, value=value)
    preferences[key] = preference.to_dict()
    preferences_storage.save(preferences)
    return preference.to_dict()


def get_preferences() -> dict:
    """Return all saved user preferences."""
    return preferences_storage.load(default={})
