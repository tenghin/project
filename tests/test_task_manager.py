import tempfile
import unittest
from pathlib import Path

from task_manager import TaskManager


class TaskManagerTests(unittest.TestCase):
    def test_add_and_list_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            storage = Path(tmp) / "tasks.json"
            manager = TaskManager(str(storage))

            created = manager.add_task("Write tests")
            tasks = manager.list_tasks()

            self.assertEqual(created.id, 1)
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0].title, "Write tests")
            self.assertFalse(tasks[0].completed)

    def test_complete_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            storage = Path(tmp) / "tasks.json"
            manager = TaskManager(str(storage))
            task = manager.add_task("Ship feature")

            completed = manager.complete_task(task.id)

            self.assertTrue(completed.completed)

    def test_remove_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            storage = Path(tmp) / "tasks.json"
            manager = TaskManager(str(storage))
            task = manager.add_task("Unused")

            removed = manager.remove_task(task.id)

            self.assertEqual(removed.id, task.id)
            self.assertEqual(manager.list_tasks(), [])

    def test_persists_tasks_between_instances(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            storage = Path(tmp) / "tasks.json"
            manager = TaskManager(str(storage))
            manager.add_task("Persist me")

            reloaded = TaskManager(str(storage))

            self.assertEqual(len(reloaded.list_tasks()), 1)
            self.assertEqual(reloaded.list_tasks()[0].title, "Persist me")


if __name__ == "__main__":
    unittest.main()
