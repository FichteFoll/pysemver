# import unittest

# from semver import SemVer

# SV = SemVer()


# class TestParseFunctions(unittest.TestCase):

# 	def setUp(self):
# 		self.data = [0, 0, 0, 'alpha', 'beta']

# 	def test_parse_basic(self):
# 		self.assertEqual(SV.parse("0.0.0-alpha+beta"), self.data)


# class TestGtFunction(unittest.TestCase):

# 	def setUp(self):
# 		self.data1 = "0.0.0-beta"
# 		self.data2 = "0.0.0-alpha"

# 	def test_gt_basic(self):
# 		self.assertTrue(SV.gt(self.data1, self.data2))

# if __name__ == '__main__':
# 	unittest.main()
