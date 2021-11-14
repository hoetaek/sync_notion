from notion_client import Client
from os import environ
from datetime import datetime
from pprint import pprint
from constants import gtd_database_id, stock_database_id, meta_reminders_database_id, incubating_database_id, color_dict

token = environ["NOTION_TOKEN"]
notion = Client(auth=token)

################ stock ################
def get_pages_from_stock_db():
    pages = notion.databases.query(stock_database_id)
    stock_names = [
        page["properties"]["종목명"]["title"][0]["text"]["content"]
        for page in pages["results"]
    ]
    return stock_names


def create_stock_page(stock_name):
    notion.pages.create(
        parent={
            "database_id": stock_database_id,
        },
        properties={
            "종목명": {
                "title": [
                    {
                        "text": {
                            "content": stock_name,
                        },
                    }
                ],
            },
            "보유 여부": {"checkbox": True},
        },
    )


################ gtd ################
def create_gtd_collect_page(title, date=None):
    property_data = {
            "이름": {
                "title": [
                    {
                        "text": {
                            "content": title,
                        },
                    }
                ],
            },
            "상태": {"select": {"color": "pink", "name": "-----수집함-----"}},

        }

    if date:
        if len(date) > 10:
            date = date + ".000+09:00"
        property_data["일정"] = {"date": {"start": date}}
    page = notion.pages.create(
        parent={
            "database_id": gtd_database_id,
        },
        properties=property_data,
    )
    return page["id"]


def get_gtd_date_next_action_pages():
    result = notion.databases.query(
        gtd_database_id,
        filter={
            "or": [
                {"property": "상태", "select": {"equals": "일정"}},
                {"property": "상태", "select": {"equals": "다음 행동"}},
            ]
        },
    )
    return result["results"]


def update_gtd_date_next_action_pages_todoist_id(page_id, task_id):
    notion.pages.update(
        page_id=page_id,
        properties={
            "Todoist id": {
                "number": task_id,
            },
        },
    )


def reopen_gtd_date_next_action_page(page_id):
    notion.pages.update(
        page_id=page_id,
        properties={
            "완료": {
                "checkbox": False,
            },
        },
    )


def update_gtd_date_next_action_pages_compete(page_id):
    notion.pages.update(
        page_id=page_id,
        properties={
            "상태": {
                "select": {"color": "brown", "name": "Done"},
            },
            "완료": {
                "checkbox": True,
            },
        },
    )

################ Incubating ################
def get_incubating_pages():
    result = notion.databases.query(incubating_database_id, filter={
        "and": [{ 
            "property": "상태", 
            "multi_select": {
            "contains": "티클러 파일"
            }},
           {
            "property": "검토",
            "date": {
                "equals": "다음 행동"
            }}
            ]
})
    return result["results"]

################ meta reminder ################
def create_meta_reminders_page(reminder, label_id, color_id):
    color = {v: k for k, v in color_dict.items()}[color_id]
    page = notion.pages.create(
        parent={
            "database_id": meta_reminders_database_id,
        },
        properties={
            "실행환기": {
                "title": [
                    {
                        "text": {
                            "content": reminder,
                        },
                    }
                ],
            },
            "id": {"number": label_id},
            "color": {
                "select": {
                "name": color,
            }
            }
        },
    )
    return page["id"]


def get_meta_reminders_dict():
    pages = notion.databases.query(meta_reminders_database_id)
    reminders_dict = dict()
    for page in pages["results"]:
        if page["properties"]["실행환기"]["title"]:
            select_value = page["properties"]["color"].get("select", None)
            color_id = color_dict[select_value["name"]] if select_value else None
            reminders_dict[
                page["properties"]["실행환기"]["title"][0]["text"]["content"]
            ] = {"page_id": page["id"], "label_id": page["properties"]["id"]["number"], "color_id": color_id}
    # name: {"page_id": page_id, "label_id": label_id, "color_id": color_id}
    return reminders_dict


def delete_meta_reminders_page(reminder_page_id):
    notion.pages.update(
        page_id=reminder_page_id,
        archived=True,
    )


if __name__ == "__main__":
    colors = ["gray", "brown", "red", "orange", "yellow", "green", "blue", "purple", "pink"]
    for color in colors:
        try:
            create_meta_reminders_page("test", 2332, color)
        except Exception as e:
            print(e)

# 다음 행동은 yellow
# 일정은 defaults

# date_pages = notion.databases.query(database_id, filter={
#         "property": "상태",
#         "select": {
#         "equals": "일정"
#         }})
# next_action_pages = notion.databases.query(database_id, filter={
#         "property": "상태",
#         "select": {
#         "equals": "다음 행동"
#         }})
