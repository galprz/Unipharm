import cv2
import imutils
from BarcodeCandidate import PossibleBarcode
import ImagePreproccessor


class BarcodeDetector(object):
    def __init__(self):
        self.origImage = None
        self.tempImage = None
        self.ipp = ImagePreproccessor.ImagePreproccessor()
        self.tempResArr = None

    def loadImage(self, imagePath):
        self.origImage = cv2.imread(imagePath)
        self.tempImage = self.ipp.loadImage(
            imagePath).toGrayscale().Scharr().get()
        return self

    def getLargestContours(self, numContours=4):
        cnts = cv2.findContours(self.tempImage.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        self.tempResArr = sorted(cnts, key=cv2.contourArea, reverse=True)
        top = min(numContours, len(self.tempResArr))
        self.tempResArr = self.tempResArr[:top]
        return self

    def toBarcodeObjects(self):
        self.tempResArr = [PossibleBarcode(
            x, self.origImage) for x in self.tempResArr]
        return self

    def display(self):
        for b in self.tempResArr:
            cv2.drawContours(self.origImage, [b.getBox()], -1, (0, 255, 0), 3)
        cv2.imshow("Image", self.origImage)
        cv2.waitKey(0)

    def save(self):
        for b in self.tempResArr:
            cv2.drawContours(self.origImage, [b.getBox()], -1, (0, 255, 0), 3)
        cv2.imwrite("DetectedBarcodes.jpg", self.origImage)

    def saveCrops(self):
        count = 0
        for b in self.tempResArr:
            cv2.imwrite('crop_{}.jpg'.format(count), b.extractToImage())
            count += 1

    def get(self):
        return self.tempResArr
