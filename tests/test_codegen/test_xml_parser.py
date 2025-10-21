import pytest
import os
from unittest.mock import Mock

from codegen.XmlParser import XmlParser

from .conftest import loaded_xml_parser

# Fixture aliases for each source directory to test
xml_test1 = loaded_xml_parser
# TODO:
# New source fixtures for schema validation failure, parsing failure

# Fixture to provide a basic config object
@pytest.fixture
def config(tmp_path):
	# Mocking the Config class from the codegen library
	cfg = Mock()
	cfg.gen_dir = str(tmp_path / "gen")
	cfg.src_dir = str(tmp_path / "src")
	cfg.root_dir = str(tmp_path)
	cfg.write_stubs = True
	os.makedirs(cfg.gen_dir, exist_ok=True)
	os.makedirs(cfg.src_dir, exist_ok=True)
	return cfg


# Fixture to provide an initialized XmlParser
@pytest.fixture
def xml_parser(config):
	return XmlParser("test1", config)


def test_xml_parser_init(xml_parser):
	"""Tests the state of the XmlParser right after initialization."""
	assert xml_parser.format_name == "test1"
	# Versions and basics should be None before load_xml is called
	assert xml_parser.versions is None
	assert xml_parser.basics is None


def test_xml_parser_after_load(xml_test1):
	"""Tests the state of the XmlParser after load_xml has been called."""
	# The xml_test1 fixture calls load_xml, so these should now be initialized
	assert xml_test1.versions is not None
	assert xml_test1.basics is not None


def test_token_reading(xml_test1):
	# Checks if tokens from base.xml and test1.xml were read
	assert len(xml_test1.tokens) > 0
	# Check for a specific token from base.xml
	operator_token_found = any(
		any(sub_token[0] == "#ADD#" for sub_token in tokens)
		for tokens, _ in xml_test1.tokens
	)
	assert operator_token_found
	# Check for a specific token from test1.xml
	verexpr_token_found = any(
		any(sub_token[0] == "#V1#" for sub_token in tokens)
		for tokens, _ in xml_test1.tokens
	)
	assert verexpr_token_found


def test_path_dict_population(xml_test1):
	# Test if paths for types defined in test1.xml are correctly generated
	assert "ExampleEnum" in xml_test1.path_dict
	assert "ExampleFormatRoot" in xml_test1.path_dict
	expected_path_part = os.path.join("formats", "test1", "enums", "ExampleEnum")
	assert expected_path_part in xml_test1.path_dict["ExampleEnum"]


def test_tag_dict_population(xml_test1):
	assert xml_test1.tag_dict.get("exampleenum") == "enum"
	assert xml_test1.tag_dict.get("exampleflags") == "bitfield"
	assert xml_test1.tag_dict.get("examplebitstruct") == "bitstruct"
	assert xml_test1.tag_dict.get("structwithbasictypes") == "struct"
	assert xml_test1.tag_dict.get("structwithconditionalfields") == "compound"


def test_xinclude_processing(xml_test1):
	# Check if a type from an included file (ovl_base.xml) is present
	assert "MemStruct" in xml_test1.path_dict
	# Check if a type from a nested include (base.xml) is present
	assert "Uint" in xml_test1.basics.integrals


def test_apply_conventions(xml_test1):
	# TODO: Expand assertions
	assert "StructSnakeCase" in xml_test1.path_dict
