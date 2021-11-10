from abc import ABCMeta, abstractmethod


class Action(object, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, page_id, title, reminder, date, task_id, checked=False):
        self.page_id = page_id
        self.title = title
        self.reminder = reminder
        self.date = date
        self.task_id = task_id
        self.checked = checked


    def __str__(self) -> str:
        return str(self.__dict__)

    def __eq__(self, o: object) -> bool:
        return self.page_id == o
