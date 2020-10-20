import cromdriver
from selenium import webdriver

option = webdriver.ChromeOptions()
#option.add_argument('headless')

driver = webdriver.Chrome(options=option)
driver.get('https://www.google.com')