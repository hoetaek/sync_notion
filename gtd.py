from abstract_action import AbstractAction
from notion_db import create_gtd_collect_page


class GTD(AbstractAction):
    def __init__(self, page_id, title, labels, date, task_id):
        super().__init__(self, page_id, title, labels, date, task_id)

    @classmethod
    def from_notion(cls, page_obj):
        title = page_obj["properties"]["이름"]["title"][0]["text"]["content"]
        state = page_obj["properties"]["상태"]["select"]["name"]
        reminder = [i["name"] for i in page_obj["properties"]["실행 환기"]["multi_select"]]
        date = None
        if page_obj["properties"]["일정"]["date"] != None:
            date = page_obj["properties"]["일정"]["date"]["start"]
        todoist_id = page_obj["properties"]["Todoist id"]["number"]
        return cls(title, state, reminder, date, todoist_id)

    @classmethod
    def from_task(cls, task):
        title = task.title
        todoist_id = task.id
        labels = task.label_ids
        date = task.end_date
        return cls(title, )


    def is_at_todoist(self):
        if self.todoist_id:
            return True
        return False

    def is_at_notion(self):
        return

    def create(self):
        # if no Notion page then create
        if not self.is_at_notion():
            return create_gtd_collect_page(self.title)