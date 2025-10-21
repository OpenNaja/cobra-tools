import pytest

from codegen.Versions import Versions

from .test_xml_parser import config, xml_parser, xml_test1

def test_versions_loading(xml_test1):
	# The xml_test1 fixture loads the versions
	versions_obj = xml_test1.versions
	assert versions_obj is not None
	
	# Should have loaded the 3 version tags from test1.xml
	# + 10 in base
	assert len(versions_obj.versions) == 13
	
	version_ids = {v.attrib['id'] for v in versions_obj.versions}
	assert "V1_RELEASE" in version_ids
	assert "V2_BETA" in version_ids
	assert "V3_ALPHA" in version_ids

def test_versions_format_id():
	assert Versions.format_id("V1_RELEASE") == "v1_release"
	assert Versions.format_id("MyVersion") == "myversion"

def test_version_attributes_are_read(xml_test1):
	v2_beta = next(v for v in xml_test1.versions.versions if v.attrib['id'] == 'V2_BETA')
	assert v2_beta.attrib['version'] == '2'
	assert v2_beta.attrib['user_version'] == '1234'
