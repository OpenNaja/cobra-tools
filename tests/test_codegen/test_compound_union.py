import pytest
from io import StringIO

from codegen.Compound import Compound
from codegen.Union import Union

from .conftest import find_element_in_parser
from .test_xml_parser import config, xml_parser, xml_test1


@pytest.mark.only_for_structs([
	"StructWithOperatorExpressions"
])
def test_compound_creates_unions(xml_test1, config, struct_elem):
	compound = Compound(xml_test1, struct_elem, config)
	# The operator struct has many fields, check a few
	assert len(compound.field_unions) > 5
	# Check that all fields with unique names have their own union
	union_names = {u.name for u in compound.field_unions}
	assert "operand_a" in union_names
	assert "add_result" in union_names
	assert "lt_cond_field" in union_names


UNION_COUNTS_TEST_DATA = {
	"StructWithConditionalFields": {
		"union_field": 2,
	},
	# Example struct
	# "AnotherStruct": {
	#     "some_other_union": 3,
	#     "a_different_union": 5,
	# }
}
UNION_CASES = [
	(struct, union, count)
	for struct, unions in UNION_COUNTS_TEST_DATA.items()
	for union, count in unions.items()
]

@pytest.mark.parametrize("struct_name, union_name, expected_count", UNION_CASES)
def test_compound_groups_union_fields(xml_test1, config, struct_name, union_name, expected_count):
	# Find the specific XML element for the struct we are testing
	struct_elem = find_element_in_parser(xml_test1, struct_name)
	assert struct_elem is not None, f"Struct '{struct_name}' not found in test XML."
	
	# Run the test logic with the parametrized values
	compound = Compound(xml_test1, struct_elem, config)
	target_union = next((u for u in compound.field_unions if u.name == union_name), None)
	
	assert target_union is not None, f"Union '{union_name}' not found in struct '{struct_name}'."
	assert len(target_union.members) == expected_count


LOCAL_CONDITION_TEST_DATA = {
	"StructWithOperatorExpressions": [
		("lt_cond_field", "instance.operand_a < instance.operand_b"),
		("and_cond_field", "(instance.operand_a == 10) and instance.bool_a"),
	]
}

@pytest.mark.only_for_structs([
	"StructWithOperatorExpressions"
])
def test_union_get_local_conditions(xml_test1, config, struct_elem, subtests):
	"""
	Verifies that 'cond' attributes are correctly parsed into local conditions
	"""
	current_struct_name = struct_elem.attrib['name']
	test_cases = LOCAL_CONDITION_TEST_DATA.get(current_struct_name, [])
	compound = Compound(xml_test1, struct_elem, config)

	for field_name, expected_cond in test_cases:
		with subtests.test(msg=f"{current_struct_name}-{field_name}"):
			field_element = next(
				m for u in compound.field_unions if u.name == field_name for m in u.members
			)
			union = next(u for u in compound.field_unions if u.name == field_name)

			global_conds, local_conds = union.get_conditions(field_element, "instance")
			
			# For this test, we expect local conditions and NO global conditions.
			assert not global_conds, "Expected no global conditions, but found some."
			assert " and ".join(local_conds) == expected_cond


# Test data for global conditions.
GLOBAL_CONDITION_TEST_DATA = {
	"StructWithConditionalFields": [
		("version_1_only_field", "instance.context.version == 1"),
		("version_2_plus_field", "instance.context.version >= 2"),
	]
}

@pytest.mark.only_for_structs([
	"StructWithConditionalFields"
])
def test_union_get_global_conditions(xml_test1, config, struct_elem, subtests):
	"""
	Verifies that 'vercond' attributes are correctly parsed into global conditions
	"""
	current_struct_name = struct_elem.attrib['name']
	test_cases = GLOBAL_CONDITION_TEST_DATA.get(current_struct_name, [])
	compound = Compound(xml_test1, struct_elem, config)

	for field_name, expected_cond in test_cases:
		with subtests.test(msg=f"{current_struct_name}-{field_name}"):
			field_element = next(
				m for u in compound.field_unions if u.name == field_name for m in u.members
			)
			union = next(u for u in compound.field_unions if u.name == field_name)

			global_conds, local_conds = union.get_conditions(field_element, "instance")

			# For this test, we expect global conditions and NO local conditions.
			assert not local_conds, "Expected no local conditions, but found some"
			assert " and ".join(global_conds) == expected_cond


@pytest.mark.parametrize("field_name, attr, expected_expr", [
	("add_result", "arrays", "self.operand_a + self.operand_b"),
	("mul_result", "arrays", "self.operand_a * 3"),
	("expression_sized_array_field", "arrays", "self.expression_array_count * 2"),
])
def test_union_get_params_expressions(xml_test1, config, field_name, attr, expected_expr):
	# Find the correct struct and create a Compound instance
	if field_name == "expression_sized_array_field":
		struct_name = "StructWithArraysAndExpressions"
	else:
		struct_name = "StructWithOperatorExpressions"
		
	struct_elem = find_element_in_parser(xml_test1, struct_name)
	compound = Compound(xml_test1, struct_elem, config)
	
	# Find the specific field element and its union
	field_element = next(m for u in compound.field_unions if u.name == field_name for m in u.members)
	union = next(u for u in compound.field_unions if u.name == field_name)

	params = union.get_params(field_element, "self")
	
	if attr == "arrays":
		assert str(params.arrays[0]) == expected_expr


# Grouped test data mapping a struct name to the specific lines we want to verify.
ATTRIBUTES_TEST_DATA = {
	"StructWithConditionalFields": [
		"yield 'version_1_only_field', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version == 1, None)",
		"yield 'conditionally_present_pointer', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, True)"
	],
	"StructWithOperatorExpressions": [
		# Test a field with a default value, which appears in the 4th tuple element
		"yield 'operand_a', name_type_map['Uint'], (0, None), (False, 10), (None, None)",
		# Test a field with a local 'cond' attribute, which sets the 5th element's second item to True
		"yield 'lt_cond_field', name_type_map['Uint'], (0, None), (False, None), (None, True)"
	]
}

# The hook in conftest.py will run this test for each struct listed in the marker.
@pytest.mark.only_for_structs([
	"StructWithConditionalFields",
	"StructWithOperatorExpressions"
])
def test_union_write_attributes(
	xml_test1, config, struct_elem, subtests
):
	"""
	This test receives a specific 'struct_elem' from the conftest hook
	and creates individually reported sub-tests for each expected line
	from the write_attributes method.
	"""
	# Get the name of the struct we're currently testing
	current_struct_name = struct_elem.attrib['name']
	
	# Look up the expected lines for this specific struct from our data
	expected_lines = ATTRIBUTES_TEST_DATA.get(current_struct_name)
	assert expected_lines is not None, f"No test data for {current_struct_name}"

	# Generate the actual output string once for the current struct
	compound = Compound(xml_test1, struct_elem, config)
	output = StringIO()
	for union in compound.field_unions:
		union.write_attributes(output)
	result = output.getvalue()

	# Create a separate, named sub-test for each expected line
	for line in expected_lines:
		# Generate a clean name for the sub-test report
		field_name = line.split("yield '")[1].split("'")[0]
		with subtests.test(msg=f"Check: {field_name}"):
			assert line in result


FILTERED_ATTRIBUTES_TEST_DATA = {
	"StructWithConditionalFields": [
		"if instance.context.version == 1: yield 'version_1_only_field', name_type_map['Uint'], (0, None), (False, None)",
		"if instance.condition_flag_field: yield 'conditionally_present_pointer', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)",
		"if instance.branch_selector == 0: yield 'union_field', name_type_map['Int'], (0, None), (False, None)"
	],
	"StructWithOperatorExpressions": [
		"yield 'operand_a', name_type_map['Uint'], (0, None), (False, 10)",
		"if instance.operand_a < instance.operand_b: yield 'lt_cond_field', name_type_map['Uint'], (0, None), (False, None)"
	]
}

@pytest.mark.only_for_structs([
	"StructWithConditionalFields",
	"StructWithOperatorExpressions"
])
def test_union_write_filtered_attributes(
	xml_test1, config, struct_elem, subtests
):
	"""
	This test receives a specific 'struct_elem' from the conftest hook
	and then creates individually reported sub-tests for each expected line.
	"""
	# Get the name of the struct we're currently testing
	current_struct_name = struct_elem.attrib['name']
	
	# Look up the expected lines for this specific struct
	expected_blocks = FILTERED_ATTRIBUTES_TEST_DATA.get(current_struct_name)
	assert expected_blocks is not None, f"No test data for {current_struct_name}"

	# Generate the actual output string once
	compound = Compound(xml_test1, struct_elem, config)
	output = StringIO()
	condition = ""
	for union in compound.field_unions:
		condition = union.write_filtered_attributes(output, condition, target_variable="instance")
	result_single_string = " ".join(line.strip() for line in output.getvalue().split('\n') if line.strip())

	# Create a separate, named sub-test for each expected line
	for block in expected_blocks:
		field_name = block.split("yield '")[1].split("'")[0]
		with subtests.test(msg=f"Check: {field_name}"):
			assert block in result_single_string
