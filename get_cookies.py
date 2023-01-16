import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree
import time
from multiprocessing import Manager
import pandas as pd
from utils.utils import *
from utils.parallel_computing import *
from Configs.configs import *



def get_chrome_driver():
    # while True:
    """
    chromeOptions 是一个配置 chrome 启动是属性的类,就是初始化
    """
    option = webdriver.ChromeOptions()
    """
    add_experimental_option 添加实验性质的设置参数
    """
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    '''
    add_argument 添加启动参数
    '''

    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-dev-usage")
    # option.add_argument('--headless')
    """
    Chrome 配置驱动
    """
    driver = webdriver.Chrome(options=option)  # 在这里更换自己的谷歌驱动的地址
    driver.set_page_load_timeout(15)
    return driver

def get_fox_driver():
    options = webdriver.FirefoxOptions()
    # options.add_argument('-headless')  # 无头参数

    driver = webdriver.Firefox(options=options)

    return driver

# driver = get_fox_driver()
driver = get_chrome_driver()

driver.get("https://www.kugou.com/?islogout")

time.sleep(1)

login_button = driver.find_element('xpath','/html/body/div[1]/div[1]/div/div[2]/div[2]/div[1]')
login_button.click()
while (input("Wait? \n")):
    pass

all_cookies = driver.get_cookies()
print(all_cookies)