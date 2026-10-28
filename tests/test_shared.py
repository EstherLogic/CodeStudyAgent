
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from shared.models import Task, Preference
from shared.storage import JsonStorage
import shared.tools as tools


class TestModels(unittest.TestCase):
    def test_task_gets_id_and_timestamp(self):
        task = Task(title="Learn JavaScript")
        self.assertTrue(task.task_id)
        self.assertTrue(task.created_at)
        self.assertFalse(task.completed)

    def test_preference_stores_key_and_value(self):
        preference = Preference("language", "JavaScript")
        self.assertEqual(preference.key, "language")
        self.assertEqual(preference.value, "JavaScript")
        self.assertTrue(preference.updated_at)


class TestJsonStorage(unittest.TestCase):
    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = JsonStorage(str(Path(temp_dir) / "data.json"))
            storage.save({"language": "JavaScript"})
            self.assertEqual(storage.load(), {"language": "JavaScript"})

    def test_load_missing_file_returns_default(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = JsonStorage(str(Path(temp_dir) / "missing.json"))
            self.assertEqual(storage.load(default=[]), [])

    def test_load_invalid_json_returns_default(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "invalid.json"
            path.write_text("{invalid json", encoding="utf-8")
            storage = JsonStorage(str(path))
            self.assertEqual(storage.load(default={}), {})


class TestSharedTools(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)

        self.tasks_path = base / "tasks.json"
        self.preferences_path = base / "preferences.json"

        self.tasks_patch = patch.object(
            tools, "tasks_storage",
            JsonStorage(str(self.tasks_path)),
        )
        self.preferences_patch = patch.object(
            tools, "preferences_storage",
            JsonStorage(str(self.preferences_path)),
        )

        self.tasks_patch.start()
        self.preferences_patch.start()
        self.addCleanup(self.tasks_patch.stop)
        self.addCleanup(self.preferences_patch.stop)
        self.addCleanup(self.temp_dir.cleanup)

    def test_add_and_list_task(self):
        created = tools.add_task("Learn JavaScript", "Practice classes")
        tasks = tools.list_tasks()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["task_id"], created["task_id"])
        self.assertEqual(tasks[0]["title"], "Learn JavaScript")

    def test_complete_task(self):
        created = tools.add_task("Practice Python")
        result = tools.complete_task(created["task_id"])

        self.assertTrue(result["completed"])
        self.assertTrue(tools.list_tasks()[0]["completed"])

    def test_complete_unknown_task_returns_error(self):
        result = tools.complete_task("unknown-id")
        self.assertIn("error", result)

    def test_save_and_retrieve_preference(self):
        tools.save_preference("language", "JavaScript")
        preferences = tools.get_preferences()

        self.assertEqual(preferences["language"]["value"], "JavaScript")


if __name__ == "__main__":
    unittest.main()
