import gsheet_func
import notion_db


def update_notion_stocks():
    stocks_from_sheet = list(set(gsheet_func.get_sheet_stocks()))
    stocks_from_db = notion_db.get_pages_from_stock_db()

    new_stocks = [i for i in stocks_from_sheet if i not in stocks_from_db]
    print(new_stocks)

    for stock in new_stocks:
        notion_db.create_page(stock)