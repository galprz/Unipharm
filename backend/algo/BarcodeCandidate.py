import numpy as np
import imutils
import cv2
# pylint: disable = unsubscriptable-object


class PossibleBarcode(object):

    def __init__(self, contour, image):
        self.image = image
        self.contour = contour
        rect = cv2.minAreaRect(contour)
        box = cv2.cv.BoxPoints(
            rect) if imutils.is_cv2() else cv2.boxPoints(rect)
        box = np.int0(box)
        self.min_y = int(np.min(box[:, -1]))
        self.max_y = int(np.max(box[:, -1]))
        self.min_x = int(np.min(box[:, 0]))
        self.max_x = int(np.max(box[:, 0]))
        self.box = box

    def minX(self):
        return self.min_x

    def minY(self):
        return self.min_y

    def maxX(self):
        return self.max_x

    def maxY(self):
        return self.max_y

    def extractToImage(self):
        return self.image[self.min_y:self.max_y, self.min_x:self.max_x]

    def getBox(self):
        return self.box
