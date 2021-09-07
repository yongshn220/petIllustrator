import cv2
import sys

class Preprocess:
    def mask_img(self, o_img, m_img, b_img):
        p_origin_img = self.resize_img(o_img)
        p_mask_img = self.resize_img(m_img)
        p_background_img = self.resize_img(b_img)
        r, p_mask_image = cv2.threshold(p_mask_img, 168, 255, cv2.THRESH_BINARY)
        result_image = cv2.copyTo(p_origin_img, p_mask_image,p_background_img)
        return result_image


    def mask_transparent(self, img):
        result_image = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        result_image[:, :, 3] = img
        return result_image


    def resize_img(self, img):
        resize_img = ''

        try:
            new_img = cv2.resize(img, dsize=(640, 640), interpolation=cv2.INTER_AREA)
            resize_img = new_img
        except: return

        return resize_img


    def subtrack_img(self, o_img, m_img):
        result_img = cv2.subtract(o_img, m_img)
        return result_img