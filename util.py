import time
import traceback
from datetime import datetime
from typing import List

import notion_job
import todoist_job
from constants import (
    inbox_project_id,
    email_project_id,
    date_next_action_project_id,
    cleanup_task_id,
    bus_time_task_id,
)
from notion_gtd import GTD
from report_job import crawl_fin_reports
from todoist_task import Task
from bus_arrival import get_bus_arrival_time


def handle_webhook_task(item):
    try:
        gtd = GTD.from_webhook(item)
        if item["event_name"] == "item:completed":
            if item["event_data"]["description"]:
                if item["event_data"]["project_id"] == date_next_action_project_id:
                    gtd.complete()
                elif item["event_data"]["project_id"] == email_project_id:
                    gtd.delete()
            elif item["event_data"]["id"] == cleanup_task_id:
                notion2todoist_and_notion_cleanup()
            elif item["event_data"]["id"] == bus_time_task_id:
                arrival_time = get_bus_arrival_time()
                todoist_job.reopen_task(bus_time_task_id)
                todoist_job.update_task(
                    bus_time_task_id, {"content": arrival_time})
        elif item[
            "event_name"
        ] == "item:added" and not notion_job.search_collection_page(gtd.title):
            if item["event_data"]["project_id"] == email_project_id:
                pass
                # gtd.reminder = "이메일"
                # task_url = "https://todoist.com/showTask?id=" + str(
                #     item["event_data"]["id"]
                # )
                # children = (
                #     {
                #         "object": "block",
                #         "type": "paragraph",
                #         "paragraph": {
                #             "rich_text": [
                #                 {
                #                     "type": "text",
                #                     "text": {
                #                         "content": "todoist 보러 가기",
                #                         "link": {
                #                             "url": task_url,
                #                         },
                #                     },
                #                 },~
                #             ],
                #         },
                #     },
                # )
                # task_id = item["event_data"]["id"]
                # page_id = gtd.create(children)
                # todoist_job.update_task(task_id, {"description": page_id})
            elif item["event_data"]["project_id"] == inbox_project_id:
                # gtd.create()
                # task = Task.from_gtd(gtd)
                # task.delete()
                pass
    except Exception:
        notion_job.create_errorpage_in_gtd_collect(traceback.format_exc())


def reopen_assistant():
    todoist_job.reopen_task(cleanup_task_id)
    todoist_job.reopen_task(bus_time_task_id)


def notion2todoist_and_notion_cleanup():
    try:
        send_tickler2collection()
        send_today_next_actions2collection()
        update_checked_collection2done()
        sync_date_next_actions2todoist()
        reopen_assistant()
    except Exception:
        notion_job.create_errorpage_in_gtd_collect(traceback.format_exc())


def work_on_fin_reports():
    reports = crawl_fin_reports()
    db_urls = get_db_reports()

    for report in reversed(reports):
        link = report["link"]
        if link not in db_urls:
            page_id = notion_job.create_report_page(
                report["title"],
                report["catalog"],
                report["date"],
                report["link"],
                report["brokerage"],
                report["file_url"],
            )
            notion_job.update_fin_report_content(
                page_id, report["content"], report["file_url"]
            )


def get_db_reports():
    result = notion_job.get_db_report_pages()
    db_urls = [
        report["properties"]["링크"]["url"]
        for report in result
        if report["properties"]["링크"]["url"]
    ]
    return db_urls


def send_inbox2collection():
    inbox_tasks = [Task.from_todoist(task)
                   for task in todoist_job.get_inbox_tasks()]
    for task in inbox_tasks:
        gtd = GTD.from_todoist(task)
        gtd.create()


def send_tickler2collection():
    page_results = notion_job.get_tickler_pages()
    for page in page_results:
        page_id = page["id"]
        notion_job.update_gtd_page2collection(page_id)


def send_today_next_actions2collection():
    page_results = notion_job.get_today_next_action_pages()
    for page in page_results:
        page_id = page["id"]
        notion_job.update_gtd_page2collection(page_id)


def update_checked_collection2done():
    page_results = notion_job.get_gtd_checked_collection_pages()
    for page in page_results:
        page_id = page["id"]
        notion_job.update_gtd_page_complete(page_id)


def sync_date_next_actions2todoist():
    print("getting gtd date next action pages")
    page_results = notion_job.get_gtd_date_next_action_pages()
    gtd_date_next_action_pages = [
        GTD.from_notion(r) for r in page_results if r["properties"]["이름"]["title"]
    ]
    print("getting gtd unchecked collection pages")
    page_results = notion_job.get_gtd_unchecked_collection_pages()
    gtd_collection_pages = [
        GTD.from_notion(r) for r in page_results if r["properties"]["이름"]["title"]
    ]
    print("getting todoist date next action tasks")
    date_next_action_tasks = [
        Task.from_todoist(task) for task in todoist_job.get_date_next_action_tasks() if task["description"]
    ]
    print("closing todoist which is not in gtd")
    close_todoist_not_in_gtd(
        date_next_action_tasks, gtd_date_next_action_pages + gtd_collection_pages
    )
    print("syncing todoist labels with gtd reminders")
    sync_labels2meta_reminders(gtd_date_next_action_pages)

    # date_next_action_task_titles = [task.title for task in date_next_action_tasks]
    # date_next_action_task_dates = [task.date for task in date_next_action_tasks]
    for page in gtd_date_next_action_pages:
        task = Task.from_gtd(page)
        task_date = (
            datetime.strptime(task.date, "%Y-%m-%dT%H:%M:%S.%f+09:00")
            if task.date != None and len(task.date) > 10
            else task.date
        )
        task_from_todoist = next(
            (x for x in date_next_action_tasks if x == task), None)
        if task_from_todoist:
            if task_from_todoist.date != None:
                if len(task_from_todoist.date) == 20:
                    task_from_todoist_date = datetime.strptime(
                        task_from_todoist.date, "%Y-%m-%dT%H:%M:%SZ"
                    )
                elif len(task_from_todoist.date) == 19:
                    task_from_todoist_date = datetime.strptime(
                        task_from_todoist.date, "%Y-%m-%dT%H:%M:%S"
                    )
                else:
                    task_from_todoist_date = task_from_todoist.date
            else:
                task_from_todoist_date = task_from_todoist.date

        # if not at todoist make todoist task
        if not task_from_todoist:
            print(task)
            result = task.create()
            task_id = result["id"]
            page.task_id = task_id
            page.update()
        # if at todoist and detail changes update the details
        elif (
            task.title != task_from_todoist.title
            or task_date != task_from_todoist_date
            or [
                reminder
                for reminder in task.reminder
                if reminder not in task_from_todoist.reminder
            ]
            or task.priority != task_from_todoist.priority
        ):
            print(
                task.title != task_from_todoist.title,
                task_date != task_from_todoist_date,
                task.reminder != task_from_todoist.reminder,
                task.priority != task_from_todoist.priority,
            )
            print(task.priority, task_from_todoist.priority)
            print(task.reminder, task_from_todoist.reminder)
            print("updating", task)
            print("*" * 20)
            task.update()
        else:
            print("task doesn't need update")


def close_todoist_not_in_gtd(date_next_action_tasks, gtd_date_next_action_pages):
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
    for reminder in [
        dict(t) for t in {tuple(d.items()) for d in reminder_to_make_in_todoist}
    ]:
        print(reminder)
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
        notion_job.delete_page(reminder_page_id)
        todoist_job.delete_label(reminder_label_id)


if __name__ == "__main__":
    # send_tickler2collection()
    # send_inbox2collection()
    sync_date_next_actions2todoist()
