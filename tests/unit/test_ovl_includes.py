import filecmp
import pytest
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


class TestOVLIncludes:

	@pytest.fixture(scope="class")
	def ovl_file_includes(self) -> list[str]:
		includes = [
			"Animals\AssetPackagesExtrasList",
			"AssetPackagesExtrasList",
			"Audio\Audio",
			"Characters\Main_SmallResources",
			"Environment\Main_SmallResources",
			"Prefabs\Prefabs"
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

	def test_ovl_save_included_ovls(self, ovl_file: OvlFile) -> None:
		ovl_file.save_included_ovls("tests/tmp/ovls.include")
		result = filecmp.cmp("tests/ovldata/OVLIncludes/ovls.include", "tests/tmp/ovls.include")
		assert result is True

	def test_ovl_load_included_ovls(self, empty_ovl_file: OvlFile) -> None:
		# Ensure empty OVL is PZ for later file comparison
		assert get_game(empty_ovl_file.context)[0].value == "Planet Zoo"
		empty_ovl_file.load_included_ovls("tests/ovldata/OVLIncludes/ovls.include")
		empty_ovl_file.save("tests/tmp/OVLIncludesPZ.ovl")
		result = filecmp.cmp("tests/ovldata/OVLIncludes/OVLIncludesPZ.ovl", "tests/tmp/OVLIncludesPZ.ovl")
		assert result is True

	def test_ovl_set_included_ovls(self, empty_ovl_file: OvlFile, ovl_file_includes: list[str]) -> None:
		# Ensure empty OVL is PZ for later file comparison
		assert get_game(empty_ovl_file.context)[0].value == "Planet Zoo"
		empty_ovl_file.included_ovl_names = ovl_file_includes
		empty_ovl_file.save("tests/tmp/OVLIncludesPZ.ovl")
		result = filecmp.cmp("tests/ovldata/OVLIncludes/OVLIncludesPZ.ovl", "tests/tmp/OVLIncludesPZ.ovl")
		assert result is True
