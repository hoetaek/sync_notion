from util import sync_date_next_actions2todoist, update_notion_stocks
from notion_gtd import GTD
from todoist_task import Task
from flask import Flask, request, abort
from multiprocessing import Process
from pprint import pprint
from constants import inbox_project_id

app = Flask(__name__)


@app.route('/')
def hello_world():
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=update_notion_stocks,
        daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


@app.route('/todoist/webhook', methods=['POST'])
def todoist():
    if request.method == 'POST':
        item = request.json
        pprint(item)
        if item["event_name"] == "item:completed" and item["event_data"]["description"]:
            gtd = GTD.from_webhook(item)
            gtd.complete()
        elif item["event_name"] == "item:added" and item["event_data"]["project_id"] == inbox_project_id:
            gtd = GTD.from_webhook(item)
            gtd.create()
            task = Task.from_gtd(gtd)
            task.delete()
        return 'success', 200
    else:
        abort(400)


@app.route('/todoist/next-actions')
def notion2todoist():
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=sync_date_next_actions2todoist,
        daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


if __name__ == '__main__':
    app.run(debug=False)
