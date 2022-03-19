import unittest
from generated.formats.ovl import OvlFile, games, get_game, set_game, IGNORE_TYPES

# create a new empty OVL, save the ovl with diff formats, and try loading it again

class TestOVLCreate(unittest.TestCase):

	# load an empty ovl file for each test case
	def setUp(self):
		self.ovlfile = OvlFile()

	def test_ovl_save_pc(self):
		game = "Planet Coaster"
		file = 'tests/tmp/pc.ovl'
		set_game(self.ovlfile.context, game)
		set_game(self.ovlfile, game)
		self.ovlfile.create('tests/Files/')
		self.ovlfile.save(file, '')
		self.ovlfile.load(file)
		self.assertEqual(game, get_game(self.ovlfile)[0].value, "Should have the same game")

	def test_ovl_save_pz(self):
		game = "Planet Zoo 1.6+"
		file = 'tests/tmp/pz.ovl'
		set_game(self.ovlfile.context, game)
		set_game(self.ovlfile, game)
		self.ovlfile.create('tests/Files/')
		self.ovlfile.save(file, '')
		self.ovlfile.load(file)
		self.assertEqual(game, get_game(self.ovlfile)[0].value, "Should have the same game")

	def test_ovl_save_jwe1(self):
		game = "Jurassic World Evolution"
		file = 'tests/tmp/jwe.ovl'
		set_game(self.ovlfile.context, game)
		set_game(self.ovlfile, game)
		self.ovlfile.create('tests/Files/')
		self.ovlfile.save(file, '')
		self.ovlfile.load(file)
		self.assertEqual(game, get_game(self.ovlfile)[0].value, "Should have the same game")

	def test_ovl_save_jwe2(self):
		game = "Jurassic World Evolution 2"
		file = 'tests/tmp/jwe2.ovl'
		set_game(self.ovlfile.context, game)
		set_game(self.ovlfile, game)
		self.ovlfile.create('tests/Files/')
		self.ovlfile.save(file, '')
		self.ovlfile.load(file)
		self.assertEqual(game, get_game(self.ovlfile)[0].value, "Should have the same game")


if __name__ == '__main__':
	unittest.main()