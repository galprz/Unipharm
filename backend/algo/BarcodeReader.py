import cv2
from pyzbar import pyzbar
import BarcodeDetector
import ImageMarker


def read_barcodes_from_image(image_path):
    x = BarcodeDetector.BarcodeDetector().load_image(
        image_path).get_largest_contours(4).to_barcode_objects().get_all_results()
    final_barcodes = []
    for r in x:
        image = r.extractToImage()
        barcodes = pyzbar.decode(image)
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            # print the barcode type and data to the terminal
            print("[INFO] Found {} barcode: {}".format(
                barcodeType, barcodeData))
            final_barcodes.append((r, barcodeType, barcodeData))
        # show the output image
    if len(final_barcodes) > 0:
        f_image = cv2.imread(image_path)
        for barcode in final_barcodes:
            text = text = "{} ({})".format(barcode[2], barcode[1])
            f_image = ImageMarker.draw_box_on_image(
                f_image, barcode.get_top_left(), barcode.get_bottom_right())
            f_image = ImageMarker.add_text_on_image(f_image, text, (barcode.get_min_x(
            ), barcode.get_min_y()-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.waitKey(0)
        cv2.imwrite("result.jpg", f_image)
