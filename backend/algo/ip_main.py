from pyzbar import pyzbar
import cv2
import imutils
import numpy as np
from pyzbar.pyzbar import ZBarSymbol
SUPPORTED_BARCODE_TYPES = [ZBarSymbol.CODABAR, ZBarSymbol.CODE128, ZBarSymbol.CODE39, ZBarSymbol.CODE93, ZBarSymbol.COMPOSITE, ZBarSymbol.DATABAR, ZBarSymbol.DATABAR_EXP, ZBarSymbol.EAN13,
                           ZBarSymbol.EAN2, ZBarSymbol.EAN5, ZBarSymbol.EAN8, ZBarSymbol.I25, ZBarSymbol.ISBN10, ZBarSymbol.ISBN13, ZBarSymbol.NONE, ZBarSymbol.PARTIAL, ZBarSymbol.QRCODE, ZBarSymbol.UPCA, ZBarSymbol.UPCE]


def analyze(path, is_video=True, video_params=None):
    # Load Video or Image to cv2
    if is_video:
        images = parse_video(path)
    else:
        images = cv2.imread(path)
    results = []
    for index, image in enumerate(images):
        results.append((index, process_image(image)))
    return results


def parse_video(path, video_params):
    videoCapture = cv2.VideoCapture(path)
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    frame_count = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
    success, frame = videoCapture.read()
    duration = frame_count / fps
    count = 0
    resultFrames = []
    while success:
        if count >= 0 and count <= duration*fps and count % 9 == 0:
            resultFrames.append(frame)
        count += 1
        success, frame = videoCapture.read()

    return resultFrames


def process_image(image):
    b_image = image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
    gradX = cv2.Sobel(image, ddepth=ddepth, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(image, ddepth=ddepth, dx=0, dy=1, ksize=-1)

    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    # blur and threshold the image
    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

    # construct a closing kernel and apply it to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=4)
    image = cv2.dilate(closed, None, iterations=4)
    cnts = cv2.findContours(image, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    tempResArr = sorted(cnts, key=cv2.contourArea, reverse=True)
    top = min(5, len(tempResArr))
    tempResArr = tempResArr[:top]
    tempResArr = [BarcodeCandidate(
        x, b_image) for x in tempResArr]
    final_barcodes = []
    for barcode_candidate in tempResArr:
        image = barcode_candidate.extract_to_image()
        barcodes = pyzbar.decode(
            image, symbols=SUPPORTED_BARCODE_TYPES)
        for decoded_barcode in barcodes:
            final_barcodes.append(DecodedBarcode(
                barcode_candidate,
                decoded_barcode))
    return final_barcodes


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


class DecodedBarcode(object):
    def __init__(self, barcode_candidate: BarcodeCandidate, pyzbarDecoded: pyzbar.Decoded):
        self.data = pyzbarDecoded.data.decode("utf-8")
        self.type = pyzbarDecoded.type
        self.barcode = barcode_candidate

    def get_barcode_top_left_corner(self) -> tuple:
        return self.barcode.get_top_left()

    def get_barcode_bottom_right_corner(self) -> tuple:
        return self.barcode.get_bottom_right()

    def descriptive_tuple(self):
        return (self.data, self.type)
