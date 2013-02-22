import unittest
from semveritem import SemVerItem


class ItemTests(unittest.TestCase):

	def setUp(self):
		self.item1 = SemVerItem
		self.item2 = SemVerItem

	def test_equal(self):
		self.assertEqual(self.item1("0.0.0-alpha"), self.item1("0.0.0-alpha"))

if __name__ == '__main__':
	unittest.main()
