import numpy as np
import imutils
import cv2
# pylint: disable = unsubscriptable-object


class PossibleBarcode(object):
    expansionFactor = 100

    def __init__(self, contour, image):
        self.image = image
        self.contour = contour
        rect = cv2.minAreaRect(contour)
        box = cv2.cv.BoxPoints(
            rect) if imutils.is_cv2() else cv2.boxPoints(rect)
        box = np.int0(box)
        self.min_y = max(0, int(np.min(box[:, -1])) - 0)
        self.max_y = int(np.max(box[:, -1])) + 0
        self.min_x = max(0, int(np.min(box[:, 0])) - 0)
        self.max_x = int(np.max(box[:, 0])) + 0
        self.box = box

    def get_min_x(self, _expanded=False):
        return self.min_x if not _expanded else max(0, self.min_x-PossibleBarcode.expansionFactor)

    def get_min_y(self, _expanded=False):
        return self.min_y if not _expanded else max(0, self.min_y-PossibleBarcode.expansionFactor)

    def get_max_x(self, _expanded=False):
        return self.max_x if not _expanded else min(self.image.shape[1], self.max_x+PossibleBarcode.expansionFactor)

    def get_max_y(self, _expanded=False):
        return self.max_y if not _expanded else min(self.image.shape[0], self.max_y+PossibleBarcode.expansionFactor)

    def extract_to_image(self):
        return self.image[self.get_min_y(_expanded=True):self.get_max_y(_expanded=True), self.get_min_x(_expanded=True):self.get_max_x(_expanded=True)]

    def get_box(self):
        return self.box

    def get_top_left(self, _expanded=False):
        return (self.get_min_x(_expanded), self.get_min_y(_expanded))

    def get_bottom_right(self, _expanded=False):
        return (self.get_max_x(_expanded), self.get_max_y(_expanded))
