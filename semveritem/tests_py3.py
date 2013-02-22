# Python 3 specific tests.
import unittest
from semveritem import SemVerItem


class ItemTests(unittest.TestCase):

    def setUp(self):
        self.item1 = SemVerItem
        self.item2 = SemVerItem

    def test_compare_string(self):
        self.assertRaises(TypeError, lambda:self.item1("0.0.0-beta") > "0.0.0-alpha")
