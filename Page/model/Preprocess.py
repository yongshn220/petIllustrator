import cv2
import sys
import numpy as np
import binascii
import struct
import scipy
import scipy.misc
import scipy.cluster

class Preprocess:
    def mask_img(self, o_img, m_img, b_img = None):
        if not b_img:
            b_img = np.zeros([512,512,3],dtype=np.uint8)
            # b_img.fill(255)
            b_img[:] = self.getAppropriateColor(o_img)
            #b_img = cv2.imread('Page\images\Background\single1.jpg', cv2.IMREAD_COLOR)  
        p_origin_img = self.resize_img(o_img)
        p_mask_img = self.resize_img(m_img)
        p_background_img = self.resize_img(b_img)
        r, p_mask_image = cv2.threshold(p_mask_img, 168, 255, cv2.THRESH_BINARY)
        result_image = cv2.copyTo(p_origin_img, p_mask_image, p_background_img)
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

    
    # return most frequently used color from the following image.
    def getAppropriateColor(self, img, numOfCluster=5):    
        img = cv2.resize(img, dsize=(640, 640), interpolation=cv2.INTER_AREA)      # optional, to reduce time
        # ar = np.asarray(img)
        shape = img.shape
        ar = img.reshape(scipy.product(shape[:2]), shape[2]).astype(float)
        

        codes, dist = scipy.cluster.vq.kmeans(ar, numOfCluster)

        vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
        counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

        index_max = scipy.argmax(counts)                    # find most frequent
        peak = codes[index_max]
        color = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
        return peak
    