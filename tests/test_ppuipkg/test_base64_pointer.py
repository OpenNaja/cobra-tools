"""Base64 XML conversion and validation for byte-array pointers."""

import base64
from io import BytesIO
from types import SimpleNamespace
import xml.etree.ElementTree as ET

import numpy as np
import pytest

from generated.formats.base.basic import Char, Uint
from generated.formats.ppuipkg.structs.Base64ArrayPointer import Base64ArrayPointer


def test_binary_xml_roundtrip_preserves_every_byte(context, payload, encode_pointer, decode_pointer):
	pointer = Base64ArrayPointer(context, len(payload), Char)
	pointer.read_template(BytesIO(payload))
	assert pointer.data.dtype == np.dtype("int8")
	assert pointer.data.tobytes() == payload

	xml = encode_pointer(pointer)
	assert xml.get("encoding") == "base64"
	assert xml.text == base64.b64encode(payload).decode("ascii")
	decoded = decode_pointer(xml.text, len(payload))
	assert decoded.data.tobytes() == payload
	assert decoded.data.flags.writeable


@pytest.mark.parametrize("container", [bytes, bytearray, memoryview], ids=["bytes", "bytearray", "memoryview"])
def test_export_accepts_byte_containers(context, payload, encode_pointer, container):
	pointer = Base64ArrayPointer(context, len(payload), Char)
	pointer.data = container(payload)
	assert base64.b64decode(encode_pointer(pointer).text, validate=True) == payload


def test_wrapped_base64_and_pool_metadata_survive(decode_pointer, encode_pointer):
	pointer = decode_pointer("\n Q U J D \t\n", 3, pool_type="5")
	assert pointer.data.tobytes() == b"ABC"
	assert pointer.pool_type == 5
	output = encode_pointer(pointer)
	assert output.get("pool_type") == "5"
	assert output.text == "QUJD"


@pytest.mark.parametrize("encoding", [None, "decimal"], ids=["unmarked", "decimal"])
def test_legacy_signed_and_unsigned_decimal_bytes_remain_readable(decode_pointer, encode_pointer, encoding):
	pointer = decode_pointer("-128 -1 0 127 128 255", 6, encoding=encoding)
	assert pointer.data.tobytes() == b"\x80\xff\x00\x7f\x80\xff"
	assert encode_pointer(pointer).get("encoding") == "base64"


def test_empty_content_roundtrip(decode_pointer, encode_pointer):
	pointer = decode_pointer("", 0)
	assert pointer.data.tobytes() == b""
	assert encode_pointer(pointer).get("encoding") == "base64"
	assert encode_pointer(pointer).text == ""


def test_missing_empty_pointer_is_allowed(context):
	pointer = Base64ArrayPointer.from_xml(
		SimpleNamespace(context=context), ET.Element("ppuipkgfile"), "file_content", 0, Char
	)
	assert pointer.data.tobytes() == b""


def test_missing_nonempty_pointer_is_rejected(context):
	with pytest.raises(ValueError, match="Missing file_content"):
		Base64ArrayPointer.from_xml(
			SimpleNamespace(context=context), ET.Element("ppuipkgfile"), "file_content", 1, Char
		)


@pytest.mark.parametrize("text", ["!!!!", "A===", "QUJ", "\u2603"], ids=["alphabet", "padding", "truncated", "unicode"])
def test_invalid_base64_is_rejected(decode_pointer, text):
	with pytest.raises(ValueError, match="Invalid Base64"):
		decode_pointer(text, 3)


@pytest.mark.parametrize("text", ["256", "-129", "65 invalid 66"], ids=["overflow", "underflow", "not_integer"])
def test_invalid_decimal_is_rejected(decode_pointer, text):
	with pytest.raises(ValueError, match="Decimal|decimal"):
		decode_pointer(text, 1, encoding=None)


def test_unsupported_encoding_is_rejected(decode_pointer):
	with pytest.raises(ValueError, match="Unsupported"):
		decode_pointer("414243", 3, encoding="hex")


def test_decoded_size_mismatch_is_rejected(decode_pointer):
	with pytest.raises(ValueError, match="file_size is 4"):
		decode_pointer("QUJD", 4)


def test_export_size_mismatch_is_rejected(decode_pointer, encode_pointer):
	pointer = decode_pointer("QUJD", 3)
	pointer.arg = 2
	with pytest.raises(ValueError, match="file_size is 2"):
		encode_pointer(pointer)


def test_nonbyte_template_is_rejected(context, encode_pointer):
	pointer = Base64ArrayPointer(context, 1, Uint)
	with pytest.raises(TypeError, match="one-byte"):
		encode_pointer(pointer)


def test_nested_content_is_rejected(context):
	parent = ET.fromstring("<ppuipkgfile><file_content><invalid/></file_content></ppuipkgfile>")
	with pytest.raises(ValueError, match="child elements"):
		Base64ArrayPointer.from_xml(
			SimpleNamespace(context=context), parent, "file_content", 0, Char
		)
