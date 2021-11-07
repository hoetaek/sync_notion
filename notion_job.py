from notion_client import Client
from os import environ
from datetime import datetime
from pprint import pprint
from constants import gtd_database_id, stock_database_id, meta_reminders_database_id

token = environ["NOTION_TOKEN"]
notion = Client(auth=token)


def get_pages_from_stock_db():
    pages = notion.databases.query(stock_database_id)
    stock_names = [page["properties"]["종목명"]["title"][0]["text"]["content"] for page in pages["results"]]
    return stock_names


def create_stock_page(stock_name):
    notion.pages.create(
        parent= {
            'database_id': stock_database_id,
            },
        properties= {
            '종목명': {
                'title': [
                    {
                        'text': {
                        'content': stock_name,
                        },
                        }
                    ],
                },
            '보유 여부': {'checkbox': True},
            },
        )

def create_gtd_collect_page(title):
    page = notion.pages.create(
        parent= {
            'database_id': gtd_database_id,
            },
        properties= {
            '이름': {
                'title': [
                    {
                        'text': {
                        'content': title,
                        },
                        }
                    ],
                },
            '상태': {
                'select': {
                    'color': 'pink',
                    'name': '-----수집함-----'
                }
            },
            },
        )
    return page['id']


def get_gtd_date_next_action_pages():
    result = notion.databases.query(gtd_database_id, filter={
        "or": [{ 
            "property": "상태", 
            "select": {
            "equals": "일정"
            }},
           {
            "property": "상태",
            "select": {
                "equals": "다음 행동"
            }}
            ]
})
    return result["results"]

def update_gtd_date_next_action_pages(page_id, task_id):
    page = notion.pages.update(
        page_id = page_id,
        properties = {
        "Todoist id": {
            "number": task_id,
        },
        },
    )

def create_meta_reminders_page(reminder, label_id):
    page = notion.pages.create(
        parent= {
            'database_id': meta_reminders_database_id,
            },
        properties= {
            '실행환기': {
                'title': [
                    {
                        'text': {
                        'content': reminder,
                        },
                        }
                    ],
                },
            'id': {
                'number': label_id
            },
            },
        )
    return page['id']


def get_meta_reminders_dict():
    pages = notion.databases.query(meta_reminders_database_id)
    reminders_dict = dict()
    for page in pages["results"]:
        if page["properties"]["실행환기"]["title"]:
            reminders_dict[page["properties"]["실행환기"]["title"][0]["text"]["content"]] = page["properties"]["id"]["number"]
    return reminders_dict

if __name__=="__main__":
    pages = get_gtd_date_next_action_pages()
    pprint(pages)

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