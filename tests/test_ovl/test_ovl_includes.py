import filecmp
from pathlib import Path
import pytest
from pytest import TempPathFactory
from generated.formats.ovl import OvlFile, get_game


@pytest.fixture(scope="function")
def empty_ovl_file() -> OvlFile:
	ovlfile = OvlFile()
	ovlfile.load('tests/ovldata/Empty/EmptyPZ.ovl')
	return ovlfile


@pytest.fixture(scope="function")
def ovl_file() -> OvlFile:
	ovlfile = OvlFile()
	ovlfile.load('tests/ovldata/OVLIncludes/OVLIncludesPZ.ovl')
	return ovlfile


@pytest.fixture(scope="module")
def tmp(tmp_path_factory: TempPathFactory):
	path = tmp_path_factory.mktemp("includes")
	return path


class TestOVLIncludes:

	@pytest.fixture(scope="class")
	def ovl_file_includes(self) -> list[str]:
		includes = [
			R"Animals\AssetPackagesExtrasList",
			R"AssetPackagesExtrasList",
			R"Audio\Audio",
			R"Characters\Main_SmallResources",
			R"Environment\Main_SmallResources",
			R"Prefabs\Prefabs"
		]
		return includes

	def test_ovl_no_included_ovls(self, empty_ovl_file: OvlFile) -> None:
		assert len(empty_ovl_file.included_ovls) == 0
		assert len(empty_ovl_file.included_ovl_names) == 0
		assert empty_ovl_file.included_ovl_names == []

	def test_ovl_included_ovls(self, ovl_file: OvlFile, ovl_file_includes: list[str]) -> None:
		assert len(ovl_file.included_ovls) == 6
		assert len(ovl_file.included_ovl_names) == 6
		assert ovl_file.included_ovl_names == ovl_file_includes

	def test_ovl_save_included_ovls(self, ovl_file: OvlFile, tmp: Path) -> None:
		out = tmp.with_name("ovls.include")
		ovl_file.save_included_ovls(out)
		result = filecmp.cmp("tests/ovldata/OVLIncludes/ovls.include", out)
		assert result is True

	def test_ovl_load_included_ovls(self, empty_ovl_file: OvlFile, tmp: Path) -> None:
		out = tmp.with_name("OVLIncludesPZ.ovl")
		# Ensure empty OVL is PZ for later file comparison
		assert empty_ovl_file.game == "Planet Zoo"
		empty_ovl_file.load_included_ovls("tests/ovldata/OVLIncludes/ovls.include")
		empty_ovl_file.save(out)
		result = filecmp.cmp("tests/ovldata/OVLIncludes/OVLIncludesPZ.ovl", out)
		assert result is True

	def test_ovl_set_included_ovls(self, empty_ovl_file: OvlFile, ovl_file_includes: list[str], tmp: Path) -> None:
		out = tmp.with_name("OVLIncludesPZ.ovl")
		# Ensure empty OVL is PZ for later file comparison
		assert empty_ovl_file.game == "Planet Zoo"
		empty_ovl_file.included_ovl_names = ovl_file_includes
		empty_ovl_file.save(out)
		result = filecmp.cmp("tests/ovldata/OVLIncludes/OVLIncludesPZ.ovl", out)
		assert result is True
