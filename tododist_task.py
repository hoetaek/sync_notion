from os import environ
import requests, uuid, json


token = environ["TODOIST_TOKEN"]
project_id = 2169583011
def get_inbox_tasks():
    inbox_project_id = 2169583011
    result = requests.get(
        "https://api.todoist.com/rest/v1/tasks",
        params={"project_id": inbox_project_id},
        headers={
            "Authorization": "Bearer " + token
        }).json()
    return result


def create_inbox_task():
    inbox_project_id = 2169583011
    result = requests.post(
        "https://api.todoist.com/rest/v1/tasks",
        data=json.dumps({
            "content": "Buy Milk",
            "project_id": inbox_project_id
        }),
        headers={
            "Content-Type": "application/json",
            "X-Request-Id": str(uuid.uuid4()),
            "Authorization": "Bearer " + token
        }).json()
    return result


def update_task(todoist_id, title):
    requests.post(
        "https://api.todoist.com/rest/v1/tasks/" + todoist_id,
        data=json.dumps({
            "content": title
        }),
        headers={
            "Content-Type": "application/json",
            "X-Request-Id": str(uuid.uuid4()),
            "Authorization": "Bearer " + token
        })


def get_all_labels():
    labels = requests.get(
        "https://api.todoist.com/rest/v1/labels", 
        headers={
            "Authorization": "Bearer " + token
        }).json()
    return [label for label in labels]


def create_label(label_name):
    result = requests.post(
        "https://api.todoist.com/rest/v1/labels",
        data=json.dumps({
            "name": label_name
        }),
        headers={
            "Content-Type": "application/json",
            "X-Request-Id": str(uuid.uuid4()),
            "Authorization": "Bearer " + token
        }).json()
    return result
    

if __name__=="__main__":
    print(create_inbox_task())