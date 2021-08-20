import cv2
import numpy as np



class Cartoonify:
    def __init__(self):
        self.img = None
        self.blur = 2


    def k_mean_method(self, image, clusters, rounds):
        height, width = image.shape[:2]
        samples = np.zeros([height * width, 3], dtype=np.float32)

        count = 0
        for x in range(height):

            for y in range(width):
                samples[count] = image[x][y]
                count += 1

        compactness, labels, centers = cv2.kmeans(
            samples,
            clusters,
            None,
            criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,10000,0.0001),
            attempts=rounds,
            flags=cv2.KMEANS_PP_CENTERS
        )

        centers = np.uint8(centers)
        res = centers[labels.flatten()]

        result_img = res.reshape(image.shape)

        result_img = cv2.GaussianBlur(result_img, (9, 9), 0)
        return result_img


    def contour_image(self, img):

        blue, green, red = cv2.split(img)

        contours, hierarchy = cv2.findContours(image=img, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        cnt = contours[0]
        cv2.drawContours(img, [cnt], 0, (0, 255, 0), 3)
        return img


    def cartoon_method(self, img):
        edge_img = self.detect_edge(img)
        color = cv2.bilateralFilter(img, 9, 250, 250)
        cartoon_img = cv2.bitwise_and(color, color, mask=edge_img)
        return cartoon_img


    def canny_method(self, img):

        edge_img = self.process_image(img, 2)
        edge_img = self.white_to_transparent(edge_img)

        k_mean_img = self.k_mean_method(img, 16, 1)

        added_img = self.overlay_transparent(k_mean_img, edge_img, 0, 0)

        contour_img = self.process_image(added_img, 1)
        contour_img = self.white_to_transparent(contour_img)

        result_img = self.overlay_transparent(added_img, contour_img, 0, 0)
        # result_img = self.contour_image(result_img)

        vivid_img = self.vivid_image(added_img)
        return vivid_img



    def detect_edge(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        return edges


    def process_image(self, img, blur):
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        if blur == 2:
            gray = cv2.GaussianBlur(gray, (9, 9), 0)
            canny = cv2.Canny(gray, 50, 100)

        elif blur == 1:
            gray = cv2.GaussianBlur(gray, (9, 9), 0)
            canny = cv2.Canny(gray, 100, 400)
            kernel = np.ones((5, 5), np.uint8)
            canny = cv2.dilate(canny, kernel, iterations=1)
        else:
            canny = cv2.Canny(gray, 50, 75)

        # canny = self.rescale(canny, self.pseudoDim)


        r, dil_img = cv2.threshold(canny, 50, 255, cv2.THRESH_BINARY_INV)

        result_img = cv2.cvtColor(dil_img, cv2.COLOR_GRAY2BGR)
        return result_img


    def vivid_image(self, img):

        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=5., tileGridSize=(3, 3
                                                            ))

        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
        l, a, b = cv2.split(lab)  # split on 3 different channels

        l2 = clahe.apply(l)  # apply CLAHE to the L-channel

        lab = cv2.merge((l2, a, b))  # merge channels
        result_img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR

        return result_img



    def overlay_transparent(self, background_img, img_to_overlay_t, x, y, overlay_size=None):
        """
        @brief      Overlays a transparant PNG onto another image using CV2

        @param      background_img    The background image
        @param      img_to_overlay_t  The transparent image to overlay (has alpha channel)
        @param      x                 x location to place the top-left corner of our overlay
        @param      y                 y location to place the top-left corner of our overlay
        @param      overlay_size      The size to scale our overlay to (tuple), no scaling if None

        @return     Background image with overlay on top
        """

        bg_img = background_img.copy()

        if overlay_size is not None:
            img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

        # Extract the alpha mask of the RGBA image, convert to RGB
        b, g, r, a = cv2.split(img_to_overlay_t)
        overlay_color = cv2.merge((b, g, r))

        # Apply some simple filtering to remove edge noise
        mask = cv2.medianBlur(a, 1)

        h, w, _ = overlay_color.shape
        roi = bg_img[y:y + h, x:x + w]

        # Black-out the area behind the logo in our original ROI
        img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))

        # Mask out the logo from the logo image.
        img2_fg = cv2.bitwise_and(overlay_color, overlay_color, mask=mask)

        # Update the original image with our new ROI
        bg_img[y:y + h, x:x + w] = cv2.add(img1_bg, img2_fg)

        return bg_img

    def overlay_image(self, img1, img2):
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2BGRA)
        print(img1.shape)
        print(img2.shape)
        ol_img = cv2.addWeighted(img1, 1, img2, 0.5, 0)
        return ol_img

    def white_to_transparent(self, img):

        # get the image dimensions (height, width and channels)

        h, w, c = img.shape

        # append Alpha channel -- required for BGRA (Blue, Green, Red, Alpha)
        alpha_img = np.concatenate([img, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)

        # create a mask where white pixels ([255, 255, 255]) are True
        white = np.all(img == [255, 255, 255], axis=-1)

        # change the values of Alpha to 0 for all the white pixels
        alpha_img[white, -1] = 0

        # save the image
        return alpha_img