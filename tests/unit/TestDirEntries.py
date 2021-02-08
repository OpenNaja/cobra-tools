import unittest
from generated.formats.ovl import OvlFile

class TestDirEntries(unittest.TestCase):

	# load an empty ovl file for each test case
	def setUp(self):
		self.ovlfile = OvlFile()
		self.ovlfile.load('tests/Data/empty.ovl')

	def test_ovl_no_dirs(self):
		self.assertEqual(len(self.ovlfile.dirs), 0, "Should have no dirs")

	def test_inject_dir(self):
		self.assertEqual(len(self.ovlfile.dirs), 0, "Should have no dirs")

		self.ovlfile.inject_dir('test1')
		self.assertEqual(len(self.ovlfile.dirs), 1, "Should have one dir entry")
		self.assertEqual(self.ovlfile.dirs[0].name, "test1", "should have dir entry 1 name 'test1'")

		self.ovlfile.inject_dir('test2')
		self.assertEqual(len(self.ovlfile.dirs), 2, "Should have two dir entry")
		self.assertEqual(self.ovlfile.dirs[1].name, "test2", "should have dir entry 2 as 'test2'")

		# try adding a existing dir entry
		self.ovlfile.inject_dir('test1')
		self.assertEqual(len(self.ovlfile.dirs), 2, "Should have two dir entry")

	def test_remove_dir(self):
		self.assertEqual(len(self.ovlfile.dirs), 0, "Should have no dirs")

		self.ovlfile.inject_dir('test1')
		self.assertEqual(len(self.ovlfile.dirs), 1, "Should have one dir entry")
		self.assertEqual(self.ovlfile.dirs[0].name, "test1", "should have dir entry 1 as 'test1'")

		self.ovlfile.inject_dir('test2')
		self.assertEqual(len(self.ovlfile.dirs), 2, "Should have two dir entry")
		self.assertEqual(self.ovlfile.dirs[1].name, "test2", "should have dir entry 2 as 'test2'")

		# remove existing dir entry
		self.ovlfile.remove_dir('test1')
		self.assertEqual(len(self.ovlfile.dirs), 1, "Should have one dir entry")
		self.assertEqual(self.ovlfile.dirs[0].name, "test2", "should have dir entry 1 as 'test2'")

		# remove non-existing dir
		self.ovlfile.remove_dir('test3')
		self.assertEqual(len(self.ovlfile.dirs), 1, "Should have one dir entry")
		self.assertEqual(self.ovlfile.dirs[0].name, "test2", "should have dir entry 1 as 'test2'")


	def test_rename_dir(self):
		self.assertEqual(len(self.ovlfile.dirs), 0, "Should have no dirs")

		self.ovlfile.inject_dir('test1')
		self.assertEqual(len(self.ovlfile.dirs), 1, "Should have one dir entry")
		self.assertEqual(self.ovlfile.dirs[0].name, "test1", "should have dir entry 1 as 'test1'")

		self.ovlfile.inject_dir('test2')
		self.assertEqual(len(self.ovlfile.dirs), 2, "Should have two dir entry")
		self.assertEqual(self.ovlfile.dirs[1].name, "test2", "should have dir entry 2 as 'test2'")

		# try renaming an existing dir entry
		self.ovlfile.rename_dir('test1', 'test3')
		self.assertEqual(len(self.ovlfile.dirs), 2, "Should have two dir entry")
		self.assertEqual(self.ovlfile.dirs[0].name, "test3", "should have dir entry 1 as 'test3'")

		# try renaming a missing dir entry
		self.ovlfile.rename_dir('test1', 'test5')
		self.assertEqual(len(self.ovlfile.dirs), 2, "Should have two dir entry")
		self.assertEqual(self.ovlfile.dirs[0].name, "test3", "should have dir entry 1 as 'test3'")

	"""
	def test_bad_type(self):
		with self.assertRaises(TypeError):
			self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")
	"""

if __name__ == '__main__':
    unittest.main()