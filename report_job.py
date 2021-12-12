from datetime import datetime

import requests
from bs4 import BeautifulSoup


def crawl_fin_reports():
    res = requests.get("https://finance.naver.com/research/industry_list.naver")
    html = res.text

    soup = BeautifulSoup(html, "html.parser")

    reports = []
    for tr in soup.select("tr")[:47]:
        report = dict()
        for i, td in enumerate(tr.select("td")):
            if i == 0:
                report["catalog"] = td.text
            elif i == 1:
                report["title"] = td.text
                report["link"] = (
                    "https://finance.naver.com/research/" + td.select("a")[0]["href"]
                )

                res = requests.get(report["link"])
                html = res.text
                soup = BeautifulSoup(html, "html.parser")
                content = "\n".join([i.text for i in soup.select("div > p")])
                report["content"] = content

            elif i == 2:
                report["brokerage"] = td.text
            elif i == 3:
                report["file_url"] = td.select("a")[0]["href"]
            elif i == 4:
                report["date"] = datetime.strptime(td.text, "%y.%m.%d").strftime(
                    "%Y-%m-%d"
                )
        if report and ("title" in report.keys()):
            reports.append(report)
    return reports
