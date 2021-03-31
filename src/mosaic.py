import cv2 as cv
import numpy as np
import random as rng


class Mosaic():
    def __init__(self, canvasUpdate, img = None):
        self.img = img
        self.canvasUpdate = canvasUpdate
        self.settings = {
            "K": 4,
            "Area": 4,
            "LineThickness": 2
        }
        self.mosaics = {}
        self.contours = {}

    def setImage(self, img):
        self.img = img
        self.mosaics = {}
        self.update()

    def set(self, setting, value):
        self.settings[setting] = value
        self.update()

    def get(self, str):
        return self.settings[str]

    def update(self):
        mosaic = self.drawKMeansContours()

        #self.mosaic = mosaic
        self.canvasUpdate(mosaic)


    def drawMoments(self, mosaic=None):
        if mosaic is None:
            mosaic = self.img
        threshold = self.settings["K"]*10
        rng.seed(12345)

        src_gray = cv.cvtColor(mosaic, cv.COLOR_BGR2GRAY)
        src_gray = cv.blur(src_gray, (3,3))

        canny_output = cv.Canny(src_gray, threshold, threshold * 2)
        contours, _ = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # Get the moments
        mu = [None]*len(contours)
        for i in range(len(contours)):
            mu[i] = cv.moments(contours[i])

        drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

        for i in range(len(contours)):
            areaThreshold = self.settings["Area"]*5
            if cv.contourArea(contours[i]) > areaThreshold:
                color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
                cv.drawContours(drawing, contours, i, color, -1)

        return drawing


    def drawKMeans(self, mosaic=None):
        if mosaic is None:
            mosaic = self.img
        K = self.settings["K"]

        # reshape the image to a 2D array of pixels and 3 color values (RGB)
        pixel_values = mosaic.reshape((-1, 3))
        # convert to float
        pixel_values = np.float32(pixel_values)

        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, (centers) = cv.kmeans(pixel_values, K, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

        # convert back to 8 bit values
        centers = np.uint8(centers)

        # flatten the labels array
        labels = labels.flatten()

        # convert all pixels to the color of the centroids
        segmented_image = centers[labels.flatten()]

        # reshape back to the original image dimension
        mosaic = segmented_image.reshape(mosaic.shape)

        return mosaic


    def drawKMeansContours(self):
        settingHash = hash(frozenset(self.settings.items()))
        if settingHash in self.mosaics:
            return self.mosaics[settingHash]

        mosaic = self.img
        imgHSV = cv.cvtColor(mosaic, cv.COLOR_BGR2HSV)
        areaThreshold = int(self.settings["Area"] *0.001 * self.img.shape[0]*self.img.shape[1])

        mosaic = cv.blur(mosaic, (5,5))

        # reshape the image to a 2D array of pixels and 3 color values (RGB)
        pixel_values = mosaic.reshape((-1, 3))
        pixel_values = np.float32(pixel_values)

        # Splits the image into k groups of related colours
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, (centers) = cv.kmeans(pixel_values, self.settings["K"], None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

        # convert back to 8 bit values, and
        # flatten the labels array
        centers = np.uint8(centers)
        labels = labels.flatten()

        # The contours are collected for each colour region
        fullContours = []
        for i in range(self.settings["K"]):
            arr = np.zeros(centers.shape[0])
            arr[i] = 255
            arr = np.uint8(arr)

            segmented_image = arr[labels.flatten()].reshape((mosaic.shape[0], mosaic.shape[1]))
            segmented_image = np.uint8(segmented_image)

            contours, hierarchy = cv.findContours(segmented_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            fullContours = fullContours + contours

        # Fills the contours with their representative colour
        drawing = np.zeros((mosaic.shape[0], mosaic.shape[1], 3), dtype=np.uint8)
        for cnt in fullContours:
            if cv.contourArea(cnt) > areaThreshold:
                color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))

                mask = np.zeros((mosaic.shape[0], mosaic.shape[1]), np.uint8)
                cv.drawContours(mask, cnt, -1, 255, -1)
                mean = cv.mean(self.img, mask=mask)

                cv.drawContours(drawing, [cnt], 0, mean, -2, cv.LINE_8, hierarchy, 0)

        # Draws the outline of the contours
        for cnt in fullContours:
            if cv.contourArea(cnt) > areaThreshold:
                cv.drawContours(drawing, [cnt], 0, (0,0,0), self.settings["LineThickness"], cv.LINE_8, hierarchy, 0)


        self.mosaics[settingHash] = drawing
        return drawing


    def drawFast(self, mosaic=None):
        if mosaic is None:
            mosaic = self.img

        # Initiate FAST object with default values
        fast = cv.FastFeatureDetector_create()
        # find and draw the keypoints
        kp = fast.detect(mosaic, None)
        mosaic = cv.drawKeypoints(mosaic, kp, None, color=(255,0,0))
        return mosaic


    def drawContours(self, mosaic=None):
        if mosaic is None:
            mosaic = self.img

        threshold = self.settings["K"]*10
        rng.seed(12345)

        src_gray = cv.cvtColor(mosaic, cv.COLOR_BGR2GRAY)
        src_gray = cv.blur(src_gray, (3,3))

        # Detect edges using Canny
        canny_output = cv.Canny(src_gray, threshold, threshold * 2)
        # Find contours
        contours, hierarchy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # Draw contours
        drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
        for i in range(len(contours)):
            color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
            cv.drawContours(drawing, contours, i, color, 2, cv.LINE_8, hierarchy, 0)

        return drawing
