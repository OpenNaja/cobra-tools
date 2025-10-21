import os
import pytest
import logging
import shutil
import filecmp
from dataclasses import dataclass, field

from codegen.__main__ import generate_classes
from codegen import Config, ExitCode, LogMessageID

@dataclass
class CodegenTestCase:
	"""Defines the parameters for a single codegen test run"""
	id: str
	source_subdir: str
	expected_exit_code: int
	max_log_level: int = logging.INFO
	copy_schema: bool = True
	expected_logs: list[str] = field(default_factory=list)
	expected_files: list[str] = field(default_factory=list)
	cli_args: dict = field(default_factory=dict)
	formats: list[str] | None = None

# --- Test Case Definitions ---
# A successful run using the 'xml1' source dir
SUCCESS_CASE = CodegenTestCase(
	id="successful_run_xml1",
	source_subdir="xml1/source",
	expected_exit_code=ExitCode.SUCCESS,
	expected_logs=[
		(LogMessageID.GENERATION_START, None),
		(LogMessageID.DISCOVERY_COMPLETE, None),
		(LogMessageID.GENERATING_FROM_FORMAT, "test1"),
		(LogMessageID.GENERATION_FINISH_TIME, None),
	],
	# Based on Compound.py, Enum.py etc., these files should be generated.
	# We check for a few key files to confirm the process worked.
	expected_files=[
		"formats/test1/enums/ExampleEnum.py",
		"formats/test1/structs/StructWithBasicTypes.py",
		"formats/test1/bitflags/ExampleBitflags.py",  # Test "bitflags" pluralization
		"formats/test1/compounds/StructWithConditionalFields.py",
		"formats/test1/imports.py",
		"formats/test1/versions.py",
	]
)

# Placeholder for a failing run
# FAIL_CASE = CodegenTestCase(
#     id="failing_run_xml1fail",
#     source_subdir="xml1fail/source",
#     expected_exit_code=1,
#     expected_logs=[
#         
#     ],
#     expected_files=[]
# )

NO_SCHEMA_CASE = CodegenTestCase(
	id="no_schema_xml1",
	source_subdir="xml1/source",
	expected_exit_code=ExitCode.SUCCESS,
	max_log_level=logging.WARNING,
	copy_schema=False,  # Do not provide schema to test absence
	expected_logs=SUCCESS_CASE.expected_logs + [
		(LogMessageID.SCHEMA_NOT_FOUND, None),
	],
	expected_files=SUCCESS_CASE.expected_files
)


def _run_codegen(test_case: CodegenTestCase, tmp_path, caplog, monkeypatch) -> str:
	"""
	A helper that runs a single codegen test case and returns the generated path.
	"""
	test_dir = os.path.dirname(__file__)
	source_path = os.path.join(test_dir, test_case.source_subdir)
	gen_path = str(tmp_path / "generated")

	# Ensure the source directory for the test case exists
	assert os.path.isdir(source_path), f"Test source directory not found at: {source_path}"

	# Start with a dictionary of default settings
	default_config_args = {
		"write_stubs": True,
		"silent": False,
		"copy_xml": False,
		"abort_on_error": True,
	}

	# The test case's cli_args will overwrite any matching keys
	final_config_args = default_config_args.copy()
	final_config_args.update(test_case.cli_args)
	
	# Use the real Config object, not a mock
	config = Config(
		root_dir=os.path.abspath(tmp_path),
		gen_dir=os.path.basename(gen_path),
		src_dir=os.path.basename(source_path),
		**final_config_args
	)

	# The script expects to find the source dir inside the CWD
	monkeypatch.chdir(tmp_path)

	# DEBUG LOGGING
	caplog.set_level(logging.DEBUG)
	logging.debug(f"--- Test Setup: {test_case.id} ---")
	logging.debug(f"Temporary Dir (tmp_path): {tmp_path}")
	logging.debug(f"Original Source Dir (source_path): {source_path}")
	logging.debug(f"Target Generated Dir (gen_path): {gen_path}")
	logging.debug(f"Current Working Directory (post-chdir): {os.getcwd()}")
	
	copy_destination = os.path.basename(source_path)
	logging.debug(f"Copying source from '{source_path}' to '{os.path.join(tmp_path, copy_destination)}'")
	shutil.copytree(source_path, copy_destination)
	# Copy the schema directory if requested
	if test_case.copy_schema:
		repo_root = os.path.abspath(os.path.join(test_dir, '..', '..'))
		schema_source_path = os.path.join(repo_root, 'source', 'schema')
		schema_dest_path = os.path.join(tmp_path, copy_destination, 'schema')
		
		logging.debug(f"Copying schema from '{schema_source_path}' to '{schema_dest_path}'")
		if os.path.isdir(schema_source_path):
			shutil.copytree(schema_source_path, schema_dest_path)
		else:
			pytest.fail(f"Schema source directory not found at: {schema_source_path}")

	logging.debug(f"Final Config object being used: {config}")
	logging.debug("--- Starting Codegen Execution ---")


	# Execute Codegen
	# Run the main function from __main__.py
	exit_code = generate_classes(config, formats=test_case.formats)

	# Assertions

	# Check the exit code
	assert exit_code == test_case.expected_exit_code

	# Check for expected log messages
	for expected_id, expected_substring in test_case.expected_logs:
		found_log = any(
			# Check if the record has our custom msg_id and if it matches the one we expect
			getattr(record, 'msg_id', None) == expected_id and
			# If a substring is specified, also check if it's in the formatted message
			(expected_substring is None or expected_substring in record.message)
			for record in caplog.records
		)
		assert found_log, f"Expected log with ID '{expected_id.name}' and substring '{expected_substring}' not found."

	# Check for the presence of expected generated files
	for expected_file in test_case.expected_files:
		file_path = os.path.normpath(os.path.join(gen_path, expected_file))
		assert os.path.isfile(file_path), f"Expected generated file not found: {file_path}"

	# Check for unexpected high-level log messages
	unexpected_high_level_logs = []
	for record in caplog.records:
		if record.levelno > test_case.max_log_level:
			unexpected_high_level_logs.append(
				f"    - [{logging.getLevelName(record.levelno)}] {record.message}"
			)

	if unexpected_high_level_logs:
		pytest.fail(
			f"Found log messages with level > {logging.getLevelName(test_case.max_log_level)}:\n"
			+ "\n".join(unexpected_high_level_logs)
		)
	return gen_path


@pytest.mark.parametrize(
	"test_case",
	[
		SUCCESS_CASE,
		NO_SCHEMA_CASE
	],  # TODO: FAIL_CASE cases
	ids=lambda tc: tc.id
)
def test_codegen_run(test_case: CodegenTestCase, tmp_path, caplog, monkeypatch) -> None:
	"""
	Runs the main generation function and verifies the exit code, log output, and created files
	"""
	_run_codegen(test_case, tmp_path, caplog, monkeypatch)


def test_selective_run_matches_full_run(tmp_path_factory, caplog, monkeypatch):
	"""
	Verifies that a selective run produces the same output as a full run when
	there is the only format present
	"""
	# Define the two test cases
	full_run_case = CodegenTestCase(
		id="comparison_full_run",
		source_subdir="xml1/source",
		expected_exit_code=ExitCode.SUCCESS,
		copy_schema=True,
	)
	
	selective_run_case = CodegenTestCase(
		id="comparison_selective_run",
		source_subdir="xml1/source",
		expected_exit_code=ExitCode.SUCCESS,
		copy_schema=True,
		formats=["test1"]
	)

	# Run both test cases in separate temporary directories
	full_run_tmp = tmp_path_factory.mktemp("comparison_full_run")
	full_run_gen_path = _run_codegen(full_run_case, full_run_tmp, caplog, monkeypatch)

	selective_run_tmp = tmp_path_factory.mktemp("comparison_selective_run")
	selective_run_gen_path = _run_codegen(selective_run_case, selective_run_tmp, caplog, monkeypatch)

	# Compare the output directories
	comparison = filecmp.dircmp(full_run_gen_path, selective_run_gen_path)
	
	# Assert that there are no files that only exist in one of the directories
	# and no files that are different
	assert not comparison.left_only, f"Files found only in full run: {comparison.left_only}"
	assert not comparison.right_only, f"Files found only in selective run: {comparison.right_only}"
	assert not comparison.diff_files, f"Files with differences: {comparison.diff_files}"
