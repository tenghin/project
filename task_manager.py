from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List


@dataclass
class Task:
    id: int
    title: str
    completed: bool = False


class TaskManager:
    def __init__(self, storage_path: str = "tasks.json") -> None:
        self.storage_path = Path(storage_path)
        self.tasks: List[Task] = []
        self._next_id = 1
        self.load()

    def load(self) -> None:
        if not self.storage_path.exists():
            return

        with self.storage_path.open("r", encoding="utf-8") as f:
            raw_tasks = json.load(f)

        self.tasks = [Task(**item) for item in raw_tasks]
        self._next_id = max((task.id for task in self.tasks), default=0) + 1

    def save(self) -> None:
        with self.storage_path.open("w", encoding="utf-8") as f:
            json.dump([asdict(task) for task in self.tasks], f, indent=2)

    def add_task(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty")

        task = Task(id=self._next_id, title=title)
        self._next_id += 1
        self.tasks.append(task)
        self.save()
        return task

    def list_tasks(self) -> List[Task]:
        return list(self.tasks)

    def complete_task(self, task_id: int) -> Task:
        task = self._find_task(task_id)
        task.completed = True
        self.save()
        return task

    def remove_task(self, task_id: int) -> Task:
        task = self._find_task(task_id)
        self.tasks.remove(task)
        self.save()
        return task

    def _find_task(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"Task with id {task_id} was not found")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple task management system")
    parser.add_argument("--storage", default="tasks.json", help="Path to tasks file")

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a task")
    add_parser.add_argument("title", help="Task title")

    subparsers.add_parser("list", help="List tasks")

    complete_parser = subparsers.add_parser("complete", help="Mark task completed")
    complete_parser.add_argument("id", type=int, help="Task id")

    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("id", type=int, help="Task id")

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    manager = TaskManager(storage_path=args.storage)

    try:
        if args.command == "add":
            task = manager.add_task(args.title)
            print(f"Added task #{task.id}: {task.title}")
        elif args.command == "list":
            for task in manager.list_tasks():
                status = "x" if task.completed else " "
                print(f"[{status}] {task.id}: {task.title}")
        elif args.command == "complete":
            task = manager.complete_task(args.id)
            print(f"Completed task #{task.id}: {task.title}")
        elif args.command == "remove":
            task = manager.remove_task(args.id)
            print(f"Removed task #{task.id}: {task.title}")
    except ValueError as exc:
        print(str(exc))
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
