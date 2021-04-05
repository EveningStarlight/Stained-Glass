import cv2 as cv
import numpy as np
import random as rng


class Mosaic():
    def __init__(self, canvasUpdate, img = None):
        self.img = img
        self.canvasUpdate = canvasUpdate
        self.settings = {
            "K": 4,
            "BlurSize": 9,
            "MinArea": 0.2,
            "MaxArea": 100,
            "LineThickness": 2,
            "Saturation": 1.0,
            "Lightness": 1.0
        }
        self.mosaics = {}
        self.contours = {}


    def setImage(self, img):
        self.img = img
        self.mosaics = {}
        self.contours = {}
        self.update()


    def set(self, setting, value):
        self.settings[setting] = value
        self.update()


    def get(self, str):
        return self.settings[str]


    def update(self):
        settingHash = self.getSettingHash()
        contourHash = self.getContourHash()

        if settingHash in self.mosaics:
            mosaic = self.mosaics[settingHash]
        elif contourHash in self.contours:
            contours = self.contours[contourHash]
            mosaic = self.drawKMeansContours(contours)
        else:
            contours = self.getKMeansContours()
            mosaic = self.drawKMeansContours(contours)

        self.mosaics[settingHash] = mosaic
        self.canvasUpdate(mosaic)


    def getSettingHash(self):
        return hash(frozenset(self.settings.items()))


    def getContourHash(self):
        contourSettings = ('K', 'BlurSize')
        contourDic = {k:self.settings[k] for k in contourSettings if k in self.settings}
        contourHash = hash(frozenset(contourDic.items()))

        return contourHash


    def getKMeansContours(self):
        mosaic = self.img
        mosaic = cv.blur(mosaic, (self.settings["BlurSize"],self.settings["BlurSize"]))

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


        contourHash = self.getContourHash()
        self.contours[contourHash] = fullContours
        return fullContours


    def drawKMeansContours(self, allContours):
        mosaic = self.img
        minArea = int(self.settings["MinArea"]/100 * self.img.shape[0]*self.img.shape[1])
        maxArea = int(self.settings["MaxArea"]/100 * self.img.shape[0]*self.img.shape[1])
        imgHSV = cv.cvtColor(mosaic, cv.COLOR_RGB2HSV)

        contours = []
        i = 0
        while i<len(allContours):
            cnt = allContours[i]
            area = cv.contourArea(cnt)

            if area > maxArea:
                pass
            elif area > minArea:
                contours.append(cnt)

            i+=1

        # Fills the contours with their representative colour
        drawing = np.zeros((mosaic.shape[0], mosaic.shape[1], 3), dtype=np.uint8)
        for cnt in contours:
            color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))

            mask = np.zeros((mosaic.shape[0], mosaic.shape[1]), np.uint8)
            cv.drawContours(mask, cnt, -1, 255, -1)
            mean = np.array(cv.mean(imgHSV, mask=mask))

            mean[1] = min(mean[1]*self.settings["Saturation"], 255)
            mean[2] = min(mean[2]*self.settings["Lightness"], 255)

            cv.drawContours(drawing, [cnt], 0, mean, -2, cv.LINE_8)

        drawing = cv.cvtColor(drawing, cv.COLOR_HSV2RGB)

        # Draws the outline of the contours
        for cnt in contours:
            cv.drawContours(drawing, [cnt], 0, (0,0,0), self.settings["LineThickness"], cv.LINE_8)

        return drawing
