
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import tempfile
from pathlib import Path

from API.harness.loop import run_agent
from shared.storage import JsonStorage
import shared.tools as shared_tools


def make_response(content, stop_reason):
    """Create a fake model response for offline tests."""
    usage = SimpleNamespace(
        input_tokens=10,
        output_tokens=5,
        cache_read_input_tokens=0,
        cache_creation_input_tokens=0,
    )

    return SimpleNamespace(
        content=content,
        stop_reason=stop_reason,
        usage=usage,
    )


class FakeMessages:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if not self.responses:
            raise AssertionError("No fake responses left")
        return self.responses.pop(0)


class FakeClient:
    def __init__(self, responses):
        self.messages = FakeMessages(responses)


class TestAgentLoop(unittest.TestCase):
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

    def test_agent_returns_text_answer(self):
        response = make_response(
            [SimpleNamespace(type="text", text="Hello! How can I help?")],
            "end_turn",
        )
        client = FakeClient([response])

        result = run_agent(client, "Hello")

        self.assertEqual(result["answer"], "Hello! How can I help?")
        self.assertEqual(result["model_calls"], 1)
        self.assertEqual(result["tool_calls"], 0)

    def test_agent_executes_tool_and_continues(self):
        tool_call = SimpleNamespace(
            type="tool_use",
            id="tool-123",
            name="add_task",
            input={
                "title": "Practice JavaScript",
                "description": "Study classes",
            },
        )

        first_response = make_response([tool_call], "tool_use")
        second_response = make_response(
            [SimpleNamespace(type="text", text="Task added successfully.")],
            "end_turn",
        )

        client = FakeClient([first_response, second_response])
        result = run_agent(client, "Add a JavaScript task")

        self.assertEqual(result["answer"], "Task added successfully.")
        self.assertEqual(result["model_calls"], 2)
        self.assertEqual(result["tool_calls"], 1)

        tasks = shared_tools.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Practice JavaScript")

    def test_saved_task_survives_a_new_storage_instance(self):
        task = shared_tools.add_task("Learn Python")

        # Load the same file again, as a new process would.
        tasks_file = shared_tools.tasks_storage.file_path
        new_storage = JsonStorage(str(tasks_file))
        loaded_tasks = new_storage.load(default=[])

        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0]["task_id"], task["task_id"])


if __name__ == "__main__":
    unittest.main()
