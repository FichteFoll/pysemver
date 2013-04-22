"""
Copyright (c) 2013 FichteFoll

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions: The above copyright notice and this
permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


from sys import version_info
from random import shuffle

from semver import *  # SemVer, SemSel, SelParseError

# Use unittest2 for Python <2.7
if version_info < (2, 7, 0):
    import unittest2 as unittest
else:
    import unittest


class CompTests(unittest.TestCase):
    versions = """
        0.0.0-alpha.2
        0.0.0-alpha.12.0
        0.0.0-beta
        0.0.1
        1.0.0
        1.1.2-
        1.1.2-alpha
        1.1.2-beta
        1.1.2-beta+2.2
        1.1.2-beta+12.2.2
        1.1.2-gamma
        1.1.2
        1.1.2+build.2
        1.1.2+build.10
        1.1.2+
        2.0.0
        2.0.10
    """.split()

    # Do not limit the list comparison to 600 chars
    maxDiff = None

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
                    self.assertEqual(hash(v), hash(v2))
                else:
                    self.comp(v, '!=', v2)
                    self.assertNotEqual(hash(v), hash(v2))
                if i < j:
                    self.comp(v, '<',  v2)

                if i > j:
                    self.comp(v, '>', v2)

    def test_simple_sort(self):
        vers = [SemVer(v) for v in self.versions]
        vers_rand = vers[:]
        while vers_rand == vers:
            shuffle(vers_rand)

        self.assertEqual(sorted(vers_rand), vers)


class ValidityTests(unittest.TestCase):
    def valid(self, ver):
        self.assertTrue(SemVer.valid(ver))

    def test_simple(self):
        self.valid("0.0.0")

    def test_prerelease(self):
        self.valid("0.0.0-alpha")
        self.valid("0.0.0-a-b-c.2")

    def test_build(self):
        self.valid("0.0.0+a30b")
        self.valid("0.0.0+a-30.b")

    def test_prerelease_build(self):
        self.valid("0.0.0-beta.2+a30b")


class InvalidityTests(unittest.TestCase):
    def invalid(self, ver):
        self.assertFalse(SemVer.valid(ver))

    def test_invalid_num_terms(self):
        self.invalid("0.0")
        self.invalid("0.0.0.0+a40-alpha")

    def test_invalid_chars(self):
        self.invalid("0.0,0+a40-alpha")
        self.invalid("0.0-0.0+a40-alpha")
        self.invalid("0.0.~+a40-alpha")
        self.invalid("0.0.~+a40-a&&pha")

    def test_invalid_prefix(self):
        self.invalid("v0.0.0")
        self.invalid(" b 20.0.0")
        self.invalid("=0.0.0")


class ConstructorTests(unittest.TestCase):
    def returns(self, ret, *args, **kwargs):
        self.assertEqual(str(SemVer(*args, **kwargs)), ret)

    def test_constructor_opt1(self):
        self.returns("0.1.2-a40+alpha", "0.1.2-a40+alpha")
        self.returns("0.1.2-a40+alpha", ver="0.1.2-a40+alpha")
        self.returns("0.1.2-a40+alpha", ver="0.1.2-a40+alpha", clean=False)
        self.returns("0.1.2-a40+alpha", clean=False, ver="0.1.2-a40+alpha")
        self.returns("0.1.2-a40+alpha", " 213s 0.1.2-a40+alpha", True)
        self.returns("0.1.2-a40+alpha", " 213s 0.1.2-a40+alpha", clean=True)

    def test_constructor_opt2(self):
        self.returns("0.1.2",    0, 1, 2)
        self.returns("0.1.2",    0, 1, '2')
        self.returns("0.1.2-",   0, 1, 2, '')
        self.returns("0.1.2-3",  0, 1, 2, 3)
        self.returns("0.1.2-+-", 0, 1, 2, '', '-')
        self.returns("0.1.2-+-", 0, 1, 2, build='-', prerelease='')
        self.returns("0.1.2-+-", 0, build='-', prerelease='', minor=1, patch=2)
        self.returns("0.1.2+",   0, 1, 2, build='')
        self.returns("0.1.2+",   *list(range(3)), build='')
        self.returns("0.1.2",    major=0, minor=1, patch=2)
        self.returns("0.1.2",    **dict(major=0, minor=1, patch=2))
        self.returns("0.1.2+0.1.2.3.4", *('0.1.2'.split('.')), build='.'.join(map(str, range(5))))

    def test_constructor_errors(self):
        r = lambda r, *a, **kw: self.assertRaises(r, SemVer, *a, **kw)

        r(ValueError, "0.1,2+a40-alpha")
        r(ValueError, "0.1.~+a40-alpha")
        r(ValueError, " 0.1.2-a40+alpha")
        r(ValueError, " 0.1.~+a40-alpha", True)
        r(TypeError, "0.1.2+a40-alpha", c=1)
        r(TypeError, False, ver="0.1.2+a40-alpha")
        r(TypeError, 123)
        r(TypeError, list(range(3)))
        r(TypeError, lambda x: x)
        r(TypeError)

        r(TypeError, 0, 1, 2, 3, 4, 5)
        r(TypeError, 0, 1)
        r(ValueError, 0, 1, 2, '+')
        r(ValueError, 0, 1, 2, build='+')
        r(ValueError, 'a', 1, 2)
        r(ValueError, 0, 1, 'a')
        r(TypeError, 0, 1, 2, ver='0.1.2')
        r(TypeError, 0, 1, 2, v='0.1.2')


class CleanTests(unittest.TestCase):
    def clean(self, ver1, ver2):
        self.assertEqual(SemVer.clean(ver1), ver2)

    def test_before(self):
        self.clean("   0.0.0-alpha+a40",                "0.0.0-alpha+a40")
        self.clean("dsadfqh2536rhnj2ah0.0.0-alpha+a40", "0.0.0-alpha+a40")

    def test_after(self):
        self.clean("0.0.0-alpha+a40    ",         "0.0.0-alpha+a40")
        self.clean("0.0.0-alpha+a40&/dasdtyh231", "0.0.0-alpha+a40")

    def test_before_and_after(self):
        self.clean(" 123 asda3245 0.0.0-alpha+a40&!/(& 23421 sdfa1", "0.0.0-alpha+a40")


class CoercionTests(unittest.TestCase):
    def test_truthiness(self):
        self.assertTrue(SemVer("0.0.1"))

    @unittest.skipUnless(version_info[0] == 3, "Only run these in Python 3")
    def test_compare_string(self):
        self.assertRaises(TypeError, (lambda: SemVer("0.0.0-beta") > "0.0.0-alpha"))

    @unittest.skipUnless(version_info[0] == 2, "Only run these in Python 2")
    def test_unicode(self):
        # u'' is a syntax error in Py3 so wrap it in eval() (better approaches appreciated)
        self.assertTrue(eval('SemVer.valid(u"0.0.0")'))
        self.assertTrue(eval('SemSel(u"0.0.0")'))

    def test_to_string(self):
        self.assertEqual(str(SemVer("0.0.0-beta")), "0.0.0-beta")

    def test_as_dict(self):
        self.assertEqual(SemVer("0.0.0-beta+alpha")._asdict(),
                         dict(major=0, minor=0, patch=0,
                              prerelease='beta', build='alpha'))


class SelectorTests(unittest.TestCase):
    def selector(self, res, sels):
        for s in sels:
            selstr = str(SemSel(s))
            if not selstr == res:
                print('SemSel("%s") did not result in "%s"' % (s, res))
            self.assertEqual(str(SemSel(s)), res)

    def error(self, err, sels):
        r = None
        for s in sels:
            try:
                SemSel(s)
            except err:
                self.assertRaises(err, SemSel, s)
            except Exception as e:
                # `raise RuntimeError(...) from e` would be nice here but is Py3 only
                r = RuntimeError('SemSel(%r) raised %r instead of %s' % (s, e, err))
            else:
                r = RuntimeError('SemSel(%r) did not raise %s' % (s, err))
            if r:
                raise r

    def str_sel_test(self, t):
        for l in t.splitlines():
            if l.strip():
                k, v = l.split(':')
                self.selector(v.strip(), k.strip().split(', '))

    def str_err_test(self, t):
        for l in t.splitlines():
            if l.strip():
                e, v = l.split(':')
                self.error(eval(e.strip()), v.strip().split(', '))
                # Yes, eval() is evil but I have no other idea besides importing __builtin__

    def test_xrange_and_fuzzy(self):
        t = '''
            *, ~, ~>x, ~=X:               >=0.0.0-
            2.x, 2.x.x, 2, ~2, ~>2, ~2.x: >=2.0.0- <3.0.0-
            ~1.2, ~1.2.x, ~>1.2, ~>1.2.x: >=1.2.0- <1.3.0-
            ~1.2.3, ~>1.2.3:              >=1.2.3- <1.3.0-
            ~1.2.0, ~>1.2.0:              >=1.2.0- <1.3.0-
        '''
        self.str_sel_test(t)

    def test_simple_range(self):
        t = '''
            1.0.0 - 3.0.0:                   >=1.0.0 <=3.0.0
            2.1.0-beta.2 - 2.1.0-beta.3+456: >=2.1.0-beta.2 <=2.1.0-beta.3+456
        '''
        self.str_sel_test(t)

    def test_or(self):
        t = '''
            >1.0.0 || <0.2.6:            >1.0.0 || <0.2.6
            !=0.0.0-pre || <=10.0.2+123: !=0.0.0-pre || <=10.0.2+123
        '''
        self.str_sel_test(t)

    def test_and(self):
        t = '''
            >1.0.0 <0.2.6:        >1.0.0 <0.2.6
            0.0.0-pre 10.0.2+123: =0.0.0-pre =10.0.2+123
        '''
        self.str_sel_test(t)

    def test_comparators(self):
        t = '''
             <0.2.6:        <0.2.6
            >=0.2.6:       >=0.2.6
            <=0.2.6:       <=0.2.6
            =0.2.6:         =0.2.6
            0.2.6:          ~0.2.6
            0.2.6-:         =0.2.6-
            !=0.2.6:       !=0.2.6
            !0.2.6:         !0.2.6
            !0.2.6-:       !=0.2.6-
        '''
        self.str_sel_test(t)

    def test_invalids(self):
        t = '''
            ValueError: >1.0, >=1, >v1.2.3, >*
            ValueError: 1.1.1.1, a.b.c, !=1.2.x, !=0
            ValueError: 1.2.3-4++, 1.2.3++, 1.2.3 - 1.2.3++
            SelParseError: >1.2.3 - 1.2.3, 1.2.3 - >1.2.3, ~1 || - 1.2.3, 1.2.3 -
            SelParseError: ~!1.2.0, <0.2., **, 1.2.xx, 1.x.2, 1..2
            SelParseError: || <=10.0.2+123, !=0.0.0-pre ||, 1.2.3 || || 1.3.4
        '''
        self.str_err_test(t)

        self.error(TypeError, (123, 1.2, lambda a: 0))
        self.error(ValueError, (''))


class MatchTests(unittest.TestCase):
    def matches(self, state, sel, vers):
        func = (self.assertFalse, self.assertTrue)[state]
        for v in vers:
            test = bool(SemSel(sel).matches(SemVer(v)))
            if test != state:
                print('Detected failure while %ssatisfying SemSel("%s") with "%s"'
                      % ('' if state else 'not ', sel, v))
            func(test)

    def str_match_test(self, t, state=True):
        for l in t.splitlines():
            if l.strip():
                s, v = l.split(':')
                vs = v.split('^')
                if vs[0].strip():
                    self.matches(state, s.strip(), vs[0].strip().split(', '))
                if len(vs) == 2:
                    self.matches(not state, s.strip(), vs[1].strip().split(', '))

    def test_lower(self):
        t = '''
            <2.2.0:  2.1.3, 1.0.1, 2.2.0-1 ^ 2.2.0, 2.2.0+s, 3.1.2
            <=2.2.0: 2.2.0-1, 2.2.0        ^ 2.2.0+s, 3.1.2
        '''
        self.str_match_test(t)

    def test_greater(self):
        t = '''
            >2.2.0:  3.1.3, 2.3.1, 2.2.1, 2.2.0+1 ^ 2.2.0, 2.2.0-pr, 1.0.2
            >=2.2.0: 2.2.0+1, 2.2.0               ^ 2.2.0-pr, 0.0.1
        '''
        self.str_match_test(t)

    def test_equal(self):  # and unequal
        t = '''
            =2.2.0:       2.2.0                     ^ 2.2.0-2
            =2.1.0-9+8.7: 2.1.0-9+8.7               ^ 0.0.1
            !=2.2.0:      2.1.0, 2.2.0-pre.3, 2.2.1 ^ 2.2.0
        '''
        self.str_match_test(t)

    def test_satisfy(self):  # and unsatisfy
        t = '''
            2.2.0:        2.2.0, 2.2.0-2, 2.2.0+23 ^ 2.2.1-
            !2.2.0:       2.2.1-                   ^ 2.2.0, 2.2.0-2, 2.2.0+23
            2.2.0-as:     2.2.0-as                 ^ 2.2.0, 2.2.0-2+3
            !2.2.0-as:    2.2.0, 2.2.0-2+3         ^ 2.2.0-as
        '''
        self.str_match_test(t)

    def test_and(self):
        t = '''
            >=2.2.0 <2.4.0:                  2.2.0+123, 2.3.0-some ^ 2.0.0, 2.2.0-pre, 2.4.0, 3.0.0
            >=1.0.0 <2.1.0-some-pre !=2.0.9: 1.0.2, 2.1.0-nothing  ^ 2.0.9, 2.1.0, 0.9.0
        '''
        self.str_match_test(t)

    def test_or(self):
        t = '''
            >1.0.0 || 0.0.3:                       0.0.3, 2.3.4-1 ^ 0.0.4
            ~1 || 0.0.3 || <0.0.2 >0.0.1 || 2.0.x: 0.0.3, 0.0.1+, 2.0.1+d, 1.1.1-1+1 ^ 0.0.7
        '''
        self.str_match_test(t)

    def test_fuzzy(self):
        t = '''
            ~2:     2.2.1, 2.2.0+1, 2.0.0-, 2.99999.1 ^ 1.0.0, 3.0.0-
            ~2.1:   2.1.0+1, 2.1.0, 2.1.999999+78 ^ 2.0.0, 2.2.0-
            ~3.1.1: 3.1.1, 3.1.88 ^ 3.1.0+b.12, 3.2.0-
            ~:      0.0.0-, 1.0.0, 12.312321.21-134y+ry2q3as
        '''
        self.str_match_test(t)

    def test_xrange(self):
        t = '''
            2.x:   2.2.1, 2.2.0+1, 2.0.0-, 2.99999.1 ^ 1.0.2, 3.0.0-
            2.x.x: 2.2.1, 2.2.0+1, 2.0.0-, 2.99999.1 ^ 1.0.2, 3.0.0-
            2.1.*: 2.1.0+1, 2.1.0, 2.1.999999+78 ^ 2.0.0, 2.2.0-
            *:     0.0.0-, 1.0.0, 12.312321.21-134y+ry2q3as
        '''
        self.str_match_test(t)


class GetItemTests(unittest.TestCase):
    def equals(self, what, to):
        self.assertEqual(what, to)

    def test_slice(self):
        s = SemVer("1.2.3-4.5+6")
        eq = lambda w, t: self.assertEqual(w, t)

        self.assertTrue(isinstance(s[:], tuple))
        eq(s[0:1], (1,))
        eq(s[0:2], (1, 2))
        eq(s[0:3], (1, 2, 3))
        eq(s[:4], (1, 2, 3, '4.5'))
        eq(s[:5], (1, 2, 3, '4.5', '6'))
        eq(s[3:5], ('4.5', '6'))

        eq(SemVer("1.2.3")[3:5], (None, None))
        eq(SemVer("1.2.3-+")[3:], ('', ''))

    def test_index(self):
        s = SemVer("1.2.3-4.5+6")

        self.assertEqual(s[0], 1)
        self.assertEqual(s[1], 2)
        self.assertEqual(s[2], 3)
        self.assertEqual(s[3], '4.5')
        self.assertEqual(s[-2], '4.5')
        self.assertEqual(s[4], '6')
        self.assertRaises(IndexError, lambda: s[6])
        self.assertRaises(IndexError, lambda: s[-6])
        self.assertRaises(TypeError, lambda: s['b'])

    def test_len(self):
        l = lambda s, r: self.assertEqual(len(SemVer(s)), r)

        l("1.2.3-4.5+6", 5)
        l("1.2.3+6", 5)
        l("1.2.3+", 5)
        l("1.2.3-4.5", 4)
        l("1.2.3-", 4)
        l("1.2.3", 3)

    def test_attr(self):
        s = SemVer("1.2.3-4.5+6")

        self.equals(s.major, 1)
        self.equals(s.minor, 2)
        self.equals(s.patch, 3)
        self.equals(s.prerelease, '4.5')
        self.equals(s.build, '6')
        self.assertRaises(AttributeError, lambda: s.bb)

if __name__ == '__main__':
    unittest.main()
