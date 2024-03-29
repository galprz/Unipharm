from pyzbar import pyzbar
import cv2
from pyzbar.pyzbar import ZBarSymbol, decode
SUPPORTED_BARCODE_TYPES = [ZBarSymbol.CODE128]


def visualize(image, barcodes, out_path=None):
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodedata = barcode.data.decode("utf-8")
        barcodetype = barcode.type

        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodedata, barcodetype)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 2)

        # print the barcode type and data to the terminal
        print("[INFO] Found {} barcode: {}".format(barcodetype, barcodedata))
    if out_path is not None:
        cv2.imwrite(out_path, image)


#  The following is a generator that each time returns the next frame of a video given in `path`
def parse_video(path, parameters={'sample_rate': 10}):
    vc = cv2.VideoCapture(path)
    success, frame = vc.read()
    count = 0
    while success:
        if count % parameters['sample_rate'] == 0:
            yield frame
        count += 1
        success, frame = vc.read()

#  used mostly for testing, analyzes a single image with no merging of results with other image's results.


def analyze_single_image(path, parameters={}):
    res = process_image(cv2.imread(path), 0, parameters)
    return [(0, res)] if len(res) > 0 else []

#  recevies a path to a video and analyzes sampled frames from it.
#  output is a list with a tupple for each frame in which barcodes were identifdied
# where its second element is a list of objects describing the identified and decoded barcodes.


def analyze(path, parameters={'sample_rate': 10, 'visualize_numbers': []}):
    images = parse_video(path, parameters)
    result = []
    for index, image in enumerate(images):
        res = process_image(image, index, parameters)
        if len(res) > 0:
            result.append((index, res))
    return result


RAFT = 0
MATERIAL = 1
LOCATION = 2

#  This represents an identified barcode


class DecodedBarcode(object):
    def __init__(self, barcode):
        self.data = barcode.data.decode("utf-8")
        x, y, w, h = barcode.rect
        self.top_left = (x, y)
        self.bottom_right = (x + w, y + h)

        if '-' in self.data:
            self.type = LOCATION
        elif self.data[0] == 'w' or self.data[0] == 'W':
            self.type = RAFT
        else:
            self.type = MATERIAL

    #  following two methods are for topology analysis
    def get_barcode_top_left_corner(self) -> tuple:
        return self.top_left

    def get_barcode_bottom_right_corner(self) -> tuple:
        return self.bottom_right

    #  Future compatibility
    def __str__(self):
        if self.type == MATERIAL:
            c = 'MATERIAL'
        elif self.type == LOCATION:
            c = 'LOCATION'
        else:
            c = 'RAFT'

        return f'Value: {self.data}  Type: {c}  Top Left Corner: ({self.top_left[0]},{self.top_left[1]})  Bottom Right Corner: ({self.bottom_right[0]},{self.bottom_right[1]})'

    def __eq__(self, other):
        return self.data == other.data if other else False

    def __hash__(self):
        return super().__hash__()

#   The main image processing logic based on pyzbar library


def process_image(image, idx,  parameters):
    found_barcodes = pyzbar.decode(image, symbols=SUPPORTED_BARCODE_TYPES)
    previously_identified = []
    decoded_barcodes = []
    #  visualize numbers is a parameter for testing
    if 'visualize_numbers' in parameters.keys() and idx in parameters['visualize_numbers']:
        visualize(image, found_barcodes, r'D:\visualized.jpg')
    for barcode in found_barcodes:
        if barcode.data.decode("utf-8")[0] == 'S' or barcode.data.decode("utf-8")[0] in previously_identified:
            continue
        else:
            previously_identified.append(barcode.data.decode("utf-8"))
            decoded_barcodes.append(DecodedBarcode(barcode))
    return decoded_barcodes
