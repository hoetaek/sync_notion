from datetime import datetime
from os import environ

from notion_client import Client

from SH.constants import sh_gtd_database_id

token = environ["NOTION_TOKEN_SH"]
notion = Client(auth=token)


################ gtd ################
def get_sh_gtd_checked_pages():
    result = notion.databases.query(
        sh_gtd_database_id,
        filter={
            "and": [
                {
                    "or": [
                        {"property": "상태", "select": {"equals": "----수집함----"}},
                        {"property": "상태", "select": {"equals": "다음 행동"}},
                        {"property": "상태", "select": {"equals": "일정"}},
                    ]
                },
                {"property": "완료", "checkbox": {"equals": True}},
            ]
        },
    )
    return result["results"]


def update_gtd_page_complete(page_id):
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


if __name__ == "__main__":
    from pprint import pprint

    # result = notion.databases.retrieve(database_id= sh_gtd_database_id)
    pprint(get_sh_gtd_checked_pages())
