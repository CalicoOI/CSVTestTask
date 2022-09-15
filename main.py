import time
import requests
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv_writer
from constants import *
from programStartSetup import *

result_list = list()
csv_w = csv_writer.csv_access(OUTPUT_CSV_PATH, result_list)


def navigate_main_page():
    driver.get(MAIN_PAGE_LINK)


def set_year_range():
    year_table = driver.find_element(By.XPATH, TIME_RANGE_UL)
    year_table.find_element(By.PARTIAL_LINK_TEXT, '2018').click()


def parse_page():
    page = requests.get(driver.current_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    result_block = soup.find("div", {"id": RESULT_BLOCK_ID})
    result_divs = result_block.findAll("div", {"class": "gs_r"})

    for el in result_divs:
        res_dict = dict()

        res_dict[FILE_HEADERS[0]] = el.findNext("div", {"class": "gs_ri"}).findNext('h3').text
        res_dict[FILE_HEADERS[1]] = get_clean_authors(el.findNext("div", {"class": "gs_a"}).text)
        res_dict[FILE_HEADERS[2]] = get_clean_date(el.findNext("div", {"class": "gs_a"}).text)

        cit_div = el.findNext("div", {"class": "gs_fl"})
        citations = cit_div.findAll('a')

        if len(citations) > 1:
            citations = citations[2].text.replace(CITATION_CUR_LANG, '')
        else:
            citations = '0'

        res_dict[FILE_HEADERS[3]] = citations
        res_dict[FILE_HEADERS[4]] = el.findNext("div", {"class": "gs_ri"}).findNext('a').attrs.get('href')
        result_list.append(res_dict)


def order_list_by(key: str):
    global result_list
    result_list = sorted(result_list, key=lambda by: by[key])


def get_clean_date(row: str):
    part = row.rpartition('-')[0]
    return part[len(part) - 5:].strip()


def get_clean_authors(row):
    return row[0: row.index('-')].strip()


def perform_keyboard_press(key=Keys.ENTER):
    actions.send_keys(key).perform()
    actions.release()


def perform_btn_click(xpath):
    actions.click(driver.find_element(By.XPATH, xpath)).perform()
    actions.release()


def paste_text(text):
    actions.send_keys(Keys.CONTROL + text).perform()
    actions.release()


def fill_input_field(name, value):
    try:
        actions.send_keys_to_element(driver.find_element(By.XPATH, name), value).perform()
        actions.release()
    except NoSuchElementException:
        print("Can't find element by XPATH: " + name)


def do_search():
    fill_input_field(SEARCH_INPUT, SEARCH_TEXT)
    time.sleep(1)
    perform_keyboard_press()
    time.sleep(1)
    set_year_range()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)


def order_result_list():
    order_list_by(FILE_HEADERS[3])
    order_list_by(FILE_HEADERS[0])


def d_quit(): driver.quit()


if __name__ == '__main__':
    navigate_main_page()
    do_search()
    parse_page()
    order_result_list()
    csv_w.write_to_csv()
    d_quit()
