
from shared.tools import (
    add_task,
    list_tasks,
    complete_task,
    save_preference,
    get_preferences,
)


def execute_tool(name: str, arguments: dict) -> dict | list | str:
    """Execute a tool by its name and return the result."""

    if name == "add_task":
        return add_task(
            title=arguments["title"],
            description=arguments.get("description", ""),
        )

    if name == "list_tasks":
        return list_tasks()

    if name == "complete_task":
        return complete_task(task_id=arguments["task_id"])

    if name == "save_preference":
        return save_preference(
            key=arguments["key"],
            value=arguments["value"],
        )

    if name == "get_preferences":
        return get_preferences()

    return {"error": f"Unknown tool: {name}"}


def get_tool_definitions() -> list[dict]:
    """Return tool definitions for the Anthropic Messages API."""
    return [
        {
            "name": "add_task",
            "description": "Create a study task.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["title"],
            },
        },
        {
            "name": "list_tasks",
            "description": "List all study tasks.",
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
        {
            "name": "complete_task",
            "description": "Mark a study task as completed.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                },
                "required": ["task_id"],
            },
        },
        {
            "name": "save_preference",
            "description": "Save a user preference.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "value": {"type": "string"},
                },
                "required": ["key", "value"],
            },
        },
        {
            "name": "get_preferences",
            "description": "Get all saved user preferences.",
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    ]
