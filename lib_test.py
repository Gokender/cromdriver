import cromdriver
from selenium import webdriver

option = webdriver.ChromeOptions()
#option.add_argument('headless')

print(cromdriver.get_chromedriver_path())

#driver = webdriver.Chrome(options=option)
#driver.get('https://www.google.com')
#driver.quit()