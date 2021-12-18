import traceback
from os import environ

from notion_client import Client

import others.others_notion_job as others_notion_job
from others.constants import (
    hds_gtd_database_id,
    kkanbu_gtd_database_id,
    personal_gtd_database_id,
    sh_teacher_gtd_database_id,
)


def notion_cleanup_SH_teacher():
    token = environ["NOTION_TOKEN_SH"]
    notion = Client(auth=token)

    page_results = others_notion_job.get_gtd_checked_pages(
        notion, sh_teacher_gtd_database_id
    )
    print(page_results)
    for page in page_results:
        page_id = page["id"]
        others_notion_job.update_gtd_page_complete(notion, page_id)


def notion_cleanup_SH_PERSONAL():
    token = environ["NOTION_TOKEN_SH_PERSONAL"]
    notion = Client(auth=token)

    page_results = others_notion_job.get_gtd_checked_pages(
        notion, personal_gtd_database_id
    )
    print(page_results)
    for page in page_results:
        page_id = page["id"]
        others_notion_job.update_gtd_page_complete(notion, page_id)


def notion_cleanup_HDS():
    token = environ["NOTION_TOKEN_HDS"]
    notion = Client(auth=token)

    page_results = others_notion_job.get_gtd_checked_pages(notion, hds_gtd_database_id)
    print(page_results)
    for page in page_results:
        page_id = page["id"]
        others_notion_job.update_gtd_page_complete(notion, page_id)


def notion_cleanup_coding_kkanbu():
    token = environ["NOTION_TOKEN_DEV"]
    notion = Client(auth=token)

    page_results = others_notion_job.get_gtd_checked_pages(
        notion, kkanbu_gtd_database_id
    )
    print(len(page_results))
    for page in page_results:
        page_id = page["id"]
        others_notion_job.update_gtd_page_complete(notion, page_id)


if __name__ == "__main__":
    notion_cleanup_SH_teacher()
