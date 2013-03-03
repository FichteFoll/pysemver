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

    def test_invalid_prefix(self):
        self.assertFalse(SemVer.valid(" v0.0.0"))
        self.assertFalse(SemVer.valid("b0.0.0"))

    def test_constructor_errors(self):
        self.assertRaises(ValueError, SemVer, "0.0,0+a40-alpha")
        self.assertRaises(ValueError, SemVer, "0.0.~+a40-alpha")
        self.assertRaises(ValueError, SemVer, "  s 0.0.~+a40-alpha", True)
        self.assertRaises(TypeError, SemVer, 123)


class ValidityTests(unittest.TestCase):

    def test_simple(self):
        self.assertTrue(SemVer.valid("0.0.0"))

    def test_prefixes(self):
        self.assertTrue(SemVer.valid("v0.0.0"))
        self.assertTrue(SemVer.valid("=0.0.0"))
        self.assertTrue(SemVer.valid("v==0.0.0"))
        self.assertTrue(SemVer.valid("v==  0.0.0"))

    def test_prerelease(self):
        self.assertTrue(SemVer.valid("0.0.0-alpha"))

    def test_build(self):
        self.assertTrue(SemVer.valid("0.0.0+a30b"))

    def test_prerelease_build(self):
        self.assertTrue(SemVer.valid("0.0.0-beta+a30b"))

    def test_constructor(self):
        self.assertTrue(SemVer("0.0.0-a40+alpha"))
        self.assertTrue(SemVer(" 213s 0.0.0-a40+alpha", True))


class CleanTests(unittest.TestCase):

    def test_spaces_before(self):
        self.assertEqual(SemVer.clean("   0.0.0-alpha+a40"), "0.0.0-alpha+a40")

    def test_anything_before(self):
        self.assertEqual(SemVer.clean("dsadfqh2536rhnj2ah0.0.0-alpha+a40"), "0.0.0-alpha+a40")

    def test_spaces_after(self):
        self.assertEqual(SemVer.clean("= 0.0.0-alpha+a40    "), "= 0.0.0-alpha+a40")

    def test_anything_after(self):
        self.assertEqual(SemVer.clean("0.0.0-alpha+a40&/dasdtyh231"), "0.0.0-alpha+a40")

    def test_before_and_after(self):
        self.assertEqual(SemVer.clean(" 123 asda3245 v0.0.0-alpha+a40&!/(§& 23421 sdfa1"), "v0.0.0-alpha+a40")


class CoercionTests(unittest.TestCase):

    def test_invalid(self):
        self.assertTrue(bool(SemVer("0.0.0-a40+alpha")))
        self.assertFalse(bool(SemVer()))


class RangeChecks(unittest.TestCase):

    def test_simple_range(self):
        self.assertTrue(SemVer("2.0.0").satisfies("1.0.0 - 3.0.0"))
