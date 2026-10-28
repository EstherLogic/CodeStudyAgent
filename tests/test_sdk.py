
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from SDK.agent import CodeStudySDKAgent
from shared.storage import JsonStorage
import shared.tools as shared_tools


class TestSDKAgent(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)

        self.tasks_patch = patch.object(
            shared_tools,
            "tasks_storage",
            JsonStorage(str(base / "tasks.json")),
        )
        self.preferences_patch = patch.object(
            shared_tools,
            "preferences_storage",
            JsonStorage(str(base / "preferences.json")),
        )

        self.tasks_patch.start()
        self.preferences_patch.start()

        self.addCleanup(self.tasks_patch.stop)
        self.addCleanup(self.preferences_patch.stop)
        self.addCleanup(self.temp_dir.cleanup)

        self.history_path = str(base / "history.json")
        self.agent = CodeStudySDKAgent(self.history_path)

    def test_offline_chat_returns_answer_without_model_calls(self):
        result = self.agent.chat_offline("Help me study JavaScript")

        self.assertIn("Offline mode", result["answer"])
        self.assertEqual(result["model_calls"], 0)
        self.assertEqual(result["mode"], "offline")

    def test_chat_history_is_saved(self):
        self.agent.chat_offline("First message")

        # Create a new agent that loads the same history file.
        new_agent = CodeStudySDKAgent(self.history_path)
        history = new_agent.get_history()

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["content"], "First message")
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[1]["role"], "assistant")

    def test_run_tool_adds_task(self):
        result = self.agent.run_tool(
            "add_task",
            {
                "title": "Practice Python",
                "description": "Write unit tests",
            },
        )

        self.assertEqual(result["title"], "Practice Python")
        self.assertEqual(len(shared_tools.list_tasks()), 1)

    def test_unknown_tool_returns_error(self):
        result = self.agent.run_tool("unknown_tool")

        self.assertIn("error", result)

    def test_invalid_tool_arguments_return_error(self):
        result = self.agent.run_tool("add_task", {})

        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
