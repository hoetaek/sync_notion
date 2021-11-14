import gsheet_func
import notion_job
import todoist_job
from notion_gtd import GTD
from todoist_task import Task
import json, os
from typing import List, Dict


def update_notion_stocks():
    stocks_from_sheet = list(set(gsheet_func.get_sheet_stocks()))
    stocks_from_db = notion_job.get_pages_from_stock_db()

    new_stocks = [i for i in stocks_from_sheet if i not in stocks_from_db]
    print(new_stocks)

    for stock in new_stocks:
        notion_job.create_stock_page(stock)


def sync_date_next_actions2todoist():
    page_results = notion_job.get_gtd_date_next_action_pages()
    gtd_date_next_action_pages = [GTD.from_notion(r) for r in page_results]
    print("closing todoist which is not in gtd")
    close_todoist_not_in_gtd(gtd_date_next_action_pages)
    print("syncing todoist labels with gtd reminders")
    sync_labels2meta_reminders(gtd_date_next_action_pages)
    for page in gtd_date_next_action_pages:
        task = Task.from_gtd(page)
        # if at todoist update the details
        if page.is_at_todoist():
            task.update()
        # if not at todoist make todoist task
        else:
            result = task.create()
            task_id = result["id"]
            page.task_id = task_id
            page.update()


def close_todoist_not_in_gtd(gtd_date_next_action_pages):
    date_next_action_tasks = [
        Task.from_todoist(task) for task in todoist_job.get_date_next_action_tasks()
    ]
    for task in date_next_action_tasks:
        if task not in gtd_date_next_action_pages:
            task.close()


def sync_labels2meta_reminders(gtd_date_next_action_pages: List[GTD]):
    meta_reminders_dict = notion_job.get_meta_reminders_dict()
    # name: {"page_id": page_id, "label_id": label_id, "color_id": color_id}
    meta_reminder_names = list(meta_reminders_dict.keys())
    # name

    gtd_reminders = [
        reminder
        for gtd_page in gtd_date_next_action_pages
        for reminder in gtd_page.reminder
        # {"name": name, "color_id": color_id}
    ]
    reminder_to_make_in_todoist = [
        reminder
        for reminder in gtd_reminders
        if reminder["name"] not in meta_reminder_names
    ]
    # {"name": name, "color_id": color_id}
    print("making meta labels")
    for reminder in [dict(t) for t in {tuple(d.items()) for d in reminder_to_make_in_todoist}]:
        # TODO give the right color for reminder
        label_id = todoist_job.create_label(reminder["name"], reminder["color_id"])[
            "id"
        ]
        notion_job.create_meta_reminders_page(
            reminder["name"], label_id, reminder["color_id"]
        )
    Task.force_update_meta_reminders_dics()

    print("deleting not used labels")
    gtd_reminder_names = [reminder["name"] for reminder in gtd_reminders]
    reminders_to_delete = [
        (reminder_info["page_id"], reminder_info["label_id"])
        for reminder_name, reminder_info in meta_reminders_dict.items()
        if reminder_name not in gtd_reminder_names
    ]
    for reminder_page_id, reminder_label_id in reminders_to_delete:
        notion_job.delete_meta_reminders_page(reminder_page_id)
        todoist_job.delete_label(reminder_label_id)


if __name__ == "__main__":
    sync_date_next_actions2todoist()
