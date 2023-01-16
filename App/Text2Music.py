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

class Text2Music():
    def __init__(self,save_dir,p2t_pkl_file,t2m_pkl_file):
        self.save_dir = save_dir
        self.record_dict = {}
        self.p2t_pkl_file = p2t_pkl_file
        self.pkl_file = t2m_pkl_file
        self.queue = Manager().Queue()
        self.file2song = None
        self.result_queue = Manager().Queue()
        self._my_init()
        self.url = "https://www.kugou.com/yy/html/search.html"
        self.chrome_cookies =  [{'domain': '.kugou.com', 'httpOnly': False, 'name': 'Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d', 'path': '/', 'secure': False, 'value': '1673857572'}, {'domain': '.kugou.com', 'expiry': 1674721570, 'httpOnly': True, 'name': 'UserName', 'path': '/', 'secure': False, 'value': '%u006b%u0067%u006f%u0070%u0065%u006e%u0033%u0038%u0030%u0039%u0039%u0031%u0032%u0031%u0035'}, {'domain': '.kugou.com', 'expiry': 1674721570, 'httpOnly': True, 'name': 'a_id', 'path': '/', 'secure': False, 'value': '1014'}, {'domain': '.kugou.com', 'expiry': 1674721570, 'httpOnly': True, 'name': 't', 'path': '/', 'secure': False, 'value': 'd02f9d1008fe0a6867f89a84f425c81092f172353fec646fdf85d5d5f317470e'}, {'domain': '.kugou.com', 'expiry': 1674721570, 'httpOnly': True, 'name': 'dfid', 'path': '/', 'secure': False, 'value': '2mSmE11xi0lG107ryZ2puWxt'}, {'domain': '.kugou.com', 'expiry': 1674721570, 'httpOnly': False, 'name': 'KuGoo', 'path': '/', 'secure': False, 'value': 'KugooID=380991215&KugooPwd=027BCBB78F3FCC2E56F22A6BA13943FC&NickName=%u0047%u004d&Pic=http://imge.kugou.com/kugouicon/165/20200518/20200518190356526244.jpg&RegState=1&RegFrom=&t=d02f9d1008fe0a6867f89a84f425c81092f172353fec646fdf85d5d5f317470e&t_ts=1673857570&t_key=&a_id=1014&ct=1673857570&UserName=%u006b%u0067%u006f%u0070%u0065%u006e%u0033%u0038%u0030%u0039%u0039%u0031%u0032%u0031%u0035'}, {'domain': 'www.kugou.com', 'expiry': 1673861164, 'httpOnly': False, 'name': 'ACK_SERVER_10015', 'path': '/', 'secure': False, 'value': '%7B%22list%22%3A%5B%5B%22bjlogin-user.kugou.com%22%5D%5D%7D'}, {'domain': '.kugou.com', 'expiry': 1673857865, 'httpOnly': False, 'name': 'kg_mid_temp', 'path': '/', 'secure': False, 'value': '0d1789781aca68574beb317798a6ea68'}, {'domain': '.kugou.com', 'expiry': 1705393571, 'httpOnly': False, 'name': 'Hm_lvt_aedee6983d4cfc62f509129360d6bb3d', 'path': '/', 'secure': False, 'value': '1673857564'}, {'domain': '.kugou.com', 'expiry': 1674721570, 'httpOnly': True, 'name': 'KugooID', 'path': '/', 'secure': False, 'value': '380991215'}, {'domain': 'www.kugou.com', 'expiry': 1673858164, 'httpOnly': False, 'name': 'ACK_SERVER_10016', 'path': '/', 'secure': False, 'value': '%7B%22list%22%3A%5B%5B%22bjreg-user.kugou.com%22%5D%5D%7D'}, {'domain': '.kugou.com', 'expiry': 1674721570, 'httpOnly': True, 'name': 'mid', 'path': '/', 'secure': False, 'value': '0d1789781aca68574beb317798a6ea68'}, {'domain': 'www.kugou.com', 'expiry': 1673858164, 'httpOnly': False, 'name': 'ACK_SERVER_10017', 'path': '/', 'secure': False, 'value': '%7B%22list%22%3A%5B%5B%22bjverifycode.service.kugou.com%22%5D%5D%7D'}, {'domain': '.kugou.com', 'expiry': 1673943964, 'httpOnly': False, 'name': 'kg_dfid_collect', 'path': '/', 'secure': False, 'value': 'd41d8cd98f00b204e9800998ecf8427e'}, {'domain': '.kugou.com', 'expiry': 1708417563, 'httpOnly': False, 'name': 'kg_mid', 'path': '/', 'secure': False, 'value': '0d1789781aca68574beb317798a6ea68'}, {'domain': '.kugou.com', 'expiry': 1705393564, 'httpOnly': False, 'name': 'kg_dfid', 'path': '/', 'secure': False, 'value': '2mSmE11xi0lG107ryZ2puWxt'}]

        self.fox_cookies=[{'name': 'kg_mid', 'value': 'abb3b57b46a5f213cc4cc743632194ad', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 2537857508, 'sameSite': 'None'}, {'name': 'ACK_SERVER_10017', 'value': '%7B%22list%22%3A%5B%5B%22bjverifycode.service.kugou.com%22%5D%5D%7D', 'path': '/', 'domain': 'www.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1673858108, 'sameSite': 'None'}, {'name': 'ACK_SERVER_10016', 'value': '%7B%22list%22%3A%5B%5B%22bjreg-user.kugou.com%22%5D%5D%7D', 'path': '/', 'domain': 'www.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1673858108, 'sameSite': 'None'}, {'name': 'kg_dfid', 'value': '08xtOI0dSjrO3CNKPX4Q88L6', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1705393509, 'sameSite': 'None'}, {'name': 'kg_dfid_collect', 'value': 'd41d8cd98f00b204e9800998ecf8427e', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1673943909, 'sameSite': 'None'}, {'name': 'ACK_SERVER_10015', 'value': '%7B%22list%22%3A%5B%5B%22bjlogin-user.kugou.com%22%5D%5D%7D', 'path': '/', 'domain': 'www.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1673861109, 'sameSite': 'None'}, {'name': 'kg_mid_temp', 'value': 'abb3b57b46a5f213cc4cc743632194ad', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1673857810, 'sameSite': 'None'}, {'name': 'KuGoo', 'value': 'KugooID=380991215&KugooPwd=027BCBB78F3FCC2E56F22A6BA13943FC&NickName=%u0047%u004d&Pic=http://imge.kugou.com/kugouicon/165/20200518/20200518190356526244.jpg&RegState=1&RegFrom=&t=d02f9d1008fe0a6867f89a84f425c8109dfe55903ff809545588465e86c37838&t_ts=1673857519&t_key=&a_id=1014&ct=1673857519&UserName=%u006b%u0067%u006f%u0070%u0065%u006e%u0033%u0038%u0030%u0039%u0039%u0031%u0032%u0031%u0035', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1674721519, 'sameSite': 'None'}, {'name': 'KugooID', 'value': '380991215', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': True, 'expiry': 1674721519, 'sameSite': 'None'}, {'name': 't', 'value': 'd02f9d1008fe0a6867f89a84f425c8109dfe55903ff809545588465e86c37838', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': True, 'expiry': 1674721519, 'sameSite': 'None'}, {'name': 'a_id', 'value': '1014', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': True, 'expiry': 1674721519, 'sameSite': 'None'}, {'name': 'UserName', 'value': '%u006b%u0067%u006f%u0070%u0065%u006e%u0033%u0038%u0030%u0039%u0039%u0031%u0032%u0031%u0035', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': True, 'expiry': 1674721519, 'sameSite': 'None'}, {'name': 'mid', 'value': 'abb3b57b46a5f213cc4cc743632194ad', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': True, 'expiry': 1674721519, 'sameSite': 'None'}, {'name': 'dfid', 'value': '08xtOI0dSjrO3CNKPX4Q88L6', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': True, 'expiry': 1674721519, 'sameSite': 'None'}, {'name': 'Hm_lvt_aedee6983d4cfc62f509129360d6bb3d', 'value': '1673857509', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': False, 'expiry': 1705393520, 'sameSite': 'None'}, {'name': 'Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d', 'value': '1673857521', 'path': '/', 'domain': '.kugou.com', 'secure': False, 'httpOnly': False, 'sameSite': 'None'}]


    def add_cookie(self,driver,cookie):


        for cookie_i in cookie:
            try:
                driver.add_cookie(cookie_i)
            except  Exception as err:
                print(f"Add Cookie Error:\n {cookie_i}\n {err}")
        return driver

    def _my_init(self):
        with open(self.p2t_pkl_file,'rb') as f:
            self.file2song = pickle.load(f)
        if os.path.exists(self.pkl_file):
            with open(self.pkl_file, 'rb') as f:
                self.record_dict = pickle.load(f)
        print(f"self.record_dict: \n{self.record_dict}")
        self.queue = Manager().Queue()
        for file_i in self.file2song:
            if file_i not in self.record_dict:
                self.queue.put([file_i,self.file2song[file_i]])
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
                num_count +=1
                try:
                    search_area = driver.find_element('xpath','/html/body/div[3]/div/div[1]/input')
                    search_area.clear()
                    time.sleep(1)
                    search_button = driver.find_element('xpath','/html/body/div[3]/div/div[1]/div')
                    if len(lt_details_i)>=2:
                        if (":" not in lt_details_i[1]):
                            content = f"{lt_details_i[0]} {lt_details_i[1]}"
                        else:
                            content = lt_details_i[0]
                    else:
                        content=lt_details_i[0]
                    content=content.replace("MV","")
                    content = content.replace("M ", "")
                    content=content.replace("V ","")
                    content=content.replace("W","")
                    content = re.sub(r'[\(|（].+?[\)|）]',"",content)
                    search_area.send_keys(content)
                    time.sleep(1)
                    search_button.click()
                    time.sleep(2)
                    first_song = driver.find_element('xpath', '//*[@class="song_name"]')
                    first_song.click()
                    time.sleep(2 if cmd!='safari' else 5)
                    driver.switch_to.window(driver.window_handles [-1])  # 新窗口通常为最后一个，若为其他位置则自行处理
                    time.sleep(1)
                    music_div = driver.find_element('xpath','//audio[@class="music"]')
                    url = music_div.get_attribute('src')
                    result = (path_i,lt_details_i,url)
                    print(f"{cmd}  : {result}")
                    self.result_queue.put(result)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    if self.queue.qsize() == 0:
                        break
                except Exception as err:
                    with open("error.log",'w') as f:
                        self.queue.put((path_i,lt_details_i))
                        error_log = f'{cmd}  : {path_i} , {lt_details_i}  -> {err}\n'
                        print(error_log)
                        f.write(error_log)

                if num_count>=10:
                    break
            if self.queue.qsize()==0:
                break

    def save_data(self):
        while self.result_queue.qsize():
            key_i, val_i1,val_i2 = self.result_queue.get()
            self.record_dict[key_i] = [val_i1,val_i2]
        with open(self.pkl_file, 'wb') as f:
            pickle.dump(self.record_dict, f)
        print(f"Saved! -> {self.record_dict}")

    def run(self):
        funcs = ['chrome','fire_fox','save_data']
        # funcs = ['chrome']
        MultiProcess.multi_process(self.photo2text, funcs)
        return self.record_dict