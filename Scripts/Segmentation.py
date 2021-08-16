from torchvision import models
from PIL import Image
import matplotlib.pyplot as plt
import torch
import torchvision.transforms as T
import numpy as np
import cv2



class Segmentation:
    def __init__(self, img):
        self.dlab = models.segmentation.deeplabv3_resnet101(pretrained=True).eval()
        self.img = img

    def segment(self):
        self.process(self.dlab, self.img, show_orig=False)


    def process(self, net, path, show_orig=True, dev='cuda'):
        img = Image.open(path)

        if show_orig:
            plt.imshow(img)
            plt.axis('off')
            plt.show()

        trf = T.Compose(
            [T.Resize(640), T.ToTensor(), T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

        inp = trf(img).unsqueeze(0).to(dev)
        out = net.to(dev)(inp)['out']
        om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
        result_img = self.decode_segmap(om)
        return result_img
        # plt.imshow(rgb)
        # plt.axis('off')
        # plt.show()
        # save_image(rgb)

    def decode_segmap(self, image, nc=21):
        label_colors = np.array([(0, 0, 0),  # 0=background
                                 # 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
                                 (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                                 # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
                                 (0, 0, 0), (0, 0, 0), (255, 255, 255), (0, 0, 0), (0, 0, 0),
                                 # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
                                 (0, 0, 0), (255, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                                 # 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor
                                 (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)])

        r = np.zeros_like(image).astype(np.uint8)
        g = np.zeros_like(image).astype(np.uint8)
        b = np.zeros_like(image).astype(np.uint8)

        for i in range(0, nc):
            idx = image == i
            r[idx] = label_colors[i, 0]
            g[idx] = label_colors[i, 1]
            b[idx] = label_colors[i, 2]

        rgb = np.stack([r, g, b], axis=2)
        return rgb

