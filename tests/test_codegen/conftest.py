
import pytest
import os
import xml.etree.ElementTree as ET

from codegen.XmlParser import XmlParser


STRUCT_TYPES = ("compound", "struct")
ENUM_TYPES = ("enum", "bitflags", "bitfield", "bitstruct")


# Paths for each named xml fixture
XML_FIXTURE_PATHS = {
	"xml_test1": os.path.join("xml1", "source", "formats", "test1", "test1.xml"),
}

@pytest.fixture(params=XML_FIXTURE_PATHS.keys())
def loaded_xml_parser(request, config, monkeypatch):
	"""
	A parametrized fixture that loads an XmlParser for each entry in
	the XML_FIXTURE_PATHS dictionary.
	"""
	fixture_name = request.param
	relative_path = XML_FIXTURE_PATHS[fixture_name]
	
	# Dynamically create a parser with the correct format name (e.g., "test1")
	format_name = fixture_name.replace("xml_", "")
	parser = XmlParser(format_name, config)

	# Construct the full path relative to the test file's directory
	test_dir = os.path.dirname(__file__)
	test_xml_path = os.path.join(test_dir, relative_path)
	
	# Add codegen directory to sys.path for imports
	codegen_path = os.path.abspath(os.path.join(test_dir, '..', '..', 'codegen'))
	monkeypatch.syspath_prepend(codegen_path)
	
	# Load the XML
	parser.load_xml(test_xml_path)
	return parser


@pytest.fixture
def active_parser(request: pytest.FixtureRequest):
	"""
	An internal fixture that finds which XML parser fixture (e.g., 'xml_test1')
	is active for the current test and returns the initialized instance of it.
	"""
	# Find the name of the active fixture by checking against our known list
	active_fixture_name = next((name for name in XML_FIXTURE_PATHS if name in request.fixturenames), None)
	
	if not active_fixture_name:
		pytest.fail(
			"A test using 'struct_elem' or 'enum_elem' must also request a known XML fixture, "
			f"e.g., {list(XML_FIXTURE_PATHS.keys())}"
		)

	return request.getfixturevalue(active_fixture_name)


def find_element_in_parser(parser: 'XmlParser', name: str, valid_tags: tuple = STRUCT_TYPES):
	"""
	Generic helper to find a named XML element by searching the tree
	within the provided XmlParser instance.
	"""
	if not hasattr(parser, 'root') or parser.root is None:
		raise AttributeError("The provided parser object must have a 'root' attribute containing the parsed XML.")

	for child in parser.root:
		if not isinstance(child.tag, str):
			continue  # lxml comments skip
		if child.tag in valid_tags and child.attrib.get('name') == name:
			parser.replace_tokens(child)
			parser.apply_conventions(child)
			return child
	return None


def parametrize_xml_elements(metafunc: pytest.Metafunc, fixture_name: str, xml_tags: tuple,
							 marker_name: str, xml_path: str) -> None:
	"""
	A generic helper to find, filter, and parametrize a fixture with XML elements
	from a specific XML file path.
	"""
	if fixture_name in metafunc.fixturenames:
		tree = ET.parse(xml_path)
		root = tree.getroot()
		all_names = [
			child.attrib.get("name") for child in root
			if child.tag in xml_tags and child.attrib.get("name")
		]
		
		marker = metafunc.definition.get_closest_marker(marker_name)
		target_names = marker.args[0] if marker else all_names
		
		metafunc.parametrize(fixture_name, target_names, indirect=True)


def pytest_generate_tests(metafunc: pytest.Metafunc):
	"""
	This hook parametrizes tests based on which XML fixture is used.
	"""
	# Find which XML fixture (e.g., 'xml_test1') the test function requests
	active_xml_fixture = next((name for name in XML_FIXTURE_PATHS if name in metafunc.fixturenames), None)

	# If the test doesn't use a known XML fixture, we don't need to parametrize
	if not active_xml_fixture:
		return

	# Construct the full path to the correct XML file.
	base_dir = os.path.dirname(__file__)
	xml_path = os.path.join(base_dir, XML_FIXTURE_PATHS[active_xml_fixture])

	# Delegate parametrization for structs
	parametrize_xml_elements(
		metafunc,
		fixture_name="struct_elem",
		xml_tags=STRUCT_TYPES,
		marker_name="only_for_structs",
		xml_path=xml_path
	)
	# Delegate parametrization for enums
	parametrize_xml_elements(
		metafunc,
		fixture_name="enum_elem",
		xml_tags=ENUM_TYPES,
		marker_name="only_for_enums",
		xml_path=xml_path
	)


def pytest_configure(config: pytest.Config) -> None:
	"""Register custom markers."""
	config.addinivalue_line(
		"markers", "only_for_structs(names): run test only on specified structs"
	)
	config.addinivalue_line(
		"markers", "only_for_enums(names): run test only on specified enums"
	)


@pytest.fixture
def struct_elem(request: pytest.FixtureRequest, active_parser):
	"""
	A generic fixture that returns a specific struct XML element by name,
	using whichever XmlParser instance is active for the test.
	"""
	struct_name = request.param
	return find_element_in_parser(active_parser, struct_name, STRUCT_TYPES)


@pytest.fixture
def enum_elem(request: pytest.FixtureRequest, active_parser):
	"""
	A generic fixture that returns a specific enum XML element by name,
	using whichever XmlParser instance is active for the test.
	"""
	enum_name = request.param
	return find_element_in_parser(active_parser, enum_name, ENUM_TYPES)
