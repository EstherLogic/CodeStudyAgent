
from pathlib import Path

from API.harness.context import build_context
from API.harness.history import ConversationHistory
from SDK.tools import (
    add_task_tool,
    list_tasks_tool,
    complete_task_tool,
    save_preference_tool,
    get_preferences_tool,
)


class CodeStudySDKAgent:
    """Offline-testable study agent with persistent conversation history."""

    def __init__(self, history_path: str = "data/sdk_history.json"):
        self.history = ConversationHistory(history_path)
        self.tools = {
            "add_task": add_task_tool,
            "list_tasks": list_tasks_tool,
            "complete_task": complete_task_tool,
            "save_preference": save_preference_tool,
            "get_preferences": get_preferences_tool,
        }

    def run_tool(self, name: str, arguments: dict | None = None):
        """Run one of the registered tools."""
        if name not in self.tools:
            return {"error": f"Unknown tool: {name}"}

        arguments = arguments or {}

        try:
            return self.tools[name](**arguments)
        except (TypeError, KeyError) as error:
            return {"error": f"Invalid arguments for {name}: {error}"}

    def chat_offline(self, user_message: str) -> dict:
        """Provide a simple offline response for testing persistence."""
        self.history.add_message("user", user_message)

        context = build_context()
        answer = (
            "Offline mode: I received your message.\n\n"
            f"{context}\n\n"
            "No real language model was called."
        )

        self.history.add_message("assistant", answer)

        return {
            "answer": answer,
            "model_calls": 0,
            "tool_calls": 0,
            "mode": "offline",
        }

    def get_history(self) -> list[dict]:
        return self.history.get_messages()
