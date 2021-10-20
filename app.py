from util import update_notion_stocks, sync_todoist2notion
from flask import Flask
from multiprocessing import Process


app = Flask(__name__)


@app.route('/')
def hello_world():
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=update_notion_stocks,
        daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


@app.route('/todoist')
def todoist():
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=sync_todoist2notion,
        daemon=True
    )
    heavy_process.start()
    return "<script>window.onload = window.close();</script>"


if __name__ == '__main__':
    app.run(debug=False)
