import unittest
from semver import SemVer


class CompTests(unittest.TestCase):

    def setUp(self):
        self.item1 = SemVer
        self.item2 = SemVer

    def test_equal(self):
        self.assertEqual(self.item1("0.0.0-alpha"), self.item1("0.0.0-alpha"))

    def test_equal_dot(self):
        self.assertEqual(self.item1("0.0.0-alpha.12.0"), self.item1("0.0.0-alpha.12.0"))

    def test_not_equal(self):
        self.assertNotEqual(self.item1("0.0.0-beta"), self.item1("0.0.0-alpha"))

    def test_greater_than(self):
        self.assertTrue(self.item1("0.0.0-beta") > self.item1("0.0.0-alpha"))

    def test_less_than(self):
        self.assertFalse(self.item1("0.0.0-beta") < self.item1("0.0.0-alpha"))

    def test_to_string(self):
        self.assertEqual(str(self.item1("0.0.0-beta")), "0.0.0-beta")


class InvalidityTests(unittest.TestCase):

    def setUp(self):
        self.item = SemVer

    def test_invalid_order(self):
        self.assertFalse(self.item.valid("0.0.0+a400-alpha"))

    def test_invalid_num_terms_short(self):
        self.assertFalse(self.item.valid("0.0"))

    def test_invalid_num_terms_long(self):
        self.assertFalse(self.item.valid("0.0.0.0+a40-alpha"))

    def test_invalid_chars_comma(self):
        self.assertFalse(self.item.valid("0.0,0+a40-alpha"))

    def test_invalid_chars_dash(self):
        self.assertFalse(self.item.valid("0.0-0.0+a40-alpha"))

    def test_invalid_chars_tilda(self):
        self.assertFalse(self.item.valid("0.0.~+a40-alpha"))


class ValidityTests(unittest.TestCase):

    def setUp(self):
        self.item = SemVer

    def test_simple(self):
        self.assertTrue(self.item.valid("0.0.0"))

    def test_prerelease(self):
        self.assertTrue(self.item.valid("0.0.0-alpha"))

    def test_build(self):
        self.assertTrue(self.item.valid("0.0.0+a30b"))

    def test_prerelease_build(self):
        self.assertTrue(self.item.valid("0.0.0-beta+a30b"))

    def test_invalid_chars_comma(self):
        self.assertFalse(self.item.valid("0.0.0+a40-alpha"))

    def test_invalid_chars_dash(self):
        self.assertFalse(self.item.valid("0.0.0+a40-alpha"))

    def test_invalid_chars_tilda(self):
        self.assertFalse(self.item.valid("0.0.0+a40-alpha"))
