from datetime import datetime


################ gtd ################
def get_gtd_checked_pages(notion, database_id):
    filters = {
        "and": [
            {"property": "상태", "select": {"does_not_equal": "완료"}},
            {"property": "완료", "checkbox": {"equals": True}},
        ]
    }

    result = notion.databases.query(
        database_id,
        filter=filters,
    )
    return result["results"]


def update_gtd_page_complete(notion, page_id):
    notion.pages.update(
        page_id=page_id,
        properties={
            "상태": {
                "select": {"color": "brown", "name": "완료"},
            },
            "완료": {
                "checkbox": True,
            },
        },
    )


if __name__ == "__main__":
    from pprint import pprint

    # result = notion.databases.retrieve(database_id= sh_teacher_gtd_database_id)
    pprint(get_gtd_checked_pages())
