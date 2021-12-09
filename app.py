from multiprocessing import Process
from pprint import pprint

from flask import Flask, abort, request

from SH.util import notion_cleanup_SH
from util import (
    handle_webhook_task,
    notion2todoist_and_notion_cleanup,
    work_on_fin_reports,
)

app = Flask(__name__)


@app.route("/")
def hello_world():
    # heavy_process = Process(  # Create a daemonic process with heavy "my_func"
    #     target=update_notion_stocks, daemon=True
    # )
    # heavy_process.start()
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
        target=notion2todoist_and_notion_cleanup, daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


@app.route("/reports/update")
def update_fin_reports():
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=work_on_fin_reports, daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


@app.route("/sh-notion-clean-gtd")
def notion_for_SH():
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=notion_cleanup_SH, daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


if __name__ == "__main__":
    app.run(debug=False)
