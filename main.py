import collections
import time
import requests
import csv_writer
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import *
from programStartSetup import *

result_list = list()
csv_w = csv_writer.csv_access(OUTPUT_CSV_PATH)


def navigate_main_page():
    driver.get(MAIN_PAGE_LINK)


def set_year_range():
    ul_table = driver.find_element(By.XPATH, TIME_RANGE_UL)
    ul_table.find_element(By.PARTIAL_LINK_TEXT, '2018').click()


def parse_page():
    page = requests.get(driver.current_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    result_block = soup.find("div", {"id": RESULT_BLOCK_ID})
    result_divs = result_block.findAll("div", {"class": "gs_r"})
    # res_div = soup.find_all(id=RESULT_BLOCK_ID)

    for el in result_divs:
        article_text = el.text
        authors = el.findNext("div", {"class": "gs_a"}).findNext('a').text
        year = el.findNext("div", {"class": "gs_a"}).text #tmp

        citations = el.findNext("div", {"class": "gs_fl"}).findAll('a')

        if len(citations) > 1:
            citations = citations[2].text.replace("Cituoja", '')
        else:
            citations = 'cant get value'

        link = el.findNext("div", {"class": "gs_ri"}).findNext('a').attrs.get('href')

        scrapped_info = {article_text, authors, year, citations, link}
        result_list.append(scrapped_info)

    print()


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
        print('Cant\'t find element by XPATH: ' + name)


def do_search():
    fill_input_field(SEARCH_INPUT, SEARCH_TEXT)
    perform_keyboard_press()
    set_year_range()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def d_quit(): driver.quit()


if __name__ == '__main__':
    navigate_main_page()
    do_search()
    parse_page()
    csv_w.write_to_csv()
    d_quit()
