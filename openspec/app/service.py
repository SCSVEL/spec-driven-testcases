from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List


@dataclass
class Task:
	id: int
	title: str
	done: bool = False


class TaskService:
	def __init__(self) -> None:
		self._tasks: List[Task] = []
		self._next_id: int = 1

	def add_task(self, title: str) -> Dict:
		clean_title = (title or "").strip()
		if not clean_title:
			raise ValueError("Title is required")

		task = Task(id=self._next_id, title=clean_title, done=False)
		self._tasks.append(task)
		self._next_id += 1
		return asdict(task)

	def list_tasks(self) -> List[Dict]:
		return [asdict(task) for task in self._tasks]

	def complete_task(self, task_id: int) -> Dict:
		for task in self._tasks:
			if task.id == task_id:
				if task.done:
					raise ValueError("Task already completed")
				task.done = True
				return asdict(task)

		raise KeyError("Task not found")
