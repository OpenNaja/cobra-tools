"""Binary layouts and pointer memory must survive XML format changes."""

import base64
from io import BytesIO
import xml.etree.ElementTree as ET

from generated.formats.base.basic import Char
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ppuipkg.structs.Base64ArrayPointer import Base64ArrayPointer
from generated.formats.ppuipkg.structs.Ppuipkgfile import Ppuipkgfile
from generated.formats.ppuipkg.structs.PPUIPKGRoot import PPUIPKGRoot


def test_base64_pointer_writes_the_original_array_bytes(context, payload, decode_pointer, memory_loader):
	original = ArrayPointer(context, len(payload), Char)
	original.read_template(BytesIO(payload))
	modified = decode_pointer(base64.b64encode(payload).decode("ascii"), len(payload))
	outputs = []
	for pointer in (original, modified):
		loader = memory_loader()
		pointer.io_start = 16
		pointer.write_ptr(loader, loader.pool)
		outputs.append((loader.pool.data.getvalue(), loader.fragments, loader.pool.size_map))
	assert outputs[0] == outputs[1]
	assert outputs[1][0] == payload
	assert outputs[1][1] == [(16, 0)]


def test_pointer_and_file_layouts_are_unchanged(context):
	pointer = Base64ArrayPointer(context, 0, Char)
	assert pointer.get_size(pointer, context) == 8
	file = Ppuipkgfile(context)
	file.file_size = 3
	stream = BytesIO()
	Ppuipkgfile.to_stream(file, stream, context)
	assert stream.getvalue() == b"\x00" * 8 + (3).to_bytes(8, "little") + b"\x00" * 8
	assert len(stream.getvalue()) == 24


def test_root_count_offsets_are_unchanged(package_xml, load_package):
	instance = load_package(package_xml())
	stream = BytesIO()
	PPUIPKGRoot.to_stream(instance, stream, instance.context)
	root_bytes = stream.getvalue()
	assert len(root_bytes) == 40
	assert int.from_bytes(root_bytes[8:16], "little") == 1
	assert int.from_bytes(root_bytes[24:32], "little") == 1


def test_empty_arrays_keep_the_empty_root_layout(load_package):
	instance = load_package(ET.fromstring("<PPUIPKGRoot><basic_path/><files/><icondata/></PPUIPKGRoot>"))
	assert instance.files_count == 0
	assert instance.icondata_count == 0
	stream = BytesIO()
	PPUIPKGRoot.to_stream(instance, stream, instance.context)
	assert stream.getvalue() == bytes(40)


def test_legacy_and_current_xml_write_identical_memory(package_xml, load_package, package_memory, payload):
	legacy = package_xml(container="types", package_field="asset_package", count_name="file_count", encoding=None)
	current = package_xml()
	legacy_output = package_memory(load_package(legacy))
	current_output = package_memory(load_package(current))
	assert legacy_output == current_output
	data, links, sizes = current_output
	assert payload in data
	assert b"uigameface/img/characterportraits_01.png\x00" in data
	assert b"UserInterfaceFrontendC0_0\x00" in data
	assert len(links) == 7
	assert {0, 16, 32}.issubset({offset for offset, target in links})
	assert sizes
