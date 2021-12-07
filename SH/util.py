import traceback

import SH.sh_notion_job as sh_notion_job


def notion_cleanup_SH():
    try:
        print("trying")
        update_checked_collection2done()
    except Exception:
        sh_notion_job.create_errorpage_in_gtd_collect(traceback.format_exc())


def update_checked_collection2done():
    page_results = sh_notion_job.get_sh_gtd_checked_pages()
    print(page_results)
    for page in page_results:
        page_id = page["id"]
        sh_notion_job.update_gtd_page_complete(page_id)


if __name__ == "__main__":
    notion_cleanup_SH()
