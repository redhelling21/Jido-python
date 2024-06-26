from threading import Thread, Event
import numpy as np
import time
import mouse
import cv2
from PIL import ImageGrab


class AutoLootThread(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.stop = False
        self.autoloot = Event()
        self.blank = np.zeros((5, 5, 3), np.uint8)
        self.currentlyRunning = False
        self.last_mask = self.blank
        self.lootExpedition = 0
        self.last_clicked_position = (0, 0)
        self.lootBreach = 0
        self.lootLegion = 0
        self.lootHeist = 0
        self.lootBlight = 0

    def run(self):
        while not self.stop:
            if self.autoloot.wait(1) and self.currentlyRunning is False:
                cXList = []
                cYList = []
                img = np.array(ImageGrab.grab())
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                mask = cv2.inRange(img, (253, 0, 253), (255, 20, 255))
                if self.lootExpedition == 1:
                    mask = mask | cv2.inRange(img, (252, 175, 113), (255, 180, 117))
                if self.lootBlight == 1:
                    mask = mask | cv2.inRange(img, (0, 203, 253), (1, 205, 255))
                if self.lootLegion == 1:
                    mask = mask | cv2.inRange(img, (254, 254, 254), (255, 255, 255))
                if self.lootBreach == 1:
                    mask = mask | cv2.inRange(img, (0, 0, 174), (1, 1, 176))
                if self.lootHeist == 1:
                    mask = mask | cv2.inRange(img, (21, 21, 172), (23, 23, 174))
                error = self.mse(mask, self.last_mask)

                self.last_mask = mask
                if error > 0:
                    time.sleep(0.1)
                    continue
                # cv2.imwrite("mask.png", mask)
                # dilate?
                contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                foundThingToClick = False
                for contour in contours:
                    if cv2.contourArea(contour) < 100:
                        continue
                    approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
                    if len(approx) >= 4 and len(approx) <= 50:
                        foundThingToClick = True

                        # find center of the loot
                        M = cv2.moments(contour)
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        # scale cX and cY by image scale
                        cXList.append(cX)
                        cYList.append(cY)
                        break
                if foundThingToClick:
                    vector = self.extrapolate(cXList, cYList, 1.1)
                    predictedPoint = cXList[len(cXList) - 1] + vector[0], cYList[len(cYList) - 1] + vector[1]
                    if self.last_clicked_position[0] == predictedPoint[0] and self.last_clicked_position[1] == predictedPoint[1]:
                        continue
                    mouse.move(int(predictedPoint[0]), int(predictedPoint[1]))
                    self.last_clicked_position = (int(predictedPoint[0]), int(predictedPoint[1]))
                    self.leftClick()
                    time.sleep(0.1)
                else:
                    time.sleep(0.3)
            else:
                self.last_mask = self.blank
                time.sleep(1)

    def join(self, timeout=None):
        self.stop = True
        super().join(timeout)

    def extrapolate(self, xVals, yVals, lagCompensation=1.0):
        if len(xVals) < 2 or len(yVals) < 2:
            return (0, 0)

        slope = (xVals[1] - xVals[0]) * lagCompensation, (yVals[1] - yVals[0]) * lagCompensation
        return slope

    def leftClick(self, sleep=0.005):
        time.sleep(sleep)
        mouse.press()
        time.sleep(sleep)
        mouse.release()

    def mse(self, img1, img2):
        h, w = img1.shape
        if img1.shape != img2.shape:
            return 1000
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff**2)
        mse = err / (float(h * w))
        return mse
