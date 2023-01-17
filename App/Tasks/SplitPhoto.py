import os
from pdf2docx import Converter
import cv2 as cv
from PIL import Image
import pytesseract
from utils.utils import *


class SplitPhoto():
    def __init__(self, input_dir, output_dir, min_thresh=150, max_thresh=230, min_pxl_distance=40):
        self.min_thresh = min_thresh
        self.max_thresh = max_thresh
        self.min_pxl_distance = min_pxl_distance
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def save_photos(self, photo, file_name):
        cv.imwrite(file_name, photo, [cv.IMWRITE_JPEG_QUALITY, 100])

    def run(self):
        files = get_all_pattern_files(self.input_dir, '\.(png|jpg)')
        for i, file_i in enumerate(files):
            photo_i = cv.imread(file_i, cv.IMREAD_GRAYSCALE)
            tempt = photo_i.mean(axis=1)
            filter_flag = (tempt >= self.min_thresh)
            tempt = tempt[filter_flag]
            photo_i = photo_i[filter_flag, :]
            div_index = []
            for j, val_j in enumerate(tempt):
                if val_j < self.max_thresh and ((not div_index) or (j - div_index[-1]) >= self.min_pxl_distance):
                    div_index.append(j)
            print((div_index))

            for j in range(1, len(div_index)):
                photo_j = photo_i[div_index[j - 1]:div_index[j], :]
                file_name_j = os.path.join(self.output_dir, f'{i}_{j}.jpg')
                self.save_photos(photo_j, file_name_j)
