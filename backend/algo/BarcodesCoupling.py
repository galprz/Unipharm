from ip_main import *
from dataclasses import dataclass
import json

# get image dimensions
with open('camera_settings.json') as f:
    d = json.loads(f.read())
    IMAGE_WIDTH, IMAGE_HEIGHT = d['image_width'], d['image_height']


def couple_barcodes(path):
    """ Tries to group the location, material and raft barcodes while analyzing the video.

    Args:
        path (string): the path of the video file

    Returns:
        BarcodesTrios: all the barcodes in couples or trios (depends on the recognition quality)
    """
    barcodes_trios = BarcodesTrios()
    barcodes_per_frame = analyze(path)
    for frame_index, barcodes in barcodes_per_frame:
        locations, materials, rafts = classify_barcodes(barcodes)
        for loc in locations:
            for material in materials:
                if can_match(loc, material):
                    barcodes_trios[loc] = material
                for raft in rafts:
                    if can_match(loc, raft):
                        barcodes_trios[loc] = raft
                    if can_match(material, raft):
                        barcodes_trios[material] = raft
    return barcodes_trios


def classify_barcodes(barcodes):
    locations = []
    materials = []
    rafts = []
    for barcode in barcodes:
        if barcode.type == LOCATION:
            locations.append(barcode)
        elif barcode.type == MATERIAL:
            materials.append(barcode)
        elif barcode.type == RAFT:
            rafts.append(barcode)
    # filter only unique barcodes
    locations = list(set(locations))
    materials = list(set(materials))
    rafts = list(set(rafts))
    return locations, materials, rafts


def can_match(barcode1, barcode2):
    if barcode1.type == barcode2.type:
        return False

    x1_top_left, y1_top_left = barcode1.get_barcode_top_left_corner()
    x1_bottom_right, y1_bottom_right = barcode1.get_barcode_bottom_right_corner()
    x1_avg = (x1_bottom_right + x1_top_left) / 2
    y1_avg = (y1_bottom_right + y1_top_left) / 2

    x2_top_left, y2_top_left = barcode2.get_barcode_top_left_corner()
    x2_bottom_right, y2_bottom_right = barcode2.get_barcode_bottom_right_corner()
    x2_avg = (x2_bottom_right + x2_top_left) / 2
    y2_avg = (y2_bottom_right + y2_top_left) / 2

    x_diff = abs(x1_avg - x2_avg)
    y_diff = abs(y1_avg - y2_avg)
    
    if set([barcode1.type, barcode2.type]) == set([LOCATION, MATERIAL]):
        return x_diff <= 0.4 * IMAGE_WIDTH
    elif set([barcode1.type, barcode2.type]) == set([LOCATION, RAFT]):
        return x_diff <= 0.3 * IMAGE_WIDTH and y_diff <= 0.2 * IMAGE_HEIGHT
    elif set([barcode1.type, barcode2.type]) == set([RAFT, MATERIAL]):
        return x_diff <= 0.25 * IMAGE_WIDTH
    return False    # should not get here


@dataclass
class Trio:
    location = None
    material = None
    raft = None


class BarcodesTrios:
    """ Class of the trios of the barcodes in a video.

        It can be accessed by either location or material or raft.
        E.g. if you have the location, BarcodesTrios[location] will return you the whole trio with this location 
        (if exists, otherwise an empty Trio with all None fields).

        It can be managed similarly. For example, BarcodesTrios[location] = material 
        will update the material field in the trio corresponding to this location.
    """

    def __init__(self):
        self.trios = []
        self.trios_by_location = {}
        self.trios_by_material = {}
        self.trios_by_raft = {}
    
    def __getitem__(self, key: DecodedBarcode):
        if key.type == LOCATION:
            return self.trios_by_location[key]
        if key.type == MATERIAL:
            return self.trios_by_material[key]
        if key.type == RAFT:
            return self.trios_by_raft[key]
        return self.__find_in_trios(key)
    
    def __setitem__(self, key: DecodedBarcode, val: DecodedBarcode):
        assert(key.type != val.type)

        trio = self.__find_in_trios(key)
        is_in_trios = trio.location or trio.material or trio.raft
        # insert key to the right field in trio
        if key.type == LOCATION:
            trio.location = key
        elif key.type == MATERIAL:
            trio.material = key
        elif key.type == RAFT:
            trio.raft = key
        
        # insert val to the right field in trio
        if val.type == LOCATION:
            trio.location = val
        elif val.type == MATERIAL:
            trio.material = val
        elif val.type == RAFT:
            trio.raft = val
        
        if not is_in_trios:
            self.trios.append(trio)
        
        if trio.location:
            self.trios_by_location[trio.location] = trio
        if trio.material:
            self.trios_by_material[trio.material] = trio
        if trio.raft:
            self.trios_by_raft[trio.raft] = trio
    

    def __find_in_trios(self, key):
        for trio in self.trios:
            if  (key.type == LOCATION and trio.location == key) or \
                (key.type == MATERIAL and trio.material == key) or \
                (key.type == RAFT and trio.raft == key):
                return trio
        return Trio()
