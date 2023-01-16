from App.Photo2Text import *
from App.SplitPhoto import *
from App.Text2Music import *
from Configs.configs import *
class Flow():
    def __init__(self):
        self.PHOTO_DIR =os.path.join(DATA_PATH,'input')
        self.SPLITED_PHOTO_DIR =os.path.join(DATA_PATH,'splited_photos')
        self.MUSIC_DIR =os.path.join(DATA_PATH,'music')
        self.p2t_pkl_file = os.path.join(DATA_PATH, 'Photo2Text.pkl')
        self.t2m_pkl_file = os.path.join(DATA_PATH, 'Text2Music.pkl')
        os.makedirs(self.PHOTO_DIR,exist_ok=True)
        os.makedirs(self.SPLITED_PHOTO_DIR,exist_ok=True)
        os.makedirs(self.MUSIC_DIR,exist_ok=True)

    def run(self):
        SplitPhoto(self.PHOTO_DIR,self.SPLITED_PHOTO_DIR).run()
        Photo2Text(self.SPLITED_PHOTO_DIR,self.p2t_pkl_file).run()
        Text2Music(self.MUSIC_DIR,self.p2t_pkl_file,self.t2m_pkl_file).run()
