
from API.harness.memory import AgentMemory
from shared.tools import list_tasks


def build_context() -> str:
    """Build a compact context from persistent memory and tasks."""
    memory = AgentMemory()
    preferences = memory.recall()
    tasks = list_tasks()

    lines = ["User context:"]

    if preferences:
        lines.append("Saved preferences:")
        for key, item in preferences.items():
            lines.append(f"- {key}: {item['value']}")
    else:
        lines.append("No saved preferences.")

    if tasks:
        lines.append("Study tasks:")
        for task in tasks:
            status = "completed" if task["completed"] else "pending"
            lines.append(f"- [{status}] {task['title']}")
    else:
        lines.append("No study tasks.")

    return "\n".join(lines)
