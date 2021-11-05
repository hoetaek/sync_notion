from notion_client import Client
from os import environ
from datetime import datetime
from pprint import pprint
from gtd import GTD

token = environ["NOTION_TOKEN"]
notion = Client(auth=token)


def get_pages_from_stock_db():
    database_id = "a7ba96b55c5f42aebacbe8a1818c3c88"
    pages = notion.databases.query(database_id)
    stock_names = [page["properties"]["종목명"]["title"][0]["text"]["content"] for page in pages["results"]]
    return stock_names


def create_stock_page(stock_name):
    database_id = "a7ba96b55c5f42aebacbe8a1818c3c88"
    notion.pages.create(
        parent= {
            'database_id': database_id,
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
    database_id = "c596f2ffc3e04190bf72a763e0503b06"
    page = notion.pages.create(
        parent= {
            'database_id': database_id,
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
    database_id = "c596f2ffc3e04190bf72a763e0503b06"
    pages = notion.databases.query(database_id, filter={
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
    gtd_pages = [GTD.from_notion(page) for page in pages["results"]]
    return gtd_pages


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