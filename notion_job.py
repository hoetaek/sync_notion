from datetime import datetime
from os import environ

from notion_client import Client

from constants import (
    color_dict,
    gtd_database_id,
    incubating_database_id,
    meta_reminders_database_id,
    stock_database_id,
)

token = environ["NOTION_TOKEN"]
notion = Client(auth=token)


################ general ################
def get_block_children(blockId):
    result = notion.blocks.children.list({
    block_id=blockId,
    page_size=50,
  })
    return result["results"]
    

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
def create_gtd_collect_page(title, date=None, property_extra_data=None):
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


def create_errorpage_in_gtd_collect(errormessage):
    property_data = {
        "이름": {
            "title": [
                {
                    "text": {
                        "content": "error at "
                        + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    },
                }
            ],
        },
        "상태": {"select": {"color": "pink", "name": "-----수집함-----"}},
    }

    page = notion.pages.create(
        parent={
            "database_id": gtd_database_id,
        },
        properties=property_data,
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "text": [
                        {
                            "type": "text",
                            "text": {
                                "content": errormessage,
                            },
                        },
                    ],
                },
            },
        ],
    )
    return page["id"]


def get_gtd_checked_collection_pages():
    result = notion.databases.query(
        gtd_database_id,
        filter={
            "and": [
                {"property": "상태", "select": {"equals": "-----수집함-----"}},
                {"property": "완료", "checkbox": {"equals": True}},
            ]
        },
    )
    return result["results"]


def get_gtd_email_collection_page(email_title: str):
    result = notion.databases.query(
        gtd_database_id,
        filter={
            "and": [
                {"property": "상태", "select": {"equals": "-----수집함-----"}},
                {"property": "이름", "text": {"equals": email_title}},
            ]
        },
    )
    return result["results"]


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


def paragraph_block_format(content):
    return {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "text": [
                        {
                            "type": "text",
                            "text": {
                                "content": content,
                            },
                        },
                    ],
                },
            }

def update_gtd_email_collection_page(page_id, file_url, contents):
    block_children = [
        {
                "object": "block",
                "type": "embed",
                "embed": {
                    "url": file_url,
                },
            },
    ]

    for content in list(filter(lambda x: x != "", contents.split("\n"))):
        block_children.append(paragraph_block_format(content))

    notion.blocks.children.append(
        block_id=page_id,
        children=block_children
    )


################ Incubating ################
def get_incubating_pages():
    result = notion.databases.query(
        incubating_database_id,
        filter={
            "and": [
                {"property": "상태", "select": {"equals": "티클러 파일"}},
                {
                    "property": "검토",
                    "date": {"on_or_before": datetime.now().isoformat()},
                },
            ]
        },
    )
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
            },
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
            ] = {
                "page_id": page["id"],
                "label_id": page["properties"]["id"]["number"],
                "color_id": color_id,
            }
    # name: {"page_id": page_id, "label_id": label_id, "color_id": color_id}
    return reminders_dict


def delete_meta_reminders_page(reminder_page_id):
    notion.pages.update(
        page_id=reminder_page_id,
        archived=True,
    )


if __name__ == "__main__":
    from pprint import pprint

    pprint(get_gtd_checked_collection_pages())
