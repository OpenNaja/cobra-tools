from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Union, TypeAlias, TYPE_CHECKING, Any, Type

import xml.etree.ElementTree as ET
LXML_INSTALLED = False
try:
    import lxml.etree as ET
    LXML_INSTALLED = True
except ImportError:
    pass

try:
    import xmlschema
    XMLSCHEMA_INSTALLED = True
except ImportError:
    xmlschema = None  # type: ignore[assignment]
    XMLSCHEMA_INSTALLED = False

if TYPE_CHECKING:
    try:
        from lxml.etree import _Element, _ElementTree
        Element: TypeAlias = Union[ET.Element[str], _Element]
        ElementTree: TypeAlias = Union[ET.ElementTree[ET.Element[str]], _ElementTree]
    except ImportError:
        # If lxml stubs are not found, the checker uses the fallback type
        Element: TypeAlias = ET.Element[str]  # type: ignore[no-redef, misc]
        ElementTree: TypeAlias = ET.ElementTree[ET.Element[str]]  # type: ignore[no-redef, misc]
else:
    from typing import Any
    Element = Any
    ElementTree = Any


NamespacedTypes: TypeAlias = dict[str, dict[str, str]]
FormatDependencies: TypeAlias = dict[str, list[str]]


class ExitCode(IntEnum):
    SUCCESS = 0
    INVALID_SCHEMA = 10
    VALIDATION_ERROR = 20
    UNEXPECTED_ERROR = 100


@dataclass
class Config:
    root_dir: str
    gen_dir: str
    src_dir: str
    silent: bool = False
    write_stubs: bool = True
    copy_xml: bool = False
    abort_on_error: bool = False
    concurrent: bool = False


class XmlGenerationError(Exception):
    """Used for general errors during parsing or code generation."""
    pass


class XmlValidationError(Exception):
    """Used for manual validation errors that XSD cannot catch."""
    pass


parsing_exceptions_list: list[Type[Exception]] = [ET.ParseError]
if XMLSCHEMA_INSTALLED and xmlschema:
    parsing_exceptions_list.append(xmlschema.XMLSchemaParseError)
PARSING_EXCEPTIONS = tuple(parsing_exceptions_list)


class LogMessageID(Enum):
    """
    Unique, stable identifiers for all log messages.
    The string value is the format template for the message.
    """
    
    # --- __main__.py ---
    DISCOVERY_START = "Starting discovery pass..."
    DISCOVERY_FAIL = "Failed to parse {xml_path} during discovery: {e}"
    DISCOVERY_COMPLETE = "Discovery complete. Found {type_count} types across {format_count} formats."
    GENERATION_START = "Starting class generation"
    DISCOVERY_FINISH_TIME = "Discovery pass finished in {duration:.2f} seconds."
    SUBFOLDER_SYNC = "Syncing subfolder '{subdir_name}'..."
    SCHEMA_LOAD_START = "Loading and compiling XSD schema..."
    SCHEMA_LOAD_SUCCESS = "Schema loaded successfully."
    SCHEMA_LOAD_FAIL = "Failed to load or parse XSD schema: {e}"
    SCHEMA_NOT_FOUND = "Schema file not found at {schema_path}, skipping validation."
    PROCESSING_SINGLE = "Processing {file_count} formats in single-process mode..."
    PROCESSING_MULTI = "Processing {file_count} formats in parallel..."
    VALIDATION_ERRORS_HEADER = "Codegen finished with validation errors."
    VALIDATION_SKIPPED_COUNT = "Total files skipped: {count}"
    VALIDATION_SKIPPED_FILES = "Validation errors: {files}"
    GENERATION_FINISH_TIME = "Class generation finished in {duration:.2f} seconds."
    UNEXPECTED_ERROR = "An unexpected error occurred while processing '{format_name}'.\n{traceback}"
    VALIDATION_ERROR_SKIP = "Skipping '{format_name}' due to a validation error."
    AUTOPEP8_NOT_FOUND = "Tried to run autopep8, but module not found."

    # --- codegen_worker.py ---
    ALREADY_READ_SKIP = "Already read {format_name}, skipping"
    GENERATING_FROM_FORMAT = "Generating '{format_name}' format"

    # --- XmlParser.py ---
    XMLSCHEMA_NOT_INSTALLED = "xmlschema library is not installed, skipping XSD validation."
    LXML_NOT_FOUND = "lxml not found, using xmlschema's default parser."
    VALIDATION_FAILED_HEADER = "XSD validation failed for {filename}:"
    VALIDATION_ERROR_DETAIL = "  File: {file}, {context} - {message}"
    VALIDATION_SUCCESS = "Successfully validated {filename} with xmlschema"
    PARSING_ERROR = "A parsing error occurred during xmlschema validation for {filename}: {e}"
    UNEXPECTED_VALIDATION_ERROR = "An unexpected error occurred during xmlschema validation for {filename}: {e}"
    VALIDATION_ABORT = "Aborting parsing for {filename} due to schema validation failure."
    VALIDATION_SKIPPING_CACHED = "Skipping validation for cached file: {filename}"
    PARSING_CHILD_FAILED = "Parsing child {child} failed"
    ANNOTATION_ONCE_PER_FILE = "  {filename}: {message}"
    ANNOTATION_PER_INSTANCE = "  <{tag}> at Line {line}: {message}"
    
    # --- Imports.py ---
    RECURSIVE_FIELD_WARN = "Field {field_name} with type {field_type} in format {format_name} is not a reference to a preceding type, but is not marked as recursive"

    # --- BaseClass.py ---
    MISSING_NAME_ATTR_WARN = "XML element <{tag}> is missing required 'name' attribute, skipping."
    MISSING_GLOBALS_WRAPPER = "{class_name} does not wrap imports with START_GLOBALS/END_GLOBALS"
    INHERIT_NOT_DECLARED = "Class {class_name} in format {format_name} inherits from {base_class}, but this is not declared in the xml before it!"
    GET_CLASS_CALL_FAIL = "[get_class_call] Invalid source code, falling back to '{fallback}'"

    def __str__(self) -> str:
        return self.value
