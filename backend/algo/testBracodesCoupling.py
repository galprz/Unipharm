import unittest
from unittest.mock import patch
from ip_main import DecodedBarcode, LOCATION, RAFT, MATERIAL
from BarcodesCoupling import couple_barcodes, Trio


def DecodedBarcode_init_mock(self, data, top_left, bottom_right):
    self.data = data
    self.top_left = top_left
    self.bottom_right = bottom_right

    if '-' in self.data:
        self.type = LOCATION
    elif self.data[0] == 'w' or self.data[0] == 'W':
        self.type = RAFT
    else:
        self.type = MATERIAL


@patch('ip_main.analyze')
class TestBarcodesCopuling(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        with patch.object(DecodedBarcode, '__init__', DecodedBarcode_init_mock):
            self.decoded_barcodes = [DecodedBarcode('E-04-01', (212,0), (436,120)),
                                    DecodedBarcode('C-23-04', (1331,0), (1331,460)),
                                    DecodedBarcode('W00025640', (217,309), (418,387)),
                                    DecodedBarcode('W00025419', (1116,294), (1317,372)),
                                    DecodedBarcode('92103022', (238,140), (393,218)),
                                    DecodedBarcode('92103015', (1141,133), (1296,202))]
        trio1, trio2 = Trio(), Trio()
        # trio1: 'E-04-01', 'W00025640', '92103022'
        trio1.location = self.decoded_barcodes[0]
        trio1.raft = self.decoded_barcodes[2]
        trio1.material = self.decoded_barcodes[4]
        # trio2: 'C-23-04', 'W00025419', '92103015'
        trio2.location = self.decoded_barcodes[1]
        trio2.raft = self.decoded_barcodes[3]
        trio2.material = self.decoded_barcodes[5]
        self.trios = [trio1, trio2]


    def test_simple(self, analyze_mock):
        analyze_mock.return_value = [(0, self.decoded_barcodes)]
        barcodes_trios = couple_barcodes('')

        self.assertEqual(len(barcodes_trios.trios), len(self.trios))
        for actual_trio in self.trios:
            found_trio = find_trio_by_trio(actual_trio, barcodes_trios)
            self.assertEqual(actual_trio.location, found_trio.location)
            self.assertEqual(actual_trio.material, found_trio.material)
            self.assertEqual(actual_trio.raft, found_trio.raft)
    

    def test_with_locations_below(self, analyze_mock):
        with patch.object(DecodedBarcode, '__init__', DecodedBarcode_init_mock):
            locations_above = [DecodedBarcode('A-65-08', (212,494), (436,572)),
                               DecodedBarcode('B-42-07', (1331,488), (1331,566))]
        analyze_mock.return_value = [(0, locations_above + self.decoded_barcodes)]
        barcodes_trios = couple_barcodes('')

        self.assertEqual(len(barcodes_trios.trios), len(self.trios))
        for actual_trio in self.trios:
            found_trio = find_trio_by_trio(actual_trio, barcodes_trios)
            self.assertEqual(actual_trio.location, found_trio.location)
            self.assertEqual(actual_trio.material, found_trio.material)
            self.assertEqual(actual_trio.raft, found_trio.raft)


def find_trio_by_trio(actual_trio, trios):
    found_trio = Trio()
    if actual_trio.location:
        found_trio = trios.find(actual_trio.location)
    elif actual_trio.material:
        found_trio = trios.find(actual_trio.material)
    elif actual_trio.raft:
        found_trio = trios.find(actual_trio.raft)
    return found_trio


if __name__ == '__main__':
    unittest.main()
