"""Legacy XML names, canonical exports, and package round trips."""

import base64
import xml.etree.ElementTree as ET

import pytest

from generated.formats.ppuipkg.structs.PPUIPKGRoot import PPUIPKGRoot


@pytest.mark.parametrize("container", ["types", "icondata"])
@pytest.mark.parametrize("package_field", ["asset_package", "assetPackage", "ovs"])
@pytest.mark.parametrize("encoding", [None, "decimal", "base64"], ids=["unmarked", "decimal", "base64"])
def test_legacy_and_current_xml_remain_readable(package_xml, load_package, payload, container, package_field, encoding):
	xml = package_xml(container=container, package_field=package_field, encoding=encoding)
	instance = load_package(xml)
	assert instance.files_count == 1
	assert instance.icondata_count == 1
	assert instance.files.data[0].file_content.data.tobytes() == payload
	assert instance.icondata.data[0].image_name.data == "uigameface/img/characterportraits_01.png"
	assert instance.icondata.data[0].ovs.data == "UserInterfaceFrontendC0_0"


@pytest.mark.parametrize("count_name", ["file_count", "files_count"])
def test_legacy_and_current_count_names_are_readable(package_xml, load_package, count_name):
	instance = load_package(package_xml(count_name=count_name))
	assert instance.files_count == 1
	assert len(instance.files.data) == 1
	assert not hasattr(instance, "file_count")


def test_input_xml_is_unchanged(package_xml, load_package):
	xml = package_xml(container="types", package_field="asset_package", count_name="file_count")
	original = ET.tostring(xml)
	instance = load_package(xml)
	assert ET.tostring(xml) == original
	assert not hasattr(instance, "file_count")
	assert not hasattr(instance, "types")


def test_export_uses_canonical_names_and_base64(package_xml, load_package, payload):
	instance = load_package(package_xml(container="types", package_field="asset_package", count_name="file_count"))
	exported = ET.Element("PPUIPKGRoot")
	PPUIPKGRoot._to_xml(instance, exported, False)
	assert exported.find("types") is None
	assert exported.find("icondata/userinterfaceicondata/asset_package") is None
	assert exported.find("icondata/userinterfaceicondata/assetPackage") is None
	assert exported.findtext("icondata/userinterfaceicondata/ovs") == "UserInterfaceFrontendC0_0"
	content = exported.find("files/ppuipkgfile/file_content")
	assert content.get("encoding") == "base64"
	assert base64.b64decode(content.text, validate=True) == payload
	assert exported.find("files/ppuipkgfile").get("file_size") == str(len(payload))
	assert "file_count" not in exported.attrib
	assert "files_count" not in exported.attrib
	assert "icondata_count" not in exported.attrib
	assert load_package(exported).icondata_count == 1


def test_debug_export_includes_canonical_counts(package_xml, load_package):
	instance = load_package(package_xml())
	exported = ET.Element("PPUIPKGRoot")
	PPUIPKGRoot._to_xml(instance, exported, True)
	assert exported.get("files_count") == "1"
	assert exported.get("icondata_count") == "1"
	assert "file_count" not in exported.attrib


def test_canonical_container_takes_precedence(package_xml, load_package):
	xml = package_xml()
	legacy = ET.SubElement(ET.SubElement(xml, "types"), "userinterfaceicondata")
	ET.SubElement(legacy, "image_name").text = "ignored.png"
	ET.SubElement(legacy, "asset_package").text = "ignored-package"
	instance = load_package(xml)
	assert instance.icondata_count == 1
	assert instance.icondata.data[0].ovs.data == "UserInterfaceFrontendC0_0"


def test_empty_canonical_container_takes_precedence(package_xml, load_package):
	xml = package_xml(container="types", package_field="asset_package")
	ET.SubElement(xml, "icondata")
	instance = load_package(xml)
	assert instance.icondata_count == 0
	assert len(instance.icondata.data) == 0


@pytest.mark.parametrize("legacy_name", ["asset_package", "assetPackage"])
def test_canonical_ovs_takes_precedence(package_xml, load_package, legacy_name):
	xml = package_xml()
	icon = xml.find("icondata/userinterfaceicondata")
	ET.SubElement(icon, legacy_name).text = "ignored-package"
	instance = load_package(xml)
	assert instance.icondata.data[0].ovs.data == "UserInterfaceFrontendC0_0"


def test_array_counts_follow_entries(package_xml, load_package):
	xml = package_xml(count_name="file_count")
	xml.set("file_count", "99")
	xml.set("files_count", "88")
	xml.set("icondata_count", "77")
	instance = load_package(xml)
	assert instance.files_count == len(instance.files.data) == 1
	assert instance.icondata_count == len(instance.icondata.data) == 1


def test_missing_counts_are_inferred(package_xml, load_package):
	xml = package_xml()
	xml.attrib.clear()
	instance = load_package(xml)
	assert instance.files_count == 1
	assert instance.icondata_count == 1


def test_package_file_roundtrip(tmp_path, context, package_xml, payload):
	legacy_path = tmp_path / "legacy.ppuipkg"
	current_path = tmp_path / "current.ppuipkg"
	xml = package_xml(container="types", package_field="asset_package", count_name="file_count", encoding=None)
	ET.ElementTree(xml).write(legacy_path, encoding="utf-8")
	instance = PPUIPKGRoot.from_xml_file(str(legacy_path), context)
	with PPUIPKGRoot.to_xml_file(instance, str(current_path)):
		pass
	reloaded = PPUIPKGRoot.from_xml_file(str(current_path), context)
	assert reloaded.files_count == 1
	assert reloaded.icondata_count == 1
	assert reloaded.files.data[0].file_content.data.tobytes() == payload
	assert reloaded.icondata.data[0].ovs.data == "UserInterfaceFrontendC0_0"
	assert ET.parse(current_path).find("types") is None
	assert ET.parse(current_path).findtext("icondata/userinterfaceicondata/ovs") == "UserInterfaceFrontendC0_0"
