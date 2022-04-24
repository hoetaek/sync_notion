from os import environ

import gspread

credentials = {
    "type": "service_account",
    "project_id": "gsheet-notion-stock",
    "private_key_id": environ["PRIVATE_KEY_ID"],
    "private_key": environ["PRIVATE_KEY"].replace("\\n", "\n"),
    "client_email": "get-stock-info@gsheet-notion-stock.iam.gserviceaccount.com",
    "client_id": "113516897813603369913",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/get-stock-info%40gsheet-notion-stock.iam.gserviceaccount.com",
}


gc = gspread.service_account_from_dict(credentials)
stock_sh = gc.open_by_key("1Y1Os2QRLS5BcGgMMFpS-YnXmIEnLpjfClYYgvN2Gcko")
hds_sh = gc.open_by_key("1ki42gx7Wdv5BuJegYrqybSZdy6h7XNi0JQXcPxBWPHE")


def get_sheet_stocks():
    worksheet = stock_sh.worksheet("매매 내역")
    stocks = worksheet.col_values(3)[1:]
    return stocks


def get_indi_urls():
    worksheet = hds_sh.worksheet("04 인디스쿨 게시물 모음")
    urls = worksheet.col_values(5)[4:]
    return urls


def write_view_heart_num(input_list, input_type="view"):
    worksheet = hds_sh.worksheet("04 인디스쿨 게시물 모음")
    cell_range = "F5:F" if input_type == "view" else "G5:G"
    cell_list = worksheet.range(cell_range + str(len(input_list) + 1))

    for i, val in enumerate(input_list):  # gives us a tuple of an index and value
        cell_list[
            i
        ].value = val  # use the index on cell_list and the val from cell_values

    worksheet.update_cells(cell_list)
