import requests
from os import environ


token = environ["TODOIST_TOKEN"]
project_id = 2169583011
def get_tasks(project_id=project_id):
    result = requests.get(
        "https://api.todoist.com/rest/v1/tasks",
        params={"project_id": project_id},
        headers={
            "Authorization": "Bearer " + token
        }).json()

    tasks = [{"id": r["id"], "title": r["content"], "endDate": r.get("due").get("date") if r.get("due") != None else None} for r in result]
    return tasks


if __name__=="__main__":
    tasks = get_tasks()
    print(tasks)