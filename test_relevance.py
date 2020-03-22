import unittest

from relevance import Relevance
from test_data import SHOP_2_LISTINGS


class RelevanceTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_relevance(self):
        shop2words = Relevance(SHOP_2_LISTINGS).compute_relevant_words(5)
        self.assertEqual(3, len(shop2words))
        self.assertEqual(
            {'AtlanticHardware', 'ConnectCo', 'fruitionjewelry'},
            shop2words.keys()
        )

        self.assertEqual(
            ['number', 'numbers', 'house', 'slate', 'digit'],
            shop2words['AtlanticHardware']
        )
        self.assertEqual(
            ['crystal', 'bead', 'similar', 'item', 'receive'],
            shop2words['ConnectCo']
        )
        self.assertEqual(
            ['gold', 'sterling', 'silver', 'ring', '14k'],
            shop2words['fruitionjewelry']
        )


if __name__ == '__main__':
    unittest.main()
