import cv2
from pyzbar import pyzbar
from BarcodeDetector import BarcodeDetector
import ImageMarker
import BarcodeCandidate
import numpy
import json

Image = numpy.ndarray
BarcodeType = str
BarcodeData = str
Color = tuple


class Barcodes(object):
    def __init__(self, list_of_decoded_barcodes: list, original_image_path: str):
        self.barcodes_list = list_of_decoded_barcodes
        self.original_image_path = original_image_path

    def save_image_with_marked_barcodes(self, output_path):
        if len(self.barcodes_list) > 0:
            f_image = cv2.imread(self.original_image_path)
            for decoded_barcode in self.barcodes_list:
                f_image = place_barcode_data_and_box_on_image(
                    image=f_image,
                    decoded_barcode=decoded_barcode,
                    font=cv2.FONT_HERSHEY_SIMPLEX,
                    font_scaling=0.5,
                    color=(0, 0, 255),
                    width=2)
            cv2.imwrite(output_path, f_image)

    def get_decoded_data(self):
        return [x.descriptive_tuple() for x in self.barcodes_list]


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


def read_barcodes_from_image(image_path) -> Barcodes:
    candidates = BarcodeDetector().load_image(
        image_path).get_largest_contours(4).to_barcode_objects().get_all_results()
    final_barcodes = []
    for barcode_candidate in candidates:
        image = barcode_candidate.extract_to_image()
        barcodes = pyzbar.decode(image)
        for decoded_barcode in barcodes:
            final_barcodes.append(DecodedBarcode(
                barcode_candidate,
                decoded_barcode))
    return Barcodes(final_barcodes, image_path)


def place_barcode_data_and_box_on_image(image: Image, decoded_barcode: DecodedBarcode, font: int, font_scaling: float, color: Color, width: int) -> Image:
    text = "{} ({})".format(
        decoded_barcode.type,
        decoded_barcode.data)
    f_image = ImageMarker.draw_box_on_image(image=image,
                                            top_left_corner=decoded_barcode.get_barcode_top_left_corner(),
                                            bottom_right_corner=decoded_barcode.get_barcode_bottom_right_corner(),
                                            color=color,
                                            width=width)

    return ImageMarker.add_text_on_image(image=f_image,
                                         text=text,
                                         text_start_position=(
                                             decoded_barcode.barcode.get_min_x(), decoded_barcode.barcode.get_min_y()-10),
                                         font=font,
                                         font_scale=font_scaling,
                                         color=color,
                                         width=width)
