from ip_main import DecodedBarcode, LOCATION, MATERIAL, RAFT
import ip_main
import json
from typing import List, Tuple

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
                barcode_loc, barcode_material = can_match(loc, material)
                if barcode_loc is not None and barcode_material is not None:
                    barcodes_trios[barcode_loc] = barcode_material
                for raft in rafts:
                    barcode_loc, barcode_raft = can_match(loc, raft)
                    if barcode_loc is not None and barcode_raft is not None:
                        barcodes_trios[barcode_loc] = barcode_raft
                    barcode_material, barcode_raft = can_match(material, raft)
                    if barcode_material is not None and barcode_raft is not None:
                        barcodes_trios[barcode_material] = barcode_raft
    return barcodes_trios


def classify_barcodes(barcodes: List[DecodedBarcode]):
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


class Barcode(object):
    """ Usage:
            Barcode(db: DecodedBarcode) or Barcode(data, type)
    """
    def __init__(self, **kwargs):
        self.data = None
        self.type = None
        if len(kwargs) == 1:
            item = list(kwargs.values())[0]
            if type(item) == DecodedBarcode:
                self.data = item.data
                self.type = item.type
        elif len(kwargs) == 2:
            if {'data', 'type'} == set(kwargs):
                self.data = kwargs['data']
                self.type = kwargs['type']
    
    def __eq__(self, other):
        return self.data == other.data if other else False
    
    def __hash__(self):
        return super().__hash__()


class Trio(object):
    def __init__(self, location: Barcode=None, material: Barcode=None, raft: Barcode=None):
        self.location = location
        self.material = material
        self.raft = raft
    
    def __eq__(self, other):
        return  self.location == other.location and \
                self.material == other.material and \
                self.raft == other.raft
    
    def __hash__(self):
        return super().__hash__()


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
    
    def __getitem__(self, key: Barcode):
        if key.type == LOCATION:
            return self.trios_by_location[key]
        if key.type == MATERIAL:
            return self.trios_by_material[key]
        if key.type == RAFT:
            return self.trios_by_raft[key]
        return self.find(key)
    
    def __setitem__(self, key: Barcode, val: Barcode):
        assert(key.type != val.type)

        trio = self.find(key)
        is_in_trios = trio.location or trio.material or trio.raft
        if not is_in_trios:
            trio = self.find(val)
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
    

    def find(self, key):
        for trio in self.trios:
            if  (key.type == LOCATION and trio.location == key) or \
                (key.type == MATERIAL and trio.material == key) or \
                (key.type == RAFT and trio.raft == key):
                return trio
        return Trio()


def can_match(barcode1: DecodedBarcode, barcode2: DecodedBarcode) -> Tuple[Barcode, Barcode]:
    if barcode1.type == barcode2.type:
        return False

    loaction_barcode = barcode1 if barcode1.type == LOCATION \
                       else barcode2 if barcode2.type == LOCATION \
                       else None
    material_barcode = barcode1 if barcode1.type == MATERIAL \
                       else barcode2 if barcode2.type == MATERIAL \
                       else None
    raft_barcode = barcode1 if barcode1.type == RAFT \
                   else barcode2 if barcode2.type == RAFT \
                   else None

    loc_x_avg, loc_y_avg = __get_barcode_xy_avg(loaction_barcode) if loaction_barcode else (0, 0)
    mat_x_avg, mat_y_avg = __get_barcode_xy_avg(material_barcode) if material_barcode else (0, 0)
    raf_x_avg, raf_y_avg = __get_barcode_xy_avg(raft_barcode)     if raft_barcode     else (0, 0)
    
    if loaction_barcode and material_barcode:
        x_diff = abs(loc_x_avg - mat_x_avg)
        is_same_column = x_diff <= 0.4 * IMAGE_WIDTH
        floor = int(loaction_barcode.data[-1])
        # usually location is above the material, except for the last (8th) floor which is below the material
        if  (floor <  8 and loc_y_avg < mat_y_avg and is_same_column) or \
            (floor == 8 and loc_y_avg > mat_y_avg and is_same_column):
            return Barcode(db=loaction_barcode), Barcode(db=material_barcode)
        # take the location above if only the one below had been recognized
        if is_same_column and loc_y_avg > mat_y_avg:
            loc_above = loaction_barcode.data[:-1] + str(floor + 1)
            return Barcode(data=loc_above, type=LOCATION), Barcode(db=material_barcode)
    
    elif loaction_barcode and raft_barcode:
        x_diff = abs(loc_x_avg - raf_x_avg)
        is_same_column = x_diff <= 0.3 * IMAGE_WIDTH
        floor = int(loaction_barcode.data[-1])
        # usually location is above the raft, except for the last (8th) floor which is below the raft
        if  (floor <  8 and loc_y_avg < raf_y_avg and is_same_column) or \
            (floor == 8 and loc_y_avg > raf_y_avg and is_same_column):
            return Barcode(db=loaction_barcode), Barcode(db=raft_barcode)
        # take the location above if only the one below had been recognized
        if is_same_column and loc_y_avg > raf_y_avg:
            loc_above = loaction_barcode.data[:-1] + str(floor + 1)
            return Barcode(data=loc_above, type=LOCATION), Barcode(db=raft_barcode)
    
    # raft below material
    elif material_barcode and raft_barcode:
        x_diff = abs(mat_x_avg - raf_x_avg)
        if raf_y_avg > mat_y_avg and x_diff <= 0.25 * IMAGE_WIDTH:
            return Barcode(db=material_barcode), Barcode(db=raft_barcode)
    return None, None    # should not get here


def __get_barcode_xy_avg(barcode: DecodedBarcode):
    x_top_left, y_top_left = barcode.get_barcode_top_left_corner()
    x_bottom_right, y_bottom_right = barcode.get_barcode_bottom_right_corner()
    x_avg = (x_bottom_right + x_top_left) / 2
    y_avg = (y_bottom_right + y_top_left) / 2
    return x_avg, y_avg
