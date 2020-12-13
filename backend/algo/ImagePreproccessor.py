import cv2
import imutils


class ImagePreproccessor(object):
    def __init__(self):
        self.image = None

    def loadImage(self, imagePath):
        self.image = cv2.imread(imagePath)
        return self

    def toGrayscale(self):
        if self.image is not None:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            return self

    def Scharr(self):
        if self.image is not None:
            gray = self.image
            ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
            gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
            gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

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
            self.image = cv2.dilate(closed, None, iterations=4)
            return self

    def get(self):
        return self.image
