from abstract_action import Action
from notion_job import get_meta_reminders_dict, reopen_gtd_date_next_action_page
from todoist_job import (
    close_task,
    create_date_next_action_task,
    delete_task,
    reopen_task,
    update_date_next_action_task,
)


class Task(Action):
    meta_reminders_dict = dict()

    def __init__(
        self, page_id, title, reminder, date, task_id, priority=4, checked=False
    ):
        super(Task, self).__init__(
            page_id, title, reminder, date, task_id, priority, checked
        )

    @classmethod
    def from_todoist(cls, todoist_obj):
        page_id = todoist_obj["description"]
        title = todoist_obj["content"]
        Task.update_meta_reminders_dict()
        notion_labels_by_id = {
            v["label_id"]: {"color": v["color_id"], "name": k}
            for k, v in Task.meta_reminders_dict.items()
        }
        reminder = [
            {
                "name": notion_labels_by_id.get(label_id).get("name"),
                "color_id": notion_labels_by_id.get(label_id).get("color"),
            }
            for label_id in todoist_obj["label_ids"]
        ]
        if todoist_obj.get("due") != None:
            if todoist_obj.get("due").get("datetime") != None:
                date = todoist_obj.get("due").get("datetime")
            else:
                date = todoist_obj.get("due").get("date")
        else:
            date = None
        priority = 5 - todoist_obj["priority"]
        task_id = todoist_obj["id"]
        return cls(page_id, title, reminder, date, task_id, priority)

    @classmethod
    def from_gtd(cls, gtd):
        return cls(**gtd.__dict__)

    @classmethod
    def update_meta_reminders_dict(cls):
        if not Task.meta_reminders_dict:
            Task.meta_reminders_dict = {
                k: {"label_id": v["label_id"], "color_id": v["color_id"]}
                for k, v in get_meta_reminders_dict().items()
            }

    @classmethod
    def force_update_meta_reminders_dics(cls):
        Task.meta_reminders_dict = {
            k: {"label_id": v["label_id"], "color_id": v["color_id"]}
            for k, v in get_meta_reminders_dict().items()
        }

    def create(self):
        Task.update_meta_reminders_dict()
        label_ids = [
            Task.meta_reminders_dict[k["name"]]["label_id"] for k in self.reminder
        ]
        print(label_ids)
        return create_date_next_action_task(
            self.page_id, self.title, label_ids, self.date, self.priority
        )

    def update(self):
        Task.update_meta_reminders_dict()
        label_ids = [
            Task.meta_reminders_dict[k["name"]]["label_id"] for k in self.reminder
        ]
        update_date_next_action_task(
            self.task_id, self.title, label_ids, self.date, self.priority
        )
        # if self.checked == True:
        #     print("unchecked")
        #     reopen_task(self.task_id)
        #     reopen_gtd_date_next_action_page(self.page_id)

    def close(self):
        close_task(self.task_id)

    def delete(self):
        delete_task(self.task_id)
