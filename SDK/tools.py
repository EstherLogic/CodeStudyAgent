
from shared.tools import (
    add_task,
    list_tasks,
    complete_task,
    save_preference,
    get_preferences,
)


def add_task_tool(title: str, description: str = "") -> dict:
    """Create a study task."""
    return add_task(title=title, description=description)


def list_tasks_tool() -> list[dict]:
    """Return all saved study tasks."""
    return list_tasks()


def complete_task_tool(task_id: str) -> dict:
    """Mark a task as completed."""
    return complete_task(task_id=task_id)


def save_preference_tool(key: str, value: str) -> dict:
    """Save a user preference."""
    return save_preference(key=key, value=value)


def get_preferences_tool() -> dict:
    """Return saved user preferences."""
    return get_preferences()


def get_sdk_tools() -> list:
    """Return the tools exposed to the agent SDK."""
    return [
        add_task_tool,
        list_tasks_tool,
        complete_task_tool,
        save_preference_tool,
        get_preferences_tool,
    ]
