from abc import ABCMeta, abstractmethod
from typing import Dict, List


class Action(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(
        self, page_id, title, reminder, date, task_id, priority=4, checked=False
    ):
        self.page_id = page_id
        self.title = title
        self.reminder: List[Dict[str]] = reminder
        self.date = date
        self.task_id = task_id
        self.priority = priority
        self.checked = checked

    def __str__(self) -> str:
        return str(self.__dict__)

    def __eq__(self, o: object) -> bool:
        return self.page_id == o
