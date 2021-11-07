from abstract_action import Action
from notion_job import create_gtd_collect_page, get_gtd_date_next_action_pages, update_gtd_date_next_action_pages


class GTD(Action):
    def __init__(self, page_id, title, reminder, date, task_id):
        super().__init__(page_id, title, reminder, date, task_id)

    @classmethod
    def from_notion(cls, page_obj):
        page_id = page_obj["id"]
        title = page_obj["properties"]["이름"]["title"][0]["text"]["content"]
        reminder = [i["name"] for i in page_obj["properties"]["실행 환기"]["multi_select"]]
        date = None
        if page_obj["properties"]["일정"]["date"] != None:
            date = page_obj["properties"]["일정"]["date"]["start"]
        task_id = page_obj["properties"]["Todoist id"]["number"]
        return cls(page_id, title, reminder, date, task_id)

    @classmethod
    def from_todoist(cls, todoist):
        return cls(**todoist.__dict__)


    def is_at_todoist(self):
        if self.task_id:
            return True
        return False


    def create(self):
        # if no Notion page then create
        if not self.is_at_notion():
            return create_gtd_collect_page(self.title)

    def update(self):
        update_gtd_date_next_action_pages(self.page_id, self.task_id)


if __name__=="__main__":
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