import traceback

import notion_job


def notion_cleanup_SH():
    try:
        update_checked_collection2done()
    except Exception:
        notion_job.create_errorpage_in_gtd_collect(traceback.format_exc())


def update_checked_collection2done():
    page_results = notion_job.get_gtd_checked_collection_pages()
    for page in page_results:
        page_id = page["id"]
        notion_job.update_gtd_page_complete(page_id)


if __name__ == "__main__":
    update_checked_collection2done()
