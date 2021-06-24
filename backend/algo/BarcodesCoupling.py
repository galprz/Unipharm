from ip_main import DecodedBarcode
import ip_main
from dataclasses import dataclass
import json

# get image dimensions
with open('../../camera_settings.json') as f:
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
    barcodes_per_frame = ip_main.analyze(path)
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
        if barcode.type == ip_main.LOCATION:
            locations.append(barcode)
        elif barcode.type == ip_main.MATERIAL:
            materials.append(barcode)
        elif barcode.type == ip_main.RAFT:
            rafts.append(barcode)
    # filter only unique barcodes
    locations = list(set(locations))
    materials = list(set(materials))
    rafts = list(set(rafts))
    return locations, materials, rafts


def can_match(barcode1: DecodedBarcode, barcode2: DecodedBarcode):
    if barcode1.type == barcode2.type:
        return False

    loaction_barcode = barcode1 if barcode1.type == ip_main.LOCATION \
                       else barcode2 if barcode2.type == ip_main.LOCATION \
                       else None
    material_barcode = barcode1 if barcode1.type == ip_main.MATERIAL \
                       else barcode2 if barcode2.type == ip_main.MATERIAL \
                       else None
    raft_barcode = barcode1 if barcode1.type == ip_main.RAFT \
                   else barcode2 if barcode2.type == ip_main.RAFT \
                   else None

    loc_x_avg, loc_y_avg = __get_barcode_xy_avg(loaction_barcode) if loaction_barcode else (0, 0)
    mat_x_avg, mat_y_avg = __get_barcode_xy_avg(material_barcode) if material_barcode else (0, 0)
    raf_x_avg, raf_y_avg = __get_barcode_xy_avg(raft_barcode)     if raft_barcode     else (0, 0)
    
    # location above material
    if loaction_barcode and material_barcode:
        x_diff = abs(loc_x_avg - mat_x_avg)
        return loc_y_avg < mat_y_avg and x_diff <= 0.4 * IMAGE_WIDTH
    # location above raft
    elif loaction_barcode and raft_barcode:
        x_diff = abs(loc_x_avg - raf_x_avg)
        return loc_y_avg < raf_y_avg and x_diff <= 0.3 * IMAGE_WIDTH
    # raft under material
    elif material_barcode and raft_barcode:
        x_diff = abs(mat_x_avg - raf_x_avg)
        return raf_y_avg > mat_y_avg and x_diff <= 0.25 * IMAGE_WIDTH
    return False    # should not get here


def __get_barcode_xy_avg(barcode: DecodedBarcode):
    x_top_left, y_top_left = barcode.get_barcode_top_left_corner()
    x_bottom_right, y_bottom_right = barcode.get_barcode_bottom_right_corner()
    x_avg = (x_bottom_right + x_top_left) / 2
    y_avg = (y_bottom_right + y_top_left) / 2
    return x_avg, y_avg


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
    
    def __getitem__(self, key: ip_main.DecodedBarcode):
        if key.type == ip_main.LOCATION:
            return self.trios_by_location[key]
        if key.type == ip_main.MATERIAL:
            return self.trios_by_material[key]
        if key.type == ip_main.RAFT:
            return self.trios_by_raft[key]
        return self.find(key)
    
    def __setitem__(self, key: ip_main.DecodedBarcode, val: ip_main.DecodedBarcode):
        assert(key.type != val.type)

        trio = self.find(key)
        is_in_trios = trio.location or trio.material or trio.raft
        if not is_in_trios:
            trio = self.find(val)
            is_in_trios = trio.location or trio.material or trio.raft
        
        # insert key to the right field in trio
        if key.type == ip_main.LOCATION:
            trio.location = key
        elif key.type == ip_main.MATERIAL:
            trio.material = key
        elif key.type == ip_main.RAFT:
            trio.raft = key
        
        # insert val to the right field in trio
        if val.type == ip_main.LOCATION:
            trio.location = val
        elif val.type == ip_main.MATERIAL:
            trio.material = val
        elif val.type == ip_main.RAFT:
            trio.raft = val
        
        if not is_in_trios:
            self.trios.append(trio)
        
        if trio.location:
            self.trios_by_location[trio.location] = trio
        if trio.material:
            self.trios_by_material[trio.material] = trio
        if trio.raft:
            self.trios_by_raft[trio.raft] = trio
    

    def find(self, key):
        for trio in self.trios:
            if  (key.type == ip_main.LOCATION and trio.location == key) or \
                (key.type == ip_main.MATERIAL and trio.material == key) or \
                (key.type == ip_main.RAFT and trio.raft == key):
                return trio
        return Trio()
