import BarcodeReader
import unittest


class TestBarcodeDetection(unittest.TestCase):

    def test_finds_same_data_as_pyzbar(self):
        expected = [('E-01-00', 'CODE128'), ('E-01-01', 'CODE39')]

        res = BarcodeReader.read_barcodes_from_image(
            'D:\\Unifarm\\U\\Unipharm\\backend\\algo\\md\\P2.jpg').get_decoded_data()
        res.sort(key=lambda x: x[0])

        self.assertListEqual(
            res, expected, 'Implementation didnt find same as pyzbar')


if __name__ == "__main__":
    unittest.main()
