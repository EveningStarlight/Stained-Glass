import cv2 as cv
import numpy as np
import random as rng


class Mosaic():
    def __init__(self, canvasUpdate, img = None):
        self.img = img
        self.canvasUpdate = canvasUpdate
        self.settings = {
            "K": 3,
            "Grid": 2,
            "BlurSize": 9,
            "MinArea": 0.2,
            "LineThickness": 2,
            "Saturation": 1.0,
            "Lightness": 1.0,
            "colorScheme": 0
        }
        self.mosaics = {}
        self.contours = {}
        self.colorSchemes = ['original', 'pop', 'random']


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
            contours = self.getKMeansContours(images=None)
            mosaic = self.drawKMeansContours(contours)

        self.mosaics[settingHash] = mosaic
        self.canvasUpdate(mosaic)


    def getSettingHash(self):
        return hash(frozenset(self.settings.items()))


    def getContourHash(self):
        contourSettings = ('K', 'Grid', 'BlurSize')
        contourDic = {key:self.settings[key] for key in contourSettings if key in self.settings}
        contourHash = hash(frozenset(contourDic.items()))

        return contourHash


    def getKMeansContours(self, images):
        fullContours = []
        size = self.settings['Grid']
        height = int(self.img.shape[0]/size)
        length = int(self.img.shape[1]/size)

        for row in range(size):
            for col in range(size):
                mosaic = self.img[row*height:(row+1)*height,col*length:(col+1)*length]
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
                for i in range(self.settings["K"]):
                    arr = np.zeros(centers.shape[0])
                    arr[i] = 255
                    arr = np.uint8(arr)

                    segmented_image = arr[labels.flatten()].reshape((mosaic.shape[0], mosaic.shape[1]))
                    segmented_image = np.uint8(segmented_image)

                    contours, hierarchy = cv.findContours(segmented_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

                    for cnt in contours:
                        cnt[:,0,0] = cnt[:,0,0] + col*length
                        cnt[:,0,1] = cnt[:,0,1] + row*height
                    fullContours = fullContours + contours


        contourHash = self.getContourHash()
        self.contours[contourHash] = fullContours
        return fullContours


    def drawKMeansContours(self, allContours):
        mosaic = self.img
        squares = self.settings["Grid"] * self.settings["Grid"]
        minArea = int(self.settings["MinArea"]/100 * self.img.shape[0]*self.img.shape[1] / squares)

        contours = []
        i = 0
        while i<len(allContours):
            cnt = allContours[i]
            area = cv.contourArea(cnt)

            if area > minArea:
                contours.append(cnt)

            i+=1

        mean = np.array(cv.mean(mosaic))
        mean[1] = min(mean[1]*self.settings["Saturation"], 255)
        mean[2] = min(mean[2]*self.settings["Lightness"], 255)

        # Fills the contours with their representative colour
        drawing = np.full((mosaic.shape[0], mosaic.shape[1], 3), mean[:3], dtype=np.uint8)
        for cnt in contours:

            schemeNum = self.settings["colorScheme"]
            if self.colorSchemes[schemeNum] == 'random':
                seed = hash(tuple(cnt.flatten()))
                rng.seed(seed)
                color = (rng.randint(0,256), rng.randint(156,256), rng.randint(156,256))
                mean = np.full((1, 1, 3), color[:3], dtype=np.uint8)
            else:
                # Defines the Mask for selecting average colour
                mask = np.zeros((mosaic.shape[0], mosaic.shape[1]), np.uint8)
                cv.drawContours(mask, [cnt], -1, 255, -1)

                # Erodes the mask so that edge colours do not
                # Interfere with the main colour of the region
                kernel = np.ones((5,5),np.uint8)
                mask = cv.erode(mask, kernel, iterations=1)

                mean = np.array(cv.mean(mosaic, mask=mask))
                mean = np.full((1, 1, 3), mean[:3], dtype=np.uint8)
                mean = cv.cvtColor(mean, cv.COLOR_RGB2HSV)

            mean[0,0,1] = min(mean[0,0,1]*self.settings["Saturation"], 255)
            mean[0,0,2] = min(mean[0,0,2]*self.settings["Lightness"], 255)

            if self.colorSchemes[schemeNum] == 'original':
                mean = cv.cvtColor(mean, cv.COLOR_HSV2RGB)
            elif self.colorSchemes[schemeNum] == 'pop':
                pass
            elif self.colorSchemes[schemeNum] == 'random':
                mean = cv.cvtColor(mean, cv.COLOR_HSV2RGB)
            color = (int(mean[0,0,0]), int(mean[0,0,1]), int(mean[0,0,2]))

            cv.drawContours(drawing, [cnt], 0, color, -2, cv.LINE_8)

        # Draws the outline of the contours
        for cnt in contours:
            cv.drawContours(drawing, [cnt], 0, (20,20,20), self.settings["LineThickness"], cv.LINE_8)
        cv.rectangle(drawing, (0,0), (self.img.shape[1],self.img.shape[0]), (20,20,20), self.settings["LineThickness"], cv.LINE_8)


        return drawing
