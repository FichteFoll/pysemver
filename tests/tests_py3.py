# Python 3 specific tests.
import sys
import unittest
from semver import SemVer


@unittest.skipUnless(sys.version_info[0] == 3, "Only run these in Python > 3")
class ItemTests(unittest.TestCase):

    def setUp(self):
        self.item1 = SemVer
        self.item2 = SemVer

    def test_compare_string(self):
        self.assertRaises(TypeError, lambda: self.item1("0.0.0-beta") > "0.0.0-alpha")
