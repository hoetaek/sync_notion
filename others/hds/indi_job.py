from os import environ

from bs4 import BeautifulSoup
from selenium import webdriver

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
    on_heroku = False
    if 'HEROKU' in environ:
        on_heroku = True
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # 창을 띄우지 않음
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")  # 샌드박스 보안 비활성화
    if on_heroku:
        chrome_options.binary_location = environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(
            executable_path=environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options
        )
    else:
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)


    login(driver)

    for url in urls:
        get_view_heart_num(driver, url)
    driver.quit()

    return view_nums, heart_nums

if __name__=="__main__":
    work(["https://indischool.com/boards/libArt/37232838"])