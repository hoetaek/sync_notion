import requests

if __name__ == "__main__":
    urls = [
        # "/todoist/next-actions",
        "/reports/update",
        "/sh-notion-clean-gtd",
        "/sh-personal-clean-gtd",
        "/hds-notion-clean-gtd",
        "/kkanbu-notion-clean-gtd",
    ]
    for url in urls:
        res = requests.get("http://127.0.0.1:5000" + url)
        print(res.status_code)
"""https://notion-util.herokuapp.com/kkanbu-notion-clean-gtd"""
