from os import environ

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

view_nums = []
heart_nums = []


def login(driver):
    indi_username = environ["INDI_USERNAME"]
    indi_password = environ["INDI_PASSWORD"]
    driver.get("https://indischool.com/login")
    driver.find_element_by_id("username").send_keys(indi_username)
    driver.find_element_by_id("password").send_keys(indi_password)
    driver.find_element_by_css_selector("span > button").click()


def get_view_heart_num(driver, url):
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    view_num = int(soup.select("#post_tools > div:nth-child(2) > span")[0].text)
    heart_num = int(soup.select("#post_tools > div.flex.items-center.-mx-2")[0].text)

    view_nums.append(view_num)
    heart_nums.append(heart_num)
    print(view_num, heart_num)
    return view_num, heart_num


def work(urls):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    login(driver)

    for url in urls:
        get_view_heart_num(driver, url)
    driver.quit()

    return view_nums, heart_nums
