from multiprocessing import Process
from pprint import pprint

from flask import Flask, abort, request

from others.util import (
    notion_cleanup_coding_kkanbu,
    notion_cleanup_edutech,
    notion_cleanup_GBinder,
    notion_cleanup_HDS,
    notion_cleanup_SH_PERSONAL,
    notion_cleanup_SH_teacher,
    update_hds_indi_num,
)
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
        target=notion_cleanup_SH_teacher, daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


@app.route("/sh-personal-clean-gtd")
def notion_for_SH_PERSONAL():
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=notion_cleanup_SH_PERSONAL, daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


@app.route("/hds-notion-clean-gtd")
def notion_for_HDS():
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=notion_cleanup_HDS, daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


@app.route("/hds-gspread-update-num")
def gspread_for_HDS():
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=update_hds_indi_num, daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


@app.route("/gbinder-notion-clean-gtd")
def notion_for_GBinder():
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=notion_cleanup_GBinder, daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


@app.route("/kkanbu-notion-clean-gtd")
def notion_for_kkanbu():
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=notion_cleanup_coding_kkanbu, daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


@app.route("/edutech-notion-clean-gtd")
def notion_for_edutech():
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=notion_cleanup_edutech, daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


if __name__ == "__main__":
    app.run(debug=False, port=4040)
