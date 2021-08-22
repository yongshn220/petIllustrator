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
    def __init__(self, ori_img, bg_img):
        self.segmentation = Segmentation()
        self.preprocess = Preprocess()
        self.cartoonify = Cartoonify()
        self.origin_img = ori_img
        self.mask_img = None
        self.bg_img = bg_img
        self.result_img = None


    def convert(self):

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
        res_img = self.segmentation.segment(self.origin_img)
        return res_img
