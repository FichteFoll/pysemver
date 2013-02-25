# Python 3 specific tests.
import unittest
from semver import SemVer


class ItemTests(unittest.TestCase):

    def setUp(self):
        self.item1 = SemVer
        self.item2 = SemVer

    def test_compare_string(self):
        self.assertRaises(TypeError, lambda: self.item1("0.0.0-beta") > "0.0.0-alpha")
