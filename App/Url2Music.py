import requests
import pickle
import time
from multiprocessing import Manager
from utils.parallel_computing import *
from Configs.configs import *


class Url2Music():
    def __init__(self, save_dir, t2u_pkl_file, u2m_pkl_file):
        self.save_dir = save_dir
        self.record_dict = {}
        self.t2u_pkl_file = t2u_pkl_file
        self.pkl_file = u2m_pkl_file
        self.queue = Manager().Queue()
        self.text2url = None
        self.result_queue = Manager().Queue()
        self.min_size = 0.2*1024*1024 #2KB
        self._my_init()

    def _my_init(self):
        with open(self.t2u_pkl_file, 'rb') as f:
            self.text2url = pickle.load(f)
        if os.path.exists(self.pkl_file):
            with open(self.pkl_file, 'rb') as f:
                self.record_dict = pickle.load(f)
        print(f"self.record_dict: \n{self.record_dict}")
        self.queue = Manager().Queue()
        for file_i in self.text2url:
            if file_i not in self.record_dict:
                self.queue.put([file_i, self.text2url[file_i][0], self.text2url[file_i][1]])
        print(f"{self.queue.qsize()} tasks left")

    def save_music_mp3(self, music_url, save_file):
        try:
            print(f"Begin to get {music_url}")
            music_response = requests.get(music_url).content
            with open(save_file, 'wb')as fp:
                fp.write(music_response)
            stats = os.stat(save_file)
            if stats.st_size <= self.min_size:
                print(f"Save Error(Too Small File) :  url ({music_url})")
                os.remove(save_file)
                return False
            print(f"Saved {music_url}  -> {save_file}")
            return True
        except Exception as err:
            print(f"Save Error : {err}  | url ({music_url})")
            return False

    def url2music(self, cmd):
        if cmd == 'save_data':
            while self.queue.qsize():
                time.sleep(30)
                self.save_data()
            time.sleep(2)
            self.save_data()
        else:
            while self.queue.qsize():
                photo_i, lt_details_i, url_i = self.queue.get()
                if len(lt_details_i) >= 2:
                    if (":" not in lt_details_i[1]):
                        name = f"{lt_details_i[0]}_{lt_details_i[1]}"
                    else:
                        name = lt_details_i[0]
                else:
                    name = lt_details_i[0]
                path_i = os.path.join(self.save_dir, name + '.mp3')
                success = self.save_music_mp3(url_i, path_i)
                if success:
                    self.result_queue.put((photo_i, lt_details_i, url_i, path_i))

    def save_data(self):
        while self.result_queue.qsize():
            photo_i, text_i, url_i, music_i = self.result_queue.get()
            self.record_dict[photo_i] = [text_i, url_i, music_i]
        with open(self.pkl_file, 'wb') as f:
            pickle.dump(self.record_dict, f)
        print(f"Saved! -> {self.record_dict}")

    def muti_thread_run(self, cmd, n_thread=3):
        if cmd == 'save_data':
            self.url2music(cmd)
        else:
            params = ["" for _ in range(n_thread)]
            MultiThread.multi_thread(self.url2music, params)

    def run(self, n_process=10):
        params = ["" for i in range(n_process)] + ['save_data']
        MultiProcess.multi_process(self.muti_thread_run, params)
        return self.record_dict
