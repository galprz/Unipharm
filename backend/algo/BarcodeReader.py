import cv2
from pyzbar import pyzbar
import BarcodeDetector


def drawBarcodeResOnImage(image, barcode, bartype, data):
    image_ = image
    image_ = cv2.rectangle(image, (barcode.minX(), barcode.minY(
    )), (barcode.maxX(), barcode.maxY()), (0, 0, 255), 2)
    text = "{} ({})".format(data, bartype)
    cv2.putText(image_, text, (barcode.minX(), barcode.minY() - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return image_


def readBarcodesFromImage(imagePath):
    x = BarcodeDetector.BarcodeDetector().loadImage(
        imagePath).getLargestContours(4).toBarcodeObjects().get()
    final_barcodes = []
    for r in x:
        image = r.extractToImage()
        barcodes = pyzbar.decode(image)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # the barcode data is a bytes object so if we want to draw it on
            # our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)
            # print the barcode type and data to the terminal
            print("[INFO] Found {} barcode: {}".format(
                barcodeType, barcodeData))
            final_barcodes.append((r, barcodeType, barcodeData))
        # show the output image
    if len(final_barcodes) > 0:
        f_image = cv2.imread(imagePath)
        for barcode in final_barcodes:
            f_image = drawBarcodeResOnImage(f_image, *barcode)
        cv2.waitKey(0)
        cv2.imwrite("result.jpg", f_image)
