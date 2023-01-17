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


class Text2Url():
    def __init__(self, save_dir, p2t_pkl_file, t2u_pkl_file):
        self.save_dir = save_dir
        self.record_dict = {}
        self.p2t_pkl_file = p2t_pkl_file
        self.pkl_file = t2u_pkl_file
        self.queue = Manager().Queue()
        self.file2song = None
        self.result_queue = Manager().Queue()
        self.music_pattern = 'mp3$'
        self._my_init()
        self.url = "https://www.kugou.com/yy/html/search.html"
        self.chrome_cookies =[{'domain': '.kugou.com', 'httpOnly': False, 'name': 'Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d', 'path': '/', 'secure': False, 'value': '1673933780'}, {'domain': '.kugou.com', 'expiry': 1674797778, 'httpOnly': True, 'name': 'UserName', 'path': '/', 'secure': False, 'value': '%u006b%u0067%u006f%u0070%u0065%u006e%u0033%u0038%u0030%u0039%u0039%u0031%u0032%u0031%u0035'}, {'domain': '.kugou.com', 'expiry': 1674797778, 'httpOnly': True, 'name': 'a_id', 'path': '/', 'secure': False, 'value': '1014'}, {'domain': '.kugou.com', 'expiry': 1674797778, 'httpOnly': True, 'name': 't', 'path': '/', 'secure': False, 'value': 'd02f9d1008fe0a6867f89a84f425c81005d5731c872af3b67240fc26f918a119'}, {'domain': '.kugou.com', 'expiry': 1674797778, 'httpOnly': True, 'name': 'dfid', 'path': '/', 'secure': False, 'value': '4XSkAn1xi0he4e4ZSZ1VwZur'}, {'domain': '.kugou.com', 'expiry': 1674797778, 'httpOnly': False, 'name': 'KuGoo', 'path': '/', 'secure': False, 'value': 'KugooID=380991215&KugooPwd=027BCBB78F3FCC2E56F22A6BA13943FC&NickName=%u0047%u004d&Pic=http://imge.kugou.com/kugouicon/165/20200518/20200518190356526244.jpg&RegState=1&RegFrom=&t=d02f9d1008fe0a6867f89a84f425c81005d5731c872af3b67240fc26f918a119&t_ts=1673933778&t_key=&a_id=1014&ct=1673933778&UserName=%u006b%u0067%u006f%u0070%u0065%u006e%u0033%u0038%u0030%u0039%u0039%u0031%u0032%u0031%u0035'}, {'domain': 'www.kugou.com', 'expiry': 1673937371, 'httpOnly': False, 'name': 'ACK_SERVER_10015', 'path': '/', 'secure': False, 'value': '%7B%22list%22%3A%5B%5B%22bjlogin-user.kugou.com%22%5D%5D%7D'}, {'domain': '.kugou.com', 'expiry': 1673934073, 'httpOnly': False, 'name': 'kg_mid_temp', 'path': '/', 'secure': False, 'value': 'f2df140f28a3dd9ce09dd6f7d771dcad'}, {'domain': '.kugou.com', 'expiry': 1705469780, 'httpOnly': False, 'name': 'Hm_lvt_aedee6983d4cfc62f509129360d6bb3d', 'path': '/', 'secure': False, 'value': '1673933772'}, {'domain': '.kugou.com', 'expiry': 1674797778, 'httpOnly': True, 'name': 'mid', 'path': '/', 'secure': False, 'value': 'f2df140f28a3dd9ce09dd6f7d771dcad'}, {'domain': 'www.kugou.com', 'expiry': 1673934370, 'httpOnly': False, 'name': 'ACK_SERVER_10017', 'path': '/', 'secure': False, 'value': '%7B%22list%22%3A%5B%5B%22bjverifycode.service.kugou.com%22%5D%5D%7D'}, {'domain': '.kugou.com', 'expiry': 1674020170, 'httpOnly': False, 'name': 'kg_dfid_collect', 'path': '/', 'secure': False, 'value': 'd41d8cd98f00b204e9800998ecf8427e'}, {'domain': '.kugou.com', 'expiry': 1708493769, 'httpOnly': False, 'name': 'kg_mid', 'path': '/', 'secure': False, 'value': 'f2df140f28a3dd9ce09dd6f7d771dcad'}, {'domain': '.kugou.com', 'expiry': 1705469770, 'httpOnly': False, 'name': 'kg_dfid', 'path': '/', 'secure': False, 'value': '4XSkAn1xi0he4e4ZSZ1VwZur'}, {'domain': '.kugou.com', 'expiry': 1674797778, 'httpOnly': True, 'name': 'KugooID', 'path': '/', 'secure': False, 'value': '380991215'}, {'domain': 'www.kugou.com', 'expiry': 1673934370, 'httpOnly': False, 'name': 'ACK_SERVER_10016', 'path': '/', 'secure': False, 'value': '%7B%22list%22%3A%5B%5B%22bjreg-user.kugou.com%22%5D%5D%7D'}]


        self.fox_cookies = [{'name': 'kg_mid', 'value': '897dfa967cb4ef9d6bf9ebb269e805fb', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 2537933705, 'sameSite': 'None'}, {'name': 'ACK_SERVER_10016', 'value': '%7B%22list%22%3A%5B%5B%22bjreg-user.kugou.com%22%5D%5D%7D', 'path': '/', 'domain': 'www.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1673934306, 'sameSite': 'None'}, {'name': 'ACK_SERVER_10017', 'value': '%7B%22list%22%3A%5B%5B%22bjverifycode.service.kugou.com%22%5D%5D%7D', 'path': '/', 'domain': 'www.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1673934306, 'sameSite': 'None'}, {'name': 'kg_dfid', 'value': '4XSoGE0dSjlS184dZ14OZJKB', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1705469706, 'sameSite': 'None'}, {'name': 'kg_dfid_collect', 'value': 'd41d8cd98f00b204e9800998ecf8427e', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1674020106, 'sameSite': 'None'}, {'name': 'ACK_SERVER_10015', 'value': '%7B%22list%22%3A%5B%5B%22bjlogin-user.kugou.com%22%5D%5D%7D', 'path': '/', 'domain': 'www.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1673937306, 'sameSite': 'None'}, {'name': 'kg_mid_temp', 'value': '897dfa967cb4ef9d6bf9ebb269e805fb', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1673934007, 'sameSite': 'None'}, {'name': 'KuGoo', 'value': 'KugooID=380991215&KugooPwd=027BCBB78F3FCC2E56F22A6BA13943FC&NickName=%u0047%u004d&Pic=http://imge.kugou.com/kugouicon/165/20200518/20200518190356526244.jpg&RegState=1&RegFrom=&t=d02f9d1008fe0a6867f89a84f425c810db4d13bb983eb27bec2b2f064aff0b29&t_ts=1673933716&t_key=&a_id=1014&ct=1673933716&UserName=%u006b%u0067%u006f%u0070%u0065%u006e%u0033%u0038%u0030%u0039%u0039%u0031%u0032%u0031%u0035', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1674797716, 'sameSite': 'None'}, {'name': 'KugooID', 'value': '380991215', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': True, 'expiry': 1674797716, 'sameSite': 'None'}, {'name': 't', 'value': 'd02f9d1008fe0a6867f89a84f425c810db4d13bb983eb27bec2b2f064aff0b29', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': True, 'expiry': 1674797716, 'sameSite': 'None'}, {'name': 'a_id', 'value': '1014', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': True, 'expiry': 1674797716, 'sameSite': 'None'}, {'name': 'UserName', 'value': '%u006b%u0067%u006f%u0070%u0065%u006e%u0033%u0038%u0030%u0039%u0039%u0031%u0032%u0031%u0035', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': True, 'expiry': 1674797716, 'sameSite': 'None'}, {'name': 'mid', 'value': '897dfa967cb4ef9d6bf9ebb269e805fb', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': True, 'expiry': 1674797716, 'sameSite': 'None'}, {'name': 'dfid', 'value': '4XSoGE0dSjlS184dZ14OZJKB', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': True, 'expiry': 1674797716, 'sameSite': 'None'}, {'name': 'Hm_lvt_aedee6983d4cfc62f509129360d6bb3d', 'value': '1673933707', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1705469718, 'sameSite': 'None'}, {'name': 'Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d', 'value': '1673933719', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': False, 'sameSite': 'None'}]


    def add_cookie(self, driver, cookie):

        for cookie_i in cookie:
            try:
                driver.add_cookie(cookie_i)
            except  Exception as err:
                print(f"Add Cookie Error:\n {cookie_i}\n {err}")
        return driver

    def _my_init(self):
        with open(self.p2t_pkl_file, 'rb') as f:
            self.file2song = pickle.load(f)
        if os.path.exists(self.pkl_file):
            with open(self.pkl_file, 'rb') as f:
                self.record_dict = pickle.load(f)
        print(f"self.record_dict: \n{self.record_dict}")
        self.queue = Manager().Queue()
        for file_i in self.file2song:
            if file_i not in self.record_dict:
                self.queue.put([file_i, self.file2song[file_i]])
            elif not (re.findall(self.music_pattern, self.record_dict[file_i][1])):
                self.queue.put([file_i, self.file2song[file_i]])
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

    def text2url(self, cmd):
        get_driver = None
        if cmd == 'fire_fox':
            get_driver = self.get_fox_driver
        elif cmd == 'chrome':
            get_driver = self.get_chrome_driver
        elif cmd == 'safari':
            get_driver = self.get_safari_driver
        else:
            while self.queue.qsize():
                time.sleep(20)
                self.save_data()
            time.sleep(2)
            self.save_data()

        while get_driver:
            num_count = 0
            driver = get_driver()

            # driver.delete_all_cookies()
            driver.get(self.url)
            time.sleep(1)
            driver.delete_all_cookies()
            if cmd == 'fire_fox':
                driver = self.add_cookie(driver, self.fox_cookies)
            elif cmd == 'chrome':
                driver = self.add_cookie(driver, self.chrome_cookies)
            else:
                pass
            driver.refresh()
            time.sleep(2)
            while True:
                time.sleep(1)
                path_i, lt_details_i = self.queue.get()
                num_count += 1
                try:
                    search_area = driver.find_element('xpath', '/html/body/div[3]/div/div[1]/input')
                    search_area.clear()
                    time.sleep(1)
                    search_button = driver.find_element('xpath', '/html/body/div[3]/div/div[1]/div')
                    if len(lt_details_i) >= 2:
                        if (":" not in lt_details_i[1]):
                            content = f"{lt_details_i[0]} {lt_details_i[1]}"
                        else:
                            content = lt_details_i[0]
                    else:
                        content = lt_details_i[0]
                    content = content.replace("MV", "")
                    content = content.replace("M ", "")
                    content = content.replace("V ", "")
                    content = content.replace("W", "")
                    content = re.sub(r'[\(|（].+?[\)|）]', "", content)
                    search_area.send_keys(content)
                    time.sleep(1)
                    search_button.click()
                    time.sleep(2)

                    first_song = driver.find_element('xpath', '//*[@class="song_name"]')
                    first_song.click()
                    time.sleep(2 if cmd != 'safari' else 5)
                    driver.switch_to.window(driver.window_handles[-1])  # 新窗口通常为最后一个，若为其他位置则自行处理
                    time.sleep(1)
                    music_div = driver.find_element('xpath', '//audio[@class="music"]')
                    url = music_div.get_attribute('src')
                    result = (path_i, lt_details_i, url)
                    if re.findall(self.music_pattern, url):
                        self.result_queue.put(result)
                        print(f"{cmd}  : {result}")
                    else:
                        print(f"{cmd} (Error) : {result}")

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    if self.queue.qsize() == 0:
                        break
                except Exception as err:
                    with open("text2url_error.log", 'a+') as f:
                        self.queue.put((path_i, lt_details_i))
                        error_log = f'{cmd}  : {path_i} , {lt_details_i}  -> {err}\n'
                        print(error_log)
                        # driver.close()
                        f.write(error_log)
                        break

                if num_count >= 10:
                    # driver.close()
                    break
            if self.queue.qsize() == 0:
                break

    def save_data(self):
        while self.result_queue.qsize():
            key_i, val_i1, val_i2 = self.result_queue.get()
            self.record_dict[key_i] = [val_i1, val_i2]
        with open(self.pkl_file, 'wb') as f:
            pickle.dump(self.record_dict, f)
        print(f"Saved! -> {self.record_dict}")

    def run(self):
        funcs = ['chrome','fire_fox','save_data']
        # funcs = ['chrome']
        MultiProcess.multi_process(self.text2url, funcs)
        return self.record_dict
