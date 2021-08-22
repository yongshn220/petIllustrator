from torchvision import models
from PIL import Image
import matplotlib.pyplot as plt
import torch
import torchvision.transforms as T
import numpy as np
import cv2
from Segmentation import Segmentation as Segment
from Preprocess import Preprocess
from Cartoonify import Cartoonify





class Main:
    def __init__(self, path):
        self.segmentation = Segment()
        self.preprocess = Preprocess()
        self.cartoonify = Cartoonify()
        self.path = path
        self.origin_img = None
        self.mask_img = None
        self.bg_img = None
        self.result_img = None

    def preset(self):
        self.origin_img = cv2.imread('../Images/Raw/dog.jpg', cv2.IMREAD_COLOR)
        self.bg_img = cv2.imread('../Images/Background/Background-white.jpg', cv2.IMREAD_COLOR)


    def main(self):
        self.preset()

        # Image Segmentation
        self.mask_img = self.segment_img()
        # Mask Image (Remove background)
        sel_img = self.preprocess.mask_img(self.origin_img, self.mask_img, self.bg_img)
        # Cartoonify Image
        self.result_img = self.cartoonify.canny_method(sel_img)

        cv2.imshow('test', self.result_img)
        cv2.waitKey()
        return

    def segment_img(self):
        res_img = self.segmentation.segment(self.path)
        return res_img


#Test


m = Main('../Images/Raw/dog.jpg')
m.main()
