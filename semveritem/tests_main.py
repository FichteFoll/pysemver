import unittest
from semveritem import SemVerItem


class ItemTests(unittest.TestCase):

    def setUp(self):
        self.item1 = SemVerItem
        self.item2 = SemVerItem

    def test_equal(self):
        self.assertEqual(self.item1("0.0.0-alpha"), self.item1("0.0.0-alpha"))

    def test_not_equal(self):
        self.assertNotEqual(self.item1("0.0.0-beta"), self.item1("0.0.0-alpha"))

    def test_greater_than(self):
        self.assertTrue(self.item1("0.0.0-beta") > self.item1("0.0.0-alpha"))

    def test_less_than(self):
        self.assertFalse(self.item1("0.0.0-beta") < self.item1("0.0.0-alpha"))

    def test_to_string(self):
        self.assertEqual(str(self.item1("0.0.0-beta")), "0.0.0-beta")
