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

    def load_image(self, imagePath):
        self.origImage = cv2.imread(imagePath)
        self.tempImage = self.ipp.load_image(
            imagePath).to_grayscale().process_grayscale().get_image()
        return self

    def get_largest_contours(self, numContours=4):
        cnts = cv2.findContours(self.tempImage.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        self.tempResArr = sorted(cnts, key=cv2.contourArea, reverse=True)
        top = min(numContours, len(self.tempResArr))
        self.tempResArr = self.tempResArr[:top]
        return self

    def to_barcode_objects(self):
        self.tempResArr = [PossibleBarcode(
            x, self.origImage) for x in self.tempResArr]
        return self

    def display_detected_barcodes(self):
        for b in self.tempResArr:
            cv2.drawContours(self.origImage, [b.getBox()], -1, (0, 255, 0), 3)
        cv2.imshow("Image", self.origImage)
        cv2.waitKey(0)

    def save_in_single_file(self):
        for b in self.tempResArr:
            cv2.drawContours(self.origImage, [b.getBox()], -1, (0, 255, 0), 3)
        cv2.imwrite("DetectedBarcodes.jpg", self.origImage)

    def save_in_seperate_files(self):
        count = 0
        for b in self.tempResArr:
            cv2.imwrite('crop_{}.jpg'.format(count), b.extract_to_image())
            count += 1

    def get_all_results(self):
        return self.tempResArr
