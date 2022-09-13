from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from constants import *

driver = webdriver.Chrome(DRIVER_PATH)
wait = WebDriverWait(webdriver, 5)
actions = ActionChains(driver)


