import gsheet_func
import notion_db
import tododist_task
import json, os


def update_notion_stocks():
    stocks_from_sheet = list(set(gsheet_func.get_sheet_stocks()))
    stocks_from_db = notion_db.get_pages_from_stock_db()

    new_stocks = [i for i in stocks_from_sheet if i not in stocks_from_db]
    print(new_stocks)

    for stock in new_stocks:
        notion_db.create_stock_page(stock)


def sync_todoist2notion():
    todo_tasks = tododist_task.get_tasks()

    data_path = 'sync_data.json'
    relation_data = dict()
    if not os.path.exists(data_path):
        pass
    else:
        with open(data_path, 'r') as f:  
            relation_data = json.load(f)
    task_not_in_notion = [t for t in todo_tasks if t['id'] not in relation_data.keys()]

    for task in task_not_in_notion:
        page_id = notion_db.create_action_page(task['title'], task['endDate'])
        relation_data[task['id']] = page_id
    
    with open(data_path, 'w') as f:  
            json.dump(relation_data, f)