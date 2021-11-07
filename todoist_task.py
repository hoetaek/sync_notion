from abstract_action import Action
from notion_job import get_meta_reminders_dict
from todoist_job import create_date_next_action_task, delete_task, update_date_next_action_task, close_task


class Task(Action):
    meta_reminders_dict = dict()

    def __init__(self, page_id, title, reminder, date, task_id):
        super(Task, self).__init__(page_id, title, reminder, date, task_id)

    @classmethod
    def from_todoist(cls, todoist_obj):
        page_id = todoist_obj["description"]
        title = todoist_obj["content"]
        if not Task.meta_reminders_dict:
            Task.meta_reminders_dict = get_meta_reminders_dict()
        notion_labels = {v: k for k, v in Task.meta_reminders_dict.items()}
        reminder = [notion_labels.get(i) for i in todoist_obj["label_ids"]]
        date = todoist_obj.get("due").get("datetime") if todoist_obj.get("due") != None else None
        task_id = todoist_obj["id"]
        return cls(page_id, title, reminder, date, task_id)

    @classmethod
    def from_gtd(cls, gtd):
        return cls(**gtd.__dict__)


    @classmethod
    def update_meta_reminders_dict(cls):
        Task.meta_reminders_dict = get_meta_reminders_dict()

    def create(self):
        if not Task.meta_reminders_dict:
            Task.meta_reminders_dict = get_meta_reminders_dict()
        print("reminder", self.reminder)
        print("-" * 10)
        print("meta_reminders_dict", Task.meta_reminders_dict)
        print("-" * 10)
        label_ids = [Task.meta_reminders_dict[k] for k in self.reminder]
        print(label_ids)
        return create_date_next_action_task(self.page_id, self.title, label_ids, self.date)

    def update(self):
        if not Task.meta_reminders_dict:
            Task.meta_reminders_dict = get_meta_reminders_dict()
        label_ids = [Task.meta_reminders_dict[k] for k in self.reminder]
        update_date_next_action_task(self.task_id, self.title, label_ids, self.date)

    def close(self):
        close_task(self.task_id)

    def delete(self):
        delete_task(self.task_id)