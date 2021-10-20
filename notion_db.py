from notion_client import Client
from os import environ
from datetime import datetime
from pprint import pprint

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

def create_action_page(title, endDate):
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
                    'name': 'To Do'
                }
            },
            '마감': {
                    'date': {
                        'start': endDate if endDate else datetime.today().strftime('%Y-%m-%d'),
                    }
            }
            },
        )
    return page['id']

if __name__=="__main__":
    print(create_action_page("테스트", "2022-01-31"))
