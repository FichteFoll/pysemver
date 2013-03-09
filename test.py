import unittest
from sys import version_info
from random import shuffle

from semver import SemVer


class CompTests(unittest.TestCase):

    versions = """
        0.0.0-alpha.2
        0.0.0-alpha.12.0
        0.0.0-beta
        0.0.1
        1.0.0
        1.1.2-alpha
        1.1.2-beta+2.2
        1.1.2-beta+2.2.2
        1.1.2-beta
        1.1.2-gamma
        1.1.2
        2.0.0
        2.0.10
    """.split()

    def __init__(self, *args, **kwargs):
        super(CompTests, self).__init__(*args, **kwargs)

        self.ops = {
            '==': self.assertEqual,
            '!=': self.assertNotEqual,
            '>':  self.assertGreater,
            '>=': self.assertGreaterEqual,
            '<':  self.assertLess,
            '<=': self.assertLessEqual,
        }

    def comp(self, a, op, b):
        self.ops[op](SemVer(a), SemVer(b))

    def test_comparisons(self):
        for i, v in enumerate(self.versions):
            # Equality tests
            self.comp(v, '==', v)

            # Comparisons with other versions
            for j, v2 in enumerate(self.versions):
                if i == j:
                    self.comp(v, '==', v2)
                    self.comp(v, '<=', v2)
                    self.comp(v, '>=', v2)
                if i < j:
                    self.comp(v, '<',  v2)
                    self.comp(v, '!=', v2)
                if i > j:
                    self.comp(v, '>', v2)
                    self.comp(v, '!=', v2)

    def test_simple_sort(self):
        vers = [SemVer(v) for v in self.versions]
        vers_rand = vers[:]
        while vers_rand == vers:
            shuffle(vers_rand)

        self.assertEqual(sorted(vers_rand), vers)


class InvalidityTests(unittest.TestCase):

    def invalid(self, ver):
        self.assertFalse(SemVer.valid(ver))

    def raises(self, err, *args):
        self.assertRaises(err, SemVer, *args)

    def test_invalid_order(self):
        # Can also be considered as "test_invalid_suffix"
        self.invalid("0.0.0+a400-alpha")

    def test_invalid_num_terms(self):
        self.invalid("0.0")
        self.invalid("0.0.0.0+a40-alpha")

    def test_invalid_chars(self):
        self.invalid("0.0,0+a40-alpha")
        self.invalid("0.0-0.0+a40-alpha")
        self.invalid("0.0.~+a40-alpha")
        self.invalid("0.0.~+a40-a&&pha")

    def test_invalid_prefix(self):
        self.invalid(" v0.0.0")
        self.invalid("b0.0.0")

    def test_constructor_errors(self):
        self.raises(ValueError, "0.0,0+a40-alpha")
        self.raises(ValueError, "0.0.~+a40-alpha")
        self.raises(ValueError, "  s 0.0.~+a40-alpha", True)
        self.raises(TypeError,  123)


class ValidityTests(unittest.TestCase):

    def valid(self, ver):
        self.assertTrue(SemVer.valid(ver))

    def test_simple(self):
        self.valid("0.0.0")

    def test_prefixes(self):
        self.valid("v0.0.0")
        self.valid("=0.0.0")
        self.valid("v==0.0.0")
        self.valid("v==  0.0.0")

    def test_prerelease(self):
        self.valid("0.0.0-alpha")

    def test_build(self):
        self.valid("0.0.0+a30b")

    def test_prerelease_build(self):
        self.valid("0.0.0-beta+a30b")

    def test_constructor(self):
        self.assertTrue(SemVer("0.0.0-a40+alpha"))
        self.assertTrue(SemVer(" 213s 0.0.0-a40+alpha", True))


class CleanTests(unittest.TestCase):

    def clean(self, ver1, ver2):
        self.assertEqual(SemVer.clean(ver1), ver2)

    def test_before(self):
        self.clean("   0.0.0-alpha+a40", "0.0.0-alpha+a40")
        self.clean("dsadfqh2536rhnj2ah0.0.0-alpha+a40", "0.0.0-alpha+a40")

    def test_after(self):
        self.clean("= 0.0.0-alpha+a40    ", "= 0.0.0-alpha+a40")
        self.clean("0.0.0-alpha+a40&/dasdtyh231", "0.0.0-alpha+a40")

    def test_before_and_after(self):
        self.clean(" 123 asda3245 v0.0.0-alpha+a40&!/(& 23421 sdfa1", "v0.0.0-alpha+a40")


class CoercionTests(unittest.TestCase):

    def test_truthiness(self):
        self.assertTrue(SemVer("0.0.0-a40+alpha"))
        self.assertFalse(SemVer())

        v = SemVer()
        self.assertFalse(v)
        v.parse("0.0.0")
        self.assertTrue(v)
        self.assertRaises(RuntimeError, v.parse, "0.0.1")

    @unittest.skipUnless(version_info[0] == 3, "Only run these in Python 3")
    def test_compare_string(self):
        self.assertRaises(TypeError, lambda: SemVer("0.0.0-beta") > "0.0.0-alpha")

    @unittest.skipUnless(version_info[0] == 2, "Only run these in Python 2")
    def test_unicode(self):
        # u'' is a syntax error in Py3 so wrap it in eval() (better approaches appreciated)
        self.assertTrue(eval('SemVer.valid(u"0.0.0")'))

    def test_to_string(self):
        self.assertEqual(str(SemVer("0.0.0-beta")), "0.0.0-beta")


class RangeTests(unittest.TestCase):

    def test_simple_range(self):
        self.assertTrue(SemVer("2.0.0").satisfies("1.0.0 - 3.0.0"))
        self.assertTrue(SemVer("2.1.3").satisfies("2.1.0 - 2.1.3"))
        self.assertTrue(SemVer("2.1.3").satisfies("2.1.0 - 2.3.0"))

    def test_lt_range(self):
        self.assertTrue(SemVer("2.1.3").satisfies("<2.2.0"))
        self.assertTrue(SemVer("2.1.3").satisfies("<2.1.4"))
        self.assertTrue(SemVer("2.1.3").satisfies("<10.0.0"))
        self.assertFalse(SemVer("2.1.3").satisfies("<2.1.3"))

    def test_lte_range(self):
        self.assertTrue(SemVer("2.1.3").satisfies("<=2.1.3"))
        self.assertTrue(SemVer("2.1.3").satisfies("<=3.0.0"))
        self.assertFalse(SemVer("2.1.3").satisfies("<=2.1.2"))
        self.assertFalse(SemVer("2.1.3").satisfies("<=1.0.0"))

    def test_gt_range(self):
        self.assertTrue(SemVer("2.2.3").satisfies(">2.2.0"))
        self.assertTrue(SemVer("2.2.0").satisfies(">2.1.4"))
        self.assertTrue(SemVer("10.0.0").satisfies(">2.1.4"))
        self.assertFalse(SemVer("2.1.3").satisfies(">2.1.3"))
        self.assertFalse(SemVer("1.2.2").satisfies(">2.1.3"))

    def test_gte_range(self):
        self.assertTrue(SemVer("2.1.3").satisfies(">=2.1.3"))
        self.assertTrue(SemVer("3.0.0").satisfies(">=2.1.3"))
        self.assertFalse(SemVer("2.1.2").satisfies(">=2.1.3"))
        self.assertFalse(SemVer("1.0.0").satisfies(">=2.1.3"))

    def test_fuzzy_range(self):
        self.assertTrue(SemVer("2.1.3").satisfies("~2"))
        self.assertTrue(SemVer("2.0.0").satisfies("~2"))
        self.assertTrue(SemVer("2.99.1").satisfies("~2"))
        self.assertTrue(SemVer("2.1.3").satisfies("~2.1"))
        self.assertTrue(SemVer("2.1.0").satisfies("~2.1"))
        self.assertTrue(SemVer("2.1.3").satisfies("~2.1.3"))
        self.assertTrue(SemVer("2.1.99").satisfies("~2.1.3"))

        self.assertFalse(SemVer("3.0.0").satisfies("~2"))
        self.assertFalse(SemVer("2.0.1").satisfies("~2.1"))
        self.assertFalse(SemVer("2.2.0").satisfies("~2.1"))
        self.assertFalse(SemVer("2.1.2").satisfies("~2.1.3"))
        self.assertFalse(SemVer("2.2.0").satisfies("~2.1.3"))

    def test_x_range(self):
        self.assertTrue(SemVer("2.1.3").satisfies("2.1.x"))
        self.assertTrue(SemVer("2.1.99").satisfies("2.1.x"))
        self.assertTrue(SemVer("2.0.0").satisfies("2.x"))
        self.assertTrue(SemVer("2.99.1").satisfies("2.x"))

        self.assertFalse(SemVer("3.0.0").satisfies("2.x"))
        self.assertFalse(SemVer("2.0.1").satisfies("2.1.x"))
        self.assertFalse(SemVer("2.2.0").satisfies("2.1.x"))

if __name__ == '__main__':
    unittest.main()
