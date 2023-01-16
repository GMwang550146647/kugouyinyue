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


class Photo2Text():

    def __init__(self, photo_dir,p2t_pkl_file):
        self.record_dict = {}
        self.pkl_file = p2t_pkl_file
        self.all_photo_files = get_all_pattern_files(photo_dir, '\.jpg')
        self.queue = Manager().Queue()
        self.result_queue = Manager().Queue()
        self._my_init()

    def _my_init(self):
        if os.path.exists(self.pkl_file):
            with open(self.pkl_file, 'rb') as f:
                self.record_dict = pickle.load(f)
        print(f"self.record_dict: \n{self.record_dict}")
        self.queue = Manager().Queue()
        for file_i in self.all_photo_files:
            if file_i not in self.record_dict:
                self.queue.put(file_i)
        print(f"{self.queue.qsize()} tasks left")

    def get_chrome_driver(self):
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
        option.add_argument('--headless')
        """
        Chrome 配置驱动
        """
        driver = webdriver.Chrome(options=option)  # 在这里更换自己的谷歌驱动的地址
        driver.set_page_load_timeout(15)
        return driver

    def get_fox_driver(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')  # 无头参数

        driver = webdriver.Firefox(options=options)

        return driver

    def get_safari_driver(self):
        # options.add_argument('-headless')  # 无头参数

        driver = webdriver.Safari()

        return driver

    def photo2text(self, cmd):
        get_driver=None
        if cmd == 'fire_fox':
            get_driver = self.get_fox_driver
        elif cmd == 'chrome':
            get_driver =self.get_chrome_driver
        elif cmd == 'safari':
            get_driver = self.get_safari_driver
        else:
            while self.queue.qsize():
                time.sleep(20)
                self.save_data()
            time.sleep(2)
            self.save_data()


        url = "https://catocr.com/#/"
        while get_driver:
            num_output = 0
            driver = get_driver()
            driver.get(url)
            time.sleep(5)
            driver.delete_all_cookies()
            while self.queue.qsize():
                file_i = self.queue.get()
                anniu = driver.find_element('xpath', '//*[@id="app"]/div[2]/div/div[1]/div[3]/input')
                driver.execute_script('arguments[0].style.visibility=\'visible\'', anniu)
                anniu.send_keys(file_i)
                time.sleep(4)
                text_pos = driver.find_elements('xpath', '//div[@class="imagebox__textInner"]')
                text = [text_pos_i.get_attribute("textContent") for text_pos_i in text_pos]
                result = (file_i, text)
                print(f"{cmd} : {result}")
                if result[1]:
                    self.result_queue.put(result)
                num_output += 1
                if num_output >= 5:
                    driver.close()
                    break
            if self.queue.qsize()==0:
                break

    def save_data(self):
        while self.result_queue.qsize():
            key_i, val_i = self.result_queue.get()
            self.record_dict[key_i] = val_i
        with open(self.pkl_file, 'wb') as f:
            pickle.dump(self.record_dict, f)
        print(f"Saved! -> {self.record_dict}")

    def run(self):
        funcs = ['fire_fox','chrome','safari','save_data']
        MultiProcess.multi_process(self.photo2text, funcs)
        return self.record_dict