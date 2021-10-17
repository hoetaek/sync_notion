from notion_client import Client
from os import environ

token = environ["NOTION_TOKEN"]

notion = Client(auth=token)
database_id = "a7ba96b55c5f42aebacbe8a1818c3c88"



# page_id = "b2bac9a22a854958a67bdaab7fff5c13"
# page = notion.pages.retrieve(page_id="5efad401-0016-4090-a097-de0c3dc6efa8")
# pprint(page)

def get_pages_from_stock_db(database_id=database_id):
    pages = notion.databases.query(database_id)
    # for page in pages["results"]:
    #     pprint(page["properties"]["종목명"]["title"][0]["text"]["content"])

    stock_names = [page["properties"]["종목명"]["title"][0]["text"]["content"] for page in pages["results"]]
    return stock_names


def create_page(stock_name, database_id=database_id):
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