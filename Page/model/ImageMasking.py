import cv2
import torch
import torchvision.transforms as T
from PIL import Image




source_image_path = '../Images/Raw/dog.jpg'
mask_image_path = "../Images/Mask/DogMask.jpg"
dest_image_path = "../Images/Background/Background.jpg"




source_image = cv2.imread(source_image_path, cv2.IMREAD_COLOR)
mask_image = cv2.imread(mask_image_path, cv2.IMREAD_GRAYSCALE)
dest_image = cv2.imread(dest_image_path, cv2.IMREAD_COLOR)

p_source_image = cv2.resize(source_image, dsize=(640, 640), interpolation=cv2.INTER_AREA)

p_mask_image = cv2.resize(mask_image, dsize=(640,640), interpolation=cv2.INTER_AREA)

r, p_mask_image = cv2.threshold(p_mask_image, 168, 255, cv2.THRESH_BINARY)

p_dest_image = cv2.resize(dest_image, dsize=(640, 640), interpolation=cv2.INTER_AREA)


final_image = cv2.copyTo(p_source_image, p_mask_image)

cv2.imshow('FinalImage', final_image)
cv2.waitKey()
