from abc import ABCMeta, abstractmethod


class AbstractAction(ABCMeta):
    @abstractmethod
    def __init__(self, page_id, title, labels, date, task_id):
        self.page_id = page_id
        self.title = title
        self.labels = labels
        self.date = date
        self.task_id = task_id