from gtd import GTD
from task import Task

class Converter:
    def __init__(self):
        pass

    def gtd_to_task(self, gtd:GTD):
        return Task.from_gtd(gtd)

    def task_to_gtd(self, task:Task):
        return GTD.from_task(task)