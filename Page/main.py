import sys

from torchvision import models
from PIL import Image
import matplotlib.pyplot as plt
import torch
import torchvision.transforms as T
import numpy as np
import cv2
from model.Segmentation import Segmentation
from model.Preprocess import Preprocess
from model.Cartoonify import Cartoonify





class Main:
    def __init__(self):
        self.segmentation = Segmentation()
        self.preprocess = Preprocess()
        self.cartoonify = Cartoonify()


    def convert(self, ori_img):

        # Image Segmentation
        mask_img = self.segment_img(ori_img)
        # Mask Image (Remove background)
        bg_img = cv2.imread('./images/Background/Background-white.jpg', cv2.IMREAD_COLOR)
        # merge all Images (Remove Background)
        sel_img = self.preprocess.mask_img(ori_img, mask_img, bg_img)
        # Cartoonify Image
        result_img = self.cartoonify.canny_method(sel_img)

        return result_img

    def segment_img(self, ori_img):
        res_img = self.segmentation.segment(ori_img)
        return res_img
