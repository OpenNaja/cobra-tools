import unittest
from generated.formats.ovl import OvlFile


class TestDirEntries(unittest.TestCase):

	# load an empty ovl file for each test case
	def setUp(self):
		self.ovlfile = OvlFile()
		self.ovlfile.load('tests/Data/empty.ovl')

	def test_ovl_no_included_ovls(self):
		self.assertEqual(len(self.ovlfile.included_ovls), 0, "Should have no included_ovls")

	def test_inject_dir(self):
		self.assertEqual(len(self.ovlfile.included_ovls), 0, "Should have no included_ovls")

		self.ovlfile.add_included_ovl('test1')
		self.assertEqual(len(self.ovlfile.included_ovls), 1, "Should have one included_ovl")
		self.assertEqual(self.ovlfile.included_ovls[0].name, "test1", "should have included_ovl 1 name 'test1'")

		self.ovlfile.add_included_ovl('test2')
		self.assertEqual(len(self.ovlfile.included_ovls), 2, "Should have two included_ovl")
		self.assertEqual(self.ovlfile.included_ovls[1].name, "test2", "should have included_ovl 2 as 'test2'")

		# try adding a existing included_ovl
		self.ovlfile.add_included_ovl('test1')
		self.assertEqual(len(self.ovlfile.included_ovls), 2, "Should have two included_ovl")

	def test_remove_dir(self):
		self.assertEqual(len(self.ovlfile.included_ovls), 0, "Should have no included_ovls")

		self.ovlfile.add_included_ovl('test1')
		self.assertEqual(len(self.ovlfile.included_ovls), 1, "Should have one included_ovl")
		self.assertEqual(self.ovlfile.included_ovls[0].name, "test1", "should have included_ovl 1 as 'test1'")

		self.ovlfile.add_included_ovl('test2')
		self.assertEqual(len(self.ovlfile.included_ovls), 2, "Should have two included_ovl")
		self.assertEqual(self.ovlfile.included_ovls[1].name, "test2", "should have included_ovl 2 as 'test2'")

		# remove existing included_ovl
		self.ovlfile.remove_included_ovl('test1')
		self.assertEqual(len(self.ovlfile.included_ovls), 1, "Should have one included_ovl")
		self.assertEqual(self.ovlfile.included_ovls[0].name, "test2", "should have included_ovl 1 as 'test2'")

		# remove non-existing dir
		self.ovlfile.remove_included_ovl('test3')
		self.assertEqual(len(self.ovlfile.included_ovls), 1, "Should have one included_ovl")
		self.assertEqual(self.ovlfile.included_ovls[0].name, "test2", "should have included_ovl 1 as 'test2'")

	def test_rename_dir(self):
		self.assertEqual(len(self.ovlfile.included_ovls), 0, "Should have no included_ovls")

		self.ovlfile.add_included_ovl('test1')
		self.assertEqual(len(self.ovlfile.included_ovls), 1, "Should have one included_ovl")
		self.assertEqual(self.ovlfile.included_ovls[0].name, "test1", "should have included_ovl 1 as 'test1'")

		self.ovlfile.add_included_ovl('test2')
		self.assertEqual(len(self.ovlfile.included_ovls), 2, "Should have two included_ovl")
		self.assertEqual(self.ovlfile.included_ovls[1].name, "test2", "should have included_ovl 2 as 'test2'")

		# try renaming an existing included_ovl
		self.ovlfile.rename_included_ovl('test1', 'test3')
		self.assertEqual(len(self.ovlfile.included_ovls), 2, "Should have two included_ovl")
		self.assertEqual(self.ovlfile.included_ovls[0].name, "test3", "should have included_ovl 1 as 'test3'")

		# try renaming a missing included_ovl
		self.ovlfile.rename_included_ovl('test1', 'test5')
		self.assertEqual(len(self.ovlfile.included_ovls), 2, "Should have two included_ovl")
		self.assertEqual(self.ovlfile.included_ovls[0].name, "test3", "should have included_ovl 1 as 'test3'")

	"""
	def test_bad_type(self):
		with self.assertRaises(TypeError):
			self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")
	"""

if __name__ == '__main__':
	unittest.main()