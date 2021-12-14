from datetime import datetime


################ gtd ################
def get_gtd_checked_pages(notion, database_id, checkbox_name="완료"):
    result = notion.databases.query(
        database_id,
        filter={
            "and": [
                {
                    "or": [
                        {"property": "상태", "select": {"equals": "----수집함----"}},
                        {"property": "상태", "select": {"equals": "다음 행동"}},
                        {"property": "상태", "select": {"equals": "일정"}},
                    ]
                },
                {"property": checkbox_name, "checkbox": {"equals": True}},
            ]
        },
    )
    return result["results"]


def update_gtd_page_complete(notion, page_id, checkbox_name="완료", complete_name="Done"):
    notion.pages.update(
        page_id=page_id,
        properties={
            "상태": {
                "select": {"color": "brown", "name": complete_name},
            },
            checkbox_name: {
                "checkbox": True,
            },
        },
    )


if __name__ == "__main__":
    from pprint import pprint

    # result = notion.databases.retrieve(database_id= sh_teacher_gtd_database_id)
    pprint(get_gtd_checked_pages())
