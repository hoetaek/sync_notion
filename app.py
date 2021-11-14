from flask import Flask, request, abort
from multiprocessing import Process
from pprint import pprint

from util import sync_date_next_actions2todoist, update_notion_stocks, handle_webhook_task


app = Flask(__name__)


@app.route("/")
def hello_world():
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=update_notion_stocks, daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


@app.route("/todoist/webhook", methods=["POST"])
def todoist():
    if request.method == "POST":
        item = request.json
        pprint(item)
        handle_webhook_task(item)
        return "success", 200
    else:
        abort(400)


@app.route("/todoist/next-actions")
def notion2todoist():
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=sync_date_next_actions2todoist, daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


if __name__ == "__main__":
    app.run(debug=False)
