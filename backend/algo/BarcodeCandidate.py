import numpy as np
import imutils
import cv2
# pylint: disable = unsubscriptable-object


class BarcodeCandidate(object):

    def __init__(self, contour, image, expansion_factor=100):
        self.image = image
        rect = cv2.minAreaRect(contour)
        box = cv2.cv.BoxPoints(
            rect) if imutils.is_cv2() else cv2.boxPoints(rect)
        box = np.int0(box)
        self.__min_y = int(np.min(box[:, -1]))
        self.__max_y = int(np.max(box[:, -1]))
        self.__min_x = int(np.min(box[:, 0]))
        self.__max_x = int(np.max(box[:, 0]))
        self.__expansion_factor = expansion_factor

    def get_min_x(self, _expanded=False):
        return self.__min_x if not _expanded else max(0, self.__min_x-self.__expansion_factor)

    def get_min_y(self, _expanded=False):
        return self.__min_y if not _expanded else max(0, self.__min_y-self.__expansion_factor)

    def get_max_x(self, _expanded=False):
        return self.__max_x if not _expanded else min(self.image.shape[1], self.__max_x+self.__expansion_factor)

    def get_max_y(self, _expanded=False):
        return self.__max_y if not _expanded else min(self.image.shape[0], self.__max_y+self.__expansion_factor)

    def extract_to_image(self):
        return self.image[self.get_min_y(_expanded=True):self.get_max_y(_expanded=True), self.get_min_x(_expanded=True):self.get_max_x(_expanded=True)]

    def get_top_left(self, _expanded=False):
        return (self.get_min_x(_expanded), self.get_min_y(_expanded))

    def get_bottom_right(self, _expanded=False):
        return (self.get_max_x(_expanded), self.get_max_y(_expanded))
