import pytest

from codegen.Enum import Enum
from codegen.Bitfield import Bitfield

from .test_xml_parser import config, xml_parser, xml_test1


@pytest.mark.only_for_enums(["ExampleEnum"])
def test_enum_parsing(xml_test1, config, enum_elem):
	enum = Enum(xml_test1, enum_elem, config)
	assert enum.class_name == "ExampleEnum"
	assert enum.class_basename == "BaseEnum"
	assert "Ushort" in enum.imports.imports  # from storage="ushort"

	# Check that options are present
	option_names = {opt.attrib['name'] for opt in enum.struct}
	assert "STATUS_ACTIVE" in option_names
	assert "STATUS_DELETED" in option_names


@pytest.mark.only_for_enums(["ExampleFlags"])
def test_bitfield_parsing(xml_test1, config, enum_elem):
	bitfield = Bitfield(xml_test1, enum_elem, config)
	assert bitfield.class_name == "ExampleFlags"
	assert "Uint" in bitfield.imports.imports     # from storage="uint", uint_4
	assert "Ushort" in bitfield.imports.imports   # from ushort_6
	assert "Bool" in bitfield.imports.imports     # from bool_0
	assert bitfield.class_basename == "BasicBitfield"

	# Check that members are present
	member_names = {mem.attrib['name'] for mem in bitfield.struct}
	assert "bool_0" in member_names
	assert "uint_4" in member_names


@pytest.mark.only_for_enums(["ExampleFlags"])
def test_bitfield_get_mask(xml_test1, config, enum_elem):
	bitfield = Bitfield(xml_test1, enum_elem, config)
	bitfield.get_mask()  # This method modifies the element in place

	bool_0 = next(m for m in bitfield.struct if m.attrib['name'] == 'bool_0')
	uint_4 = next(m for m in bitfield.struct if m.attrib['name'] == 'uint_4')

	# bool_0: pos=0, width=1 -> mask = 0x1
	assert bool_0.attrib['mask'] == hex(0b1)

	# uint_4: pos=4, width=4 -> mask = 0xF0
	assert uint_4.attrib['mask'] == hex(0b11110000)
