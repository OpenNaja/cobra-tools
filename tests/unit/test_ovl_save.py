import os
import pytest
from generated.formats.ovl import OvlFile, get_game, set_game


class TestOVLSave:
	"""create a new empty OVL, save the ovl with diff formats, and try loading it again"""

	@pytest.fixture(scope="class")
	def ovl_file(self):
		if not os.path.exists("tests/tmp"):
			os.makedirs("tests/tmp")
		return OvlFile()

	def test_ovl_save_pc(self, ovl_file: OvlFile):
		game = "Planet Coaster"
		file = 'tests/tmp/pc.ovl'
		set_game(ovl_file.context, game)
		set_game(ovl_file, game)
		ovl_file.save(file)
		ovl_file.load(file)
		assert game == get_game(ovl_file)[0].value

	def test_ovl_save_pz(self, ovl_file: OvlFile):
		game = "Planet Zoo"
		file = 'tests/tmp/pz.ovl'
		set_game(ovl_file.context, game)
		set_game(ovl_file, game)
		ovl_file.save(file)
		ovl_file.load(file)
		assert game == get_game(ovl_file)[0].value

	def test_ovl_save_jwe1(self, ovl_file: OvlFile):
		game = "Jurassic World Evolution"
		file = 'tests/tmp/jwe.ovl'
		set_game(ovl_file.context, game)
		set_game(ovl_file, game)
		ovl_file.save(file)
		ovl_file.load(file)
		assert game == get_game(ovl_file)[0].value

	def test_ovl_save_jwe2(self, ovl_file: OvlFile):
		game = "Jurassic World Evolution 2"
		file = 'tests/tmp/jwe2.ovl'
		set_game(ovl_file.context, game)
		set_game(ovl_file, game)
		ovl_file.save(file)
		ovl_file.load(file)
		assert game != get_game(ovl_file)[0].value
