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
            self.decoded_barcodes = [DecodedBarcode('E-04-01', (212,494), (436,572)),
                                    DecodedBarcode('C-23-04', (1331,488), (1331,566)),
                                    DecodedBarcode('W00025640', (217,309), (418,387)),
                                    DecodedBarcode('W00025419', (1116,294), (1317,372)),
                                    DecodedBarcode('92103022', (238,140), (393,218)),
                                    DecodedBarcode('92103015', (1141,133), (1296,202))]
        trio1, trio2 = Trio(), Trio()
        trio1.location, trio1.raft, trio1.material = 'E-04-01', 'W00025640', '92103022'
        trio2.location, trio2.raft, trio2.material = 'C-23-04', 'W00025419', '92103015'
        self.trios = [trio1, trio2]


    def test_simple(self, analyze_mock):
        analyze_mock.return_value = [(0, self.decoded_barcodes)]
        barcodes_trios = couple_barcodes('')

        self.assertEqual(len(barcodes_trios.trios), len(self.trios))
        for trio in barcodes_trios.trios:
            self.assertTrue(trio in self.trios)
    

    def test_with_locations_above(self, analyze_mock):
        with patch.object(DecodedBarcode, '__init__', DecodedBarcode_init_mock):
            locations_above = [DecodedBarcode('A-65-08', (212,0), (436,120)),
                               DecodedBarcode('B-42-51', (1331,0), (1331,460))]
        analyze_mock.return_value = [(0, locations_above + self.decoded_barcodes)]
        barcodes_trios = couple_barcodes('')

        self.assertEqual(len(barcodes_trios.trios), len(self.trios))
        for trio in barcodes_trios.trios:
            self.assertTrue(trio in self.trios)


if __name__ == '__main__':
    unittest.main()
