"""Custom XML readers and writers must survive source regeneration."""

import base64
import importlib
import shutil
import sys
import xml.etree.ElementTree as ET

from codegen import Config, ExitCode
from codegen.__main__ import generate_classes


def test_regenerated_classes_keep_base64_and_legacy_readers(
	tmp_path, monkeypatch, repo_root, context, package_xml, payload,
):
	"""Regenerate into a temporary package so existing imports stay intact."""
	source = tmp_path / "source"
	source.mkdir()
	for path in (repo_root / "source").iterdir():
		if path.is_file() and path.suffix in (".py", ".pyi"):
			shutil.copy2(path, source / path.name)
	for format_name in ("base", "ovl_base", "ppuipkg"):
		shutil.copytree(
			repo_root / "source" / "formats" / format_name,
			source / "formats" / format_name,
		)

	package_name = "ppuipkg_test_generated"
	config = Config(
		root_dir=str(tmp_path), src_dir="source", gen_dir=package_name,
		write_stubs=False, abort_on_error=True, concurrent=False,
	)
	monkeypatch.chdir(tmp_path)
	assert generate_classes(config) == ExitCode.SUCCESS
	monkeypatch.syspath_prepend(str(tmp_path))

	try:
		module = importlib.import_module(f"{package_name}.formats.ppuipkg.structs.PPUIPKGRoot")
		root_type = module.PPUIPKGRoot
		instance = root_type(context)
		legacy = package_xml(
			container="types", package_field="asset_package", count_name="file_count", encoding=None,
		)
		root_type._from_xml(instance, legacy)
		assert instance.files_count == 1
		assert instance.icondata_count == 1
		assert instance.files.data[0].file_content.data.tobytes() == payload
		assert instance.icondata.data[0].ovs.data == "UserInterfaceFrontendC0_0"

		exported = ET.Element("PPUIPKGRoot")
		root_type._to_xml(instance, exported, False)
		assert exported.find("types") is None
		assert exported.findtext("icondata/userinterfaceicondata/ovs") == "UserInterfaceFrontendC0_0"
		content = exported.find("files/ppuipkgfile/file_content")
		assert content.get("encoding") == "base64"
		assert base64.b64decode(content.text, validate=True) == payload
	finally:
		for name in list(sys.modules):
			if name == package_name or name.startswith(package_name + "."):
				del sys.modules[name]
