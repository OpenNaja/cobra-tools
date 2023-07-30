import os
import logging

import pytest
from pytest import FixtureRequest

from generated.formats.ovl import OvlFile, get_game, set_game


@pytest.fixture(autouse=True)
def no_logs_gte_error(caplog):
	"""Fail test if logging.ERROR or higher"""
	yield
	errors = [record for record in caplog.get_records('call') if record.levelno >= logging.ERROR]
	assert not errors


OVLInfo = tuple[OvlFile, str, str]
FileInfo = tuple[str, int]


class TestOVLSaveCreate:
	"""create a new empty OVL, save the ovl with diff formats, and try loading it again"""

	@pytest.fixture(scope="class", params=["Planet Zoo", "Planet Coaster",
					"Jurassic World Evolution", "Jurassic World Evolution 2"])
	def ovl_file(self, request: FixtureRequest) -> OVLInfo:
		if not os.path.exists("tests/tmp"):
			os.makedirs("tests/tmp")
		ovl = OvlFile()
		ovl.load_hash_table()
		game = str(request.param)
		abbrev = "".join(item[0].upper() for item in game.split())
		filename = f"tests/tmp/{abbrev}.ovl"
		return ovl, game, filename

	@pytest.fixture(scope="class", params=["tests/Files/",])
	def files(self, request: FixtureRequest) -> FileInfo:
		dir_path = str(request.param)
		count = len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])
		return dir_path, count

	def test_ovl_save(self, ovl_file: OVLInfo):
		ovl, game, filename = ovl_file
		context = ovl.context
		set_game(ovl.context, game)
		set_game(ovl, game)
		ovl.save(filename)
		ovl.load(filename)
		assert game == get_game(ovl)[0].value
		assert context == ovl.context

	def test_ovl_create(self, ovl_file: OVLInfo, files: FileInfo):
		ovl, game, filename = ovl_file
		dir_path, file_count = files
		set_game(ovl.context, game)
		set_game(ovl, game)
		ovl.create(dir_path)
		ovl.save(filename)
		ovl.load(filename)
		assert game == get_game(ovl)[0].value
		assert ovl.num_files == file_count
