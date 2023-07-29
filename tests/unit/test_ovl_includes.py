import pytest
from generated.formats.ovl import OvlFile


class TestOVLIncludes:

	@pytest.fixture(scope="class")
	def empty_ovl_file(self):
		ovlfile = OvlFile()
		ovlfile.load('tests/ovldata/Empty/Empty.ovl')
		return ovlfile

	def test_ovl_no_included_ovls(self, empty_ovl_file):
		assert len(empty_ovl_file.included_ovls) == 0

	# TODO: Redo OVL Includes tests, this API no longer exists.
	#def test_inject_dir(self):
	#	self.assertEqual(len(self.ovlfile.included_ovls), 0, "Should have no included_ovls")

	#	self.ovlfile.included_ovl_names = ('test1.ovl',)
	#	self.assertEqual(len(self.ovlfile.included_ovls), 1, "Should have one included_ovl")
	#	self.assertEqual(self.ovlfile.included_ovls[0].name, "test1.ovl", "should have included_ovl 1 name 'test1'")

	#	self.ovlfile.included_ovl_names = ('test1.ovl', 'test2.ovl')
	#	self.assertEqual(len(self.ovlfile.included_ovls), 2, "Should have two included_ovl")
	#	self.assertEqual(self.ovlfile.included_ovls[1].name, "test2.ovl", "should have included_ovl 2 as 'test2'")

	#	# try adding a existing included_ovl
	#	self.ovlfile.included_ovl_names = ('test1.ovl', 'test2.ovl', 'test1.ovl')
	#	self.assertEqual(len(self.ovlfile.included_ovls), 2, "Should have two included_ovl")

	#def test_remove_dir(self):
	#	self.assertEqual(len(self.ovlfile.included_ovls), 0, "Should have no included_ovls")

	#	self.ovlfile.add_included_ovl('test1.ovl')
	#	self.assertEqual(len(self.ovlfile.included_ovls), 1, "Should have one included_ovl")
	#	self.assertEqual(self.ovlfile.included_ovls[0].name, "test1.ovl", "should have included_ovl 1 as 'test1'")

	#	self.ovlfile.add_included_ovl('test2.ovl')
	#	self.assertEqual(len(self.ovlfile.included_ovls), 2, "Should have two included_ovl")
	#	self.assertEqual(self.ovlfile.included_ovls[1].name, "test2.ovl", "should have included_ovl 2 as 'test2'")

	#	# remove existing included_ovl
	#	self.ovlfile.remove_included_ovl('test1.ovl')
	#	self.assertEqual(len(self.ovlfile.included_ovls), 1, "Should have one included_ovl")
	#	self.assertEqual(self.ovlfile.included_ovls[0].name, "test2.ovl", "should have included_ovl 1 as 'test2'")

	#	# remove non-existing dir
	#	self.ovlfile.remove_included_ovl('test3.ovl')
	#	self.assertEqual(len(self.ovlfile.included_ovls), 1, "Should have one included_ovl")
	#	self.assertEqual(self.ovlfile.included_ovls[0].name, "test2.ovl", "should have included_ovl 1 as 'test2'")

	#def test_rename_dir(self):
	#	self.assertEqual(len(self.ovlfile.included_ovls), 0, "Should have no included_ovls")

	#	self.ovlfile.add_included_ovl('test1.ovl')
	#	self.assertEqual(len(self.ovlfile.included_ovls), 1, "Should have one included_ovl")
	#	self.assertEqual(self.ovlfile.included_ovls[0].name, "test1.ovl", "should have included_ovl 1 as 'test1'")

	#	self.ovlfile.add_included_ovl('test2.ovl')
	#	self.assertEqual(len(self.ovlfile.included_ovls), 2, "Should have two included_ovl")
	#	self.assertEqual(self.ovlfile.included_ovls[1].name, "test2.ovl", "should have included_ovl 2 as 'test2'")

	#	# try renaming an existing included_ovl
	#	self.ovlfile.rename_included_ovl('test1.ovl', 'test3.ovl')
	#	self.assertEqual(len(self.ovlfile.included_ovls), 2, "Should have two included_ovl")
	#	self.assertEqual(self.ovlfile.included_ovls[0].name, "test3.ovl", "should have included_ovl 1 as 'test3'")

	#	# try renaming a missing included_ovl
	#	self.ovlfile.rename_included_ovl('test1.ovl', 'test5.ovl')
	#	self.assertEqual(len(self.ovlfile.included_ovls), 2, "Should have two included_ovl")
	#	self.assertEqual(self.ovlfile.included_ovls[0].name, "test3.ovl", "should have included_ovl 1 as 'test3'")

	"""
	def test_bad_type(self):
		with self.assertRaises(TypeError):
			self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")
	"""
