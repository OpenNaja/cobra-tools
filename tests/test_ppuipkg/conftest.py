"""Shared XML and memory fixtures for PPUIPKG tests."""

import base64
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
import xml.etree.ElementTree as ET

import pytest

from generated.formats.base.basic import Char
from generated.formats.ppuipkg.structs.Base64ArrayPointer import Base64ArrayPointer
from generated.formats.ppuipkg.structs.PPUIPKGRoot import PPUIPKGRoot


class _MemoryPool:
	type = 2

	def __init__(self):
		self.data = BytesIO()
		self.offsets = set()
		self.size_map = {}
		self.offset_2_link = {}

	def align_write(self, data):
		self.data.seek(0, 2)
		return self.data, self.data.tell()


class _MemoryLoader:
	"""Supply the pool and links consumed by the real pointer writer."""

	def __init__(self):
		self.pool = _MemoryPool()
		self.fragments = []
		self.stack = {}
		self.dependencies = []

	def get_pool(self, pool_type):
		return self.pool

	def attach_frag_to_ptr(self, src_pool, src_offset, target_pool, target_offset):
		self.fragments.append((src_offset, target_offset))
		src_pool.offset_2_link[src_offset] = (target_pool, target_offset)


@pytest.fixture
def context():
	return SimpleNamespace()


@pytest.fixture
def payload():
	"""Include every byte value, embedded zeroes, and signed Char boundaries."""
	return bytes(range(256)) + b"\x00\xff\x80\x7f"


@pytest.fixture
def decode_pointer(context):
	def decode(text, size, encoding="base64", **attributes):
		parent = ET.Element("ppuipkgfile")
		elem = ET.SubElement(parent, "file_content", attributes)
		if encoding is not None:
			elem.set("encoding", encoding)
		elem.text = text
		return Base64ArrayPointer.from_xml(
			SimpleNamespace(context=context), parent, "file_content", size, Char
		)

	return decode


@pytest.fixture
def encode_pointer():
	def encode(pointer):
		parent = ET.Element("ppuipkgfile")
		Base64ArrayPointer.to_xml(
			parent, "file_content", pointer, pointer.arg, pointer.template, False
		)
		return parent.find("file_content")

	return encode


@pytest.fixture
def package_xml(payload):
	def make_xml(
		container="icondata", package_field="ovs", encoding="base64",
		count_name="files_count",
	):
		root = ET.Element("PPUIPKGRoot", {count_name: "1", "icondata_count": "1"})
		ET.SubElement(root, "basic_path").text = "uigameface"
		file = ET.SubElement(
			ET.SubElement(root, "files"), "ppuipkgfile", file_size=str(len(payload))
		)
		ET.SubElement(file, "file_name").text = "js/example.js"
		content = ET.SubElement(file, "file_content")
		if encoding == "base64":
			content.set("encoding", "base64")
			content.text = base64.b64encode(payload).decode("ascii")
		else:
			if encoding is not None:
				content.set("encoding", encoding)
			content.text = " ".join(str(value) for value in payload)
		icon = ET.SubElement(ET.SubElement(root, container), "userinterfaceicondata")
		ET.SubElement(icon, "image_name").text = "uigameface/img/characterportraits_01.png"
		ET.SubElement(icon, package_field).text = "UserInterfaceFrontendC0_0"
		return root

	return make_xml


@pytest.fixture
def load_package(context):
	def load(xml):
		instance = PPUIPKGRoot(context)
		return PPUIPKGRoot._from_xml(instance, xml)

	return load


@pytest.fixture
def memory_loader():
	return _MemoryLoader


@pytest.fixture
def package_memory(memory_loader):
	def write(instance):
		loader = memory_loader()
		PPUIPKGRoot.to_stream(instance, loader.pool.data, instance.context)
		instance.write_ptrs(loader, loader.pool)
		return loader.pool.data.getvalue(), loader.fragments, loader.pool.size_map

	return write


@pytest.fixture
def repo_root():
	return Path(__file__).resolve().parents[2]
