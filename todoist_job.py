import json
import uuid
from os import environ

import requests

from constants import date_next_action_project_id, inbox_project_id

token = environ["TODOIST_TOKEN"]


def get_all_projects():
    result = requests.get(
        "https://api.todoist.com/rest/v1/projects",
        headers={"Authorization": "Bearer " + token},
    ).json()
    return result


def get_inbox_tasks():
    result = requests.get(
        "https://api.todoist.com/rest/v1/tasks",
        params={"project_id": inbox_project_id},
        headers={"Authorization": "Bearer " + token},
    ).json()
    return result


def get_date_next_action_tasks():
    result = requests.get(
        "https://api.todoist.com/rest/v1/tasks",
        params={"project_id": date_next_action_project_id},
        headers={"Authorization": "Bearer " + token},
    ).json()
    return result


def create_date_next_action_task(page_id, title, label_ids, date):
    task_data = {
        "content": title,
        "project_id": date_next_action_project_id,
        "description": page_id,
        "label_ids": label_ids,
    }
    if date and len(date) == 10:
        task_data["due_date"] = date
    else:
        task_data["due_datetime"] = date
    result = requests.post(
        "https://api.todoist.com/rest/v1/tasks",
        data=json.dumps(task_data),
        headers={
            "Content-Type": "application/json",
            "X-Request-Id": str(uuid.uuid4()),
            "Authorization": "Bearer " + token,
        },
    ).json()
    return result


def update_date_next_action_task(task_id, title, label_ids, date):
    task_data = {
        "content": title,
        "label_ids": label_ids,
    }
    if date and len(date) == 10:
        task_data["due_date"] = date
    else:
        task_data["due_datetime"] = date
    requests.post(
        "https://api.todoist.com/rest/v1/tasks/" + str(task_id),
        data=json.dumps(task_data),
        headers={
            "Content-Type": "application/json",
            "X-Request-Id": str(uuid.uuid4()),
            "Authorization": "Bearer " + token,
        },
    )


def delete_task(task_id):
    requests.delete(
        f"https://api.todoist.com/rest/v1/tasks/{task_id}",
        headers={"Authorization": "Bearer " + token},
    )


def close_task(task_id):
    requests.post(
        f"https://api.todoist.com/rest/v1/tasks/{task_id}/close",
        headers={"Authorization": "Bearer " + token},
    )


def reopen_task(task_id):
    requests.post(
        f"https://api.todoist.com/rest/v1/tasks/{task_id}/reopen",
        headers={"Authorization": "Bearer " + token},
    )


def get_all_labels():
    labels = requests.get(
        "https://api.todoist.com/rest/v1/labels",
        headers={"Authorization": "Bearer " + token},
    ).json()
    return labels


def create_label(label_name, color_id):
    result = requests.post(
        "https://api.todoist.com/rest/v1/labels",
        data=json.dumps({"name": label_name, "color": color_id}),
        headers={
            "Content-Type": "application/json",
            "X-Request-Id": str(uuid.uuid4()),
            "Authorization": "Bearer " + token,
        },
    ).json()
    return result


def delete_label(label_id):
    requests.delete(
        f"https://api.todoist.com/rest/v1/labels/{label_id}",
        headers={"Authorization": "Bearer " + token},
    )


if __name__ == "__main__":
    create_date_next_action_task(
        "156478", "test", [2158785495, 2158785496], "2021-11-07T22:00:00.000+09:00"
    )
