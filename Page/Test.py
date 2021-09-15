from main import Main
import cv2
import numpy as np

test = Main()

origin_img = cv2.imread('Page\images\Raw\dog.jpg', cv2.IMREAD_COLOR)

result_img = test.convert(origin_img)

cv2.imshow("Result", result_img)
cv2.waitKey(0)