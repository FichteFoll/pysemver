import unittest

from semver import SemVer

SV = SemVer()


class TestParseFunctions(unittest.TestCase):

	def setUp(self):
		pass

	def test_parse(self):
		pass


class TestComparisonFunctions(unittest.TestCase):

	def setUp(self):
		self.data = [
				["0.0.0", "0.0.0food"],
				["0.0.1", "0.0.0"],
				["1.0.0", "0.9.9"],
				["0.10.0", "0.9.0"],
				["0.99.0", "0.10.0"],
				["2.0.0", "1.2.3"],
				["v0.0.0", "0.0.0foo"],
				["v0.0.1", "0.0.0"],
				["v1.0.0", "0.9.9"],
				["v0.10.0", "0.9.0"],
				["v0.99.0", "0.10.0"],
				["v2.0.0", "1.2.3"],
				["0.0.0", "v0.0.0foo"],
				["0.0.1", "v0.0.0"],
				["1.0.0", "v0.9.9"],
				["0.10.0", "v0.9.0"],
				["0.99.0", "v0.10.0"],
				["2.0.0", "v1.2.3"],
				["1.2.3", "1.2.3-asdf"],
				["1.2.3-4", "1.2.3"],
				["1.2.3-4-foo", "1.2.3"],
				["1.2.3-5", "1.2.3-5-foo"],
				["1.2.3-5", "1.2.3-4"],
				["1.2.3-5-foo", "1.2.3-5-Foo"],
				["3.0.0", "2.7.2+"]
				]

	def test_gt(self):
		pass

	def test_lt(self):
		pass

	def test_eq(self):
		pass

	def test_neq(self):
		pass

	def test_cmp(self):
		pass


# SV.gt(v[0], v[1]), "gt('" + v[0] + "', '" + v[1] + "')"
# SV.lt(v[1], v[0]), "lt('" + v[1] + "', '" + v[0] + "')"
# not SV.gt(v[1], v[0]), "!gt('" + v[1] + "', '" + v[0] + "')"
# not SV.lt(v[0], v[1]), "!lt('" + v[0] + "', '" + v[1] + "')"
# SV.eq(v[0], v[0]), "eq('" + v[0] + "', '" + v[0] + "')"
# SV.eq(v[1], v[1]), "eq('" + v[1] + "', '" + v[1] + "')"
# SV.neq(v[0], v[1]), "neq('" + v[0] + "', '" + v[1] + "')"
# SV.cmp(v[1], "==", v[1]), "cmp('" + v[1] + "'' == '" + v[1] + "')"
# SV.cmp(v[0], ">=", v[1]), "cmp('" + v[0] + "'' >= '" + v[1] + "')"
# SV.cmp(v[1], "<=", v[0]), "cmp('" + v[1] + "'' <= '" + v[0] + "')"
# SV.cmp(v[0], "!=", v[1]), "cmp('" + v[1] + "'' != '" + v[1] + "')"
