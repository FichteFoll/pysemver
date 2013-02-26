import unittest
from semver import SemVer


class CompTests(unittest.TestCase):

    def test_equal(self):
        self.assertEqual(SemVer("0.0.0-alpha"), SemVer("0.0.0-alpha"))

    def test_equal_dot(self):
        self.assertEqual(SemVer("0.0.0-alpha.12.0"), SemVer("0.0.0-alpha.12.0"))

    def test_not_equal(self):
        self.assertNotEqual(SemVer("0.0.0-beta"), SemVer("0.0.0-alpha"))

    def test_greater_than(self):
        self.assertGreater(SemVer("0.0.0-beta"), SemVer("0.0.0-alpha"))

    def test_greater_equal(self):
        self.assertGreaterEqual(SemVer("0.0.0-beta"), SemVer("0.0.0-alpha"))

    def test_greater_equal_equal(self):
        self.assertGreaterEqual(SemVer("0.0.0-alpha"), SemVer("0.0.0-alpha"))

    def test_less_than(self):
        self.assertLess(SemVer("0.0.0-alpha"), SemVer("0.0.0-beta"))

    def test_less_equal(self):
        self.assertLessEqual(SemVer("0.0.0-alpha"), SemVer("0.0.0-beta"))

    def test_less_equal_equal(self):
        self.assertLessEqual(SemVer("0.0.0-beta"), SemVer("0.0.0-beta"))

    def test_to_string(self):
        self.assertEqual(str(SemVer("0.0.0-beta")), "0.0.0-beta")


class InvalidityTests(unittest.TestCase):

    def test_invalid_order(self):
        self.assertFalse(SemVer.valid("0.0.0+a400-alpha"))

    def test_invalid_num_terms_short(self):
        self.assertFalse(SemVer.valid("0.0"))

    def test_invalid_num_terms_long(self):
        self.assertFalse(SemVer.valid("0.0.0.0+a40-alpha"))

    def test_invalid_chars_comma(self):
        self.assertFalse(SemVer.valid("0.0,0+a40-alpha"))

    def test_invalid_chars_dash(self):
        self.assertFalse(SemVer.valid("0.0-0.0+a40-alpha"))

    def test_invalid_chars_tilda(self):
        self.assertFalse(SemVer.valid("0.0.~+a40-alpha"))


class ValidityTests(unittest.TestCase):

    def test_simple(self):
        self.assertTrue(SemVer.valid("0.0.0"))

    def test_prerelease(self):
        self.assertTrue(SemVer.valid("0.0.0-alpha"))

    def test_build(self):
        self.assertTrue(SemVer.valid("0.0.0+a30b"))

    def test_prerelease_build(self):
        self.assertTrue(SemVer.valid("0.0.0-beta+a30b"))

    def test_invalid_chars_comma(self):
        self.assertFalse(SemVer.valid("0.0.0+a40-alpha"))

    def test_invalid_chars_dash(self):
        self.assertFalse(SemVer.valid("0.0.0+a40-alpha"))

    def test_invalid_chars_tilda(self):
        self.assertFalse(SemVer.valid("0.0.0+a40-alpha"))


class RangeChecks(unittest.TestCase):

    def test_simple_range(self):
        self.assertTrue(SemVer("2.0.0").satisfies("1.0.0 - 3.0.0"))
