from datetime import datetime

from abstract_action import Action
from constants import color_dict
from notion_job import (
    create_gtd_collect_page,
    get_gtd_date_next_action_pages,
    get_meta_reminders_dict,
    update_gtd_date_next_action_pages_todoist_id,
    update_gtd_page_complete,
    delete_page,
)


class GTD(Action):
    def __init__(
        self, page_id, title, reminder, date, task_id, priority=4, checked=False
    ):
        super().__init__(page_id, title, reminder, date, task_id, priority, checked)

    @classmethod
    def from_notion(cls, page_obj):
        page_id = page_obj["id"]
        title = page_obj["properties"]["이름"]["title"][0]["text"]["content"]
        reminder = [
            {"name": i["name"], "color_id": color_dict[i["color"]]}
            for i in page_obj["properties"]["실행 환기"]["multi_select"]
        ]
        date = None
        print(page_obj["properties"]["상태"]["select"])
        if (
            page_obj["properties"]["일정"]["date"] != None
            and page_obj["properties"]["상태"]["select"]["name"] == "일정"
        ):
            date = page_obj["properties"]["일정"]["date"]["start"]
        task_id = page_obj["properties"]["Todoist id"]["number"]
        priority = 4
        if page_obj["properties"]["우선순위"]["rollup"]["array"]:
            priority = int(
                page_obj["properties"]["우선순위"]["rollup"]["array"][0]["formula"][
                    "string"
                ][-1]
            )
        checked = page_obj["properties"]["완료"]["checkbox"]
        return cls(page_id, title, reminder, date, task_id, priority, checked)

    @classmethod
    def from_todoist(cls, todoist):
        return cls(**todoist.__dict__)

    @classmethod
    def from_webhook(cls, item):
        task_id = item["event_data"]["id"]
        title = item["event_data"]["content"]
        reminder_dict = {v["label_id"]: k for k, v in get_meta_reminders_dict().items()}
        reminder_id = item["event_data"].get("labels", None)
        reminder = reminder_dict[reminder_id[0]] if reminder_id else None
        due_data = item["event_data"].get("due")
        date = due_data["date"] if due_data != None else None
        date = date if date != datetime.today().strftime("%Y-%m-%d") else None
        page_id = item["event_data"]["description"]
        return cls(page_id, title, reminder, date, task_id)

    def is_at_todoist(self):
        if self.task_id:
            return True
        return False

    def create(self, children=None):
        data = None
        if self.reminder:
            data = {"실행 환기": {"multi_select": [{"name": self.reminder}]}}
        return create_gtd_collect_page(
            self.title, self.date, property_extra_data=data, children=children
        )

    def update(self):
        update_gtd_date_next_action_pages_todoist_id(self.page_id, self.task_id)

    def complete(self):
        if self.page_id:
            update_gtd_page_complete(self.page_id)

    def delete(self):
        delete_page(self.page_id)


if __name__ == "__main__":
    result = get_gtd_date_next_action_pages()
    from pprint import pprint

    for page_obj in result:
        page_id = page_obj["id"]
        title = page_obj["properties"]["이름"]["title"][0]["text"]["content"]
        reminder = [i["name"] for i in page_obj["properties"]["실행 환기"]["multi_select"]]
        date = None
        if page_obj["properties"]["일정"]["date"] != None:
            date = page_obj["properties"]["일정"]["date"]["start"]
        todoist_id = page_obj["properties"]["Todoist id"]["number"]
        gtd = GTD(page_id, title, reminder, date, todoist_id)
        print(gtd)

    # pprint(date_next_action_pages)
