import os
import copy
import logging
from pathlib import Path

import pytest
from pytest import FixtureRequest, TempPathFactory

from generated.formats.ovl import OvlFile, get_game, set_game


@pytest.fixture(autouse=True)
def no_logs_gte_error(caplog):
	"""Fail test if logging.ERROR or higher"""
	yield
	errors = [record for record in caplog.get_records('call') if record.levelno >= logging.ERROR]
	assert not errors


@pytest.fixture(scope="module")
def tmp(tmp_path_factory: TempPathFactory):
	path = tmp_path_factory.mktemp("ovls")
	return path


OVLInfo = tuple[OvlFile, str, str]
FileInfo = tuple[str, int]


class TestOVLSaveCreate:
	"""create a new empty OVL, save the ovl with diff formats, and try loading it again"""

	@pytest.fixture(scope="class", params=["Planet Zoo", "Planet Coaster",
					"Jurassic World Evolution", "Jurassic World Evolution 2"])
	def ovl_file(self, request: FixtureRequest, tmp: Path) -> OVLInfo:
		ovl = OvlFile()
		ovl.load_hash_table()
		game = str(request.param)
		abbrev = "".join(item[0].upper() for item in game.split())
		filepath = tmp.with_name(f"{abbrev}.ovl")
		return ovl, game, str(filepath)

	@pytest.fixture(scope="class", params=["tests/Files/",])
	def files(self, request: FixtureRequest) -> FileInfo:
		dir_path = str(request.param)
		count = len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])
		return dir_path, count

	def test_ovl_save(self, ovl_file: OVLInfo):
		ovl, game, filepath = ovl_file
		set_game(ovl, game)
		context = copy.copy(ovl.context)
		sorted_loaders = context.sorted_loaders.copy()
		ovl.save(filepath)
		ovl.load(filepath)
		assert game == ovl.game
		assert context.version == ovl.context.version
		assert context.user_version == ovl.context.user_version
		assert sorted_loaders == ovl.context.sorted_loaders 

	def test_ovl_create(self, ovl_file: OVLInfo, files: FileInfo):
		ovl, game, filepath = ovl_file
		dir_path, file_count = files
		set_game(ovl, game)
		ovl.create(dir_path)
		context = copy.copy(ovl.context)
		sorted_loaders = context.sorted_loaders.copy()
		ovl.save(filepath)
		ovl.load(filepath)
		assert game == ovl.game
		assert ovl.context.sorted_loaders == sorted_loaders
