from App.Tasks.Photo2Text import *
from App.Tasks.SplitPhoto import *
from App.Tasks.Text2Url import *
from App.Tasks.Url2Music import *
from App.Tasks.CheckMusic import *
from Configs.configs import *
class Flow():
    def __init__(self):
        self.PHOTO_DIR =os.path.join(DATA_PATH,'input')
        self.SPLITED_PHOTO_DIR =os.path.join(DATA_PATH,'splited_photos')
        self.URL_DIR =os.path.join(DATA_PATH,'url')
        self.MUSIC_DIR =os.path.join(DATA_PATH,'music')
        self.p2t_pkl_file = os.path.join(DATA_PATH, 'Photo2Text.pkl')
        self.t2u_pkl_file = os.path.join(DATA_PATH, 'Text2Url.pkl')
        self.u2m_pkl_file = os.path.join(DATA_PATH, 'Url2Music.pkl')
        os.makedirs(self.PHOTO_DIR,exist_ok=True)
        os.makedirs(self.SPLITED_PHOTO_DIR,exist_ok=True)
        os.makedirs(self.URL_DIR,exist_ok=True)
        os.makedirs(self.MUSIC_DIR,exist_ok=True)

    def run(self):
        # SplitPhoto(self.PHOTO_DIR,self.SPLITED_PHOTO_DIR).run()
        # Photo2Text(self.SPLITED_PHOTO_DIR,self.p2t_pkl_file).run()
        # Text2Url(self.URL_DIR,self.p2t_pkl_file,self.t2u_pkl_file).run()
        Url2Music(self.MUSIC_DIR,self.t2u_pkl_file,self.u2m_pkl_file).run()
        CheckMusic(self.MUSIC_DIR,self.t2u_pkl_file,self.u2m_pkl_file).run()
