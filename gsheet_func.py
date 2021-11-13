import gspread
from os import environ

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
sh = gc.open_by_key("1Y1Os2QRLS5BcGgMMFpS-YnXmIEnLpjfClYYgvN2Gcko")


def get_sheet_stocks():
    worksheet = sh.worksheet("매매 내역")
    stocks = worksheet.col_values(3)[1:]
    return stocks
