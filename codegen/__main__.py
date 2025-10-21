import importlib.util
import logging
import os
import sys
import time
import shutil
import fnmatch
import argparse
import traceback
from typing import TYPE_CHECKING, Any, Optional
from concurrent.futures import ProcessPoolExecutor, as_completed

from . import (Config, ExitCode, FormatDependencies, NamespacedTypes, LogMessageID, PARSING_EXCEPTIONS,
               XmlValidationError, LXML_INSTALLED, XMLSCHEMA_INSTALLED, ET, xmlschema)
from .XmlParser import XmlParser
from .codegen_worker import process_single_format
from .path_utils import to_import_path, pluralize_name


if TYPE_CHECKING:
    from . import ElementTree, Element
    from xmlschema import XMLSchema11
else:
    XMLSchema11 = Any

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')


def copy_src_to_generated(subfolder_pairs: list[tuple[str, str]], cfg: 'Config') -> None:
    """
    For each provided (source, target) subfolder pair, this function wipes the
    target subfolder and copies the entire source subfolder tree.
    """
    for src_subdir, trg_subdir in subfolder_pairs:
        logging.info(f"Syncing subfolder '{os.path.basename(src_subdir)}'...")
        
        if os.path.exists(trg_subdir):
            shutil.rmtree(trg_subdir)
            
        ignore_patterns: tuple[str, ...] = ('.git', 'schema')
        if not cfg.copy_xml:
            ignore_patterns += ('*.xml',)
        if not cfg.write_stubs:
            ignore_patterns += ('*.pyi',)
        shutil.copytree(src_subdir, trg_subdir, ignore=shutil.ignore_patterns(*ignore_patterns))
 

def fix_imports(gen_dir: str) -> None:
    """Fixes hardcoded imports in non-generated files"""
    gen_import_path = to_import_path(gen_dir)
    for path, _, files in os.walk(os.path.abspath(gen_dir)):
        for pattern in ("*.py", "*.pyi"):
            for filename in fnmatch.filter(files, pattern):
                filepath = os.path.join(path, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    s = f.read()
                s = s.replace("from generated.", f"from {gen_import_path}.")
                s = s.replace("import generated.", f"import {gen_import_path}.")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(s)


def create_inits(base_dirs: list[str]) -> None:
    """Create a __init__.py file in all subdirectories that don't have one."""
    init_name = "__init__.py"
    # Loop over the specific base directories provided for processing.
    for base_dir in base_dirs:
        for root, dirs, files in os.walk(base_dir):
            if init_name not in files:
                # __init__.py does not exist, create it
                with open(os.path.join(root, init_name), 'x'):
                    pass
            # Ignore special subdirectories
            dirs[:] = [dirname for dirname in dirs if dirname[:2] != '__']


def apply_autopep8(target_dir: str) -> None:
    """Run autopep8 --in-place on the target directory, if that package is installed"""
    if importlib.util.find_spec("autopep8"):
        import autopep8  # type: ignore
        options = autopep8.parse_args(arguments=['-i', '-r', target_dir])
        autopep8.fix_multiple_files([target_dir], options=options)
    else:
        logging.warning("Tried to run autopep8, but module not found.")


def validate_xml_file(xml_path: str, xsd_schema: 'XMLSchema11', doc_tree: 'ElementTree') -> None:
    """Uses xmlschema to validate the XML file against an XSD schema."""
    if not XMLSCHEMA_INSTALLED:
        logging.warning("xmlschema library is not installed, skipping XSD validation")
        return

    if not xsd_schema:
        logging.warning(f"Schema file not found, skipping validation")
        return
        
    try:
        validation_errors = []
        # If lxml is available, use it to pre-parse the XML
        # This provides source line information to xmlschema
        if LXML_INSTALLED:
            # Pass the parsed lxml data tree to iter_errors.
            validation_errors = list(xsd_schema.iter_errors(doc_tree))
        else:
            # Fallback to xmlschema's internal parser if lxml is not installed
            logging.debug("lxml not found, using xmlschema's default parser")
            validation_errors = list(xsd_schema.iter_errors(xml_path))

        # If the list is not empty, validation has failed.
        if validation_errors:
            logging.error(f"XSD validation failed for {os.path.basename(xml_path)}:")
            for error in validation_errors:
                # Safely access source URL and line number
                display_file = os.path.basename(xml_path)
                if error.source:
                    # The source is an lxml resource object
                    if hasattr(error.source, 'root') and error.source.root is not None and hasattr(error.source.root, 'base'):
                        display_file = os.path.basename(error.source.root.base)
                    # The source is the default object with a URL
                    elif hasattr(error.source, 'url'):
                        display_file = os.path.basename(error.source.url)
            
                line = error.sourceline if error.sourceline else 0
                context = f"Line {line}"  # Default context
                if error.elem is not None and hasattr(error.elem, 'tag'):
                    context = f"<{error.elem.tag.split('}')[-1]}> at Line {line}"

                message = error.reason
                # Check if the error is from an XsdAssert and has a documented message
                if hasattr(error.validator, 'annotation') and error.validator.annotation:
                    # The .documentation attribute is a list of Element objects.
                    # We extract the .text from each and join them into a single string.
                    if error.validator.annotation is None:
                        logging.warning(f"File: {display_file}, {context} - {message}")
                    doc_texts = [doc.text for doc in error.validator.annotation.documentation if doc.text]
                    if doc_texts:
                        message = ' '.join(doc_texts).strip()

                logging.error(
                    f"  File: {display_file}, {context} - {message}"
                )
            # Raise an exception to stop the parsing of this file.
            raise XmlValidationError("Validation failed with xmlschema")

        # Set to track which 'once-per-file' messages have been printed
        printed_once_per_file_messages = set()

        if doc_tree is not None:
            for element in doc_tree.iter():
                if not isinstance(element.tag, str):
                    continue

                xsd_component = xsd_schema.find(element.tag)
                if not xsd_component or not isinstance(xsd_component, xmlschema.XsdElement):
                    continue

                component_to_check = xsd_component.ref if xsd_component.ref else xsd_component
                if component_to_check and component_to_check.annotation:
                    doc_texts = [doc.text for doc in component_to_check.annotation.documentation if doc.text and doc.text.strip()]
                    if doc_texts:
                        message = ' '.join(doc_texts).strip().replace('\n', ' ').strip()
                        # Default frequency is 'per-instance'
                        frequency = 'per-instance'
                        # Check for our custom appinfo metadata
                        if component_to_check.annotation.appinfo:
                            # .appinfo is a list of the <xs:appinfo> elements
                            for appinfo_element in component_to_check.annotation.appinfo:
                                # We need to look at the CHILDREN of the <xs:appinfo> element
                                for info_child in appinfo_element:
                                    if info_child.tag == 'info':
                                        # Found our custom <info> tag, now get its attribute
                                        frequency = info_child.get('frequency', 'per-instance')
                                        break  # Stop after finding the first <info> tag
                                else:
                                    continue # Continue if inner loop didn't break
                                break # Stop after processing first <xs:appinfo> with an <info> tag
                        
                        # Decide whether to print the message
                        if frequency == 'once-per-file':
                            if message not in printed_once_per_file_messages:
                                logging.info(f"  {os.path.basename(xml_path)}: {message}")
                                printed_once_per_file_messages.add(message)
                        else: # Default 'per-instance' behavior
                            line = element.sourceline
                            logging.info(f"  <{element.tag.split('}')[-1]}> at Line {line}: {message}")

        # If the list is empty, validation was successful.
        logging.info(f"Successfully validated {os.path.basename(xml_path)} with xmlschema")

    except PARSING_EXCEPTIONS as e:
        # Catch errors related to parsing the schema or XML itself.
        logging.error(f"A parsing error occurred during xmlschema validation for {os.path.basename(xml_path)}: {e}")
        raise
    except Exception as e:
        # Catch any other unexpected errors.
        if isinstance(e, XmlValidationError):
            raise # Re-raise our exception to signal failure.
        logging.error(f"An unexpected error occurred during xmlschema validation for {os.path.basename(xml_path)}: {e}")
        raise


def discovery_pass(formats_dir: str, cfg: 'Config', xsd_schema: 'XMLSchema11', formats: list[str] | None) -> tuple[NamespacedTypes, FormatDependencies, list[str]]:
    """
    Validates XML with XMLSchema and performs a lightweight pass over all XML files to build:
    1. A namespaced map of all defined types: {format: {type: path}}.
    2. A dependency map for each format: {format: [dependency_format]}. (Only for <module>, not XInclude)
    """
    logging.info("Starting discovery pass...", extra={'msg_id': LogMessageID.DISCOVERY_START})
    namespaced_types: NamespacedTypes = {}
    format_dependencies: FormatDependencies = {}
    validation_errors: list[str] = []

    dummy_parser = XmlParser("dummy", cfg)
    
    all_roots = {}
    format_names: list[str] = [d for d in os.listdir(formats_dir) if os.path.isdir(os.path.join(formats_dir, d))]

    # First pass: Parse XMLs, apply conventions, and find dependencies
    for format_name in format_names:
        namespaced_types[format_name] = {}
        format_dependencies[format_name] = []  # No defaults for now
        xml_path = os.path.join(formats_dir, format_name, f"{format_name}.xml")
        if os.path.isfile(xml_path):
            tree: ElementTree | None = None
            root: Element | None = None
            try:
                # Use lxml if available
                if LXML_INSTALLED and ET:
                    parser = ET.XMLParser(remove_blank_text=True)
                    tree = ET.parse(xml_path, parser)
                    root = tree.getroot()
                else:
                    tree = ET.parse(xml_path)
                    root = tree.getroot()
                should_validate = (formats is None) or (format_name in formats)
                if xsd_schema and should_validate:
                    validate_xml_file(xml_path, xsd_schema, tree)
            except (XmlValidationError, Exception) as e:
                # If validation fails, add the format to our error list and skip it
                logging.error(f"Validation failed for '{format_name}'. It will be excluded from generation.")
                validation_errors.append(format_name)
                continue

            all_roots[format_name] = root
            for child in root:
                dummy_parser.apply_conventions(child)
                # Check for an explicit module dependency
                if child.tag == "module" and "depends" in child.attrib:
                    # Override default dependencies
                    format_dependencies[format_name] = child.attrib["depends"].split()

    # Second pass: Build the namespaced path dict
    for format_name, root in all_roots.items():
        base_segments = os.path.join("formats", format_name)
        for child in root:
            if not isinstance(child.tag, str):
                continue
            if child.tag.split('}')[-1] not in ("version", "token", "include", "verattr"):
                class_name = child.attrib.get("name")
                if not class_name:
                    continue
                
                if child.tag == "module":
                    path = os.path.join(base_segments, class_name)
                elif child.tag == "basic":
                    # Basics are typically shared, place them under their format's 'basic' folder
                    path = os.path.join(base_segments, "basic")
                else:
                    module_name = child.attrib.get("module")
                    current_base = namespaced_types[format_name].get(module_name, base_segments)
                    path = os.path.join(current_base, pluralize_name(child.tag), class_name)
                
                namespaced_types[format_name][class_name] = path
                
    logging.info(f"Discovery complete. Found {sum(len(v) for v in namespaced_types.values())} types across {len(format_names)} formats.",
                 extra={'msg_id': LogMessageID.DISCOVERY_COMPLETE})
    return namespaced_types, format_dependencies, validation_errors


def _handle_error(exc: Exception, xml_path: str) -> ExitCode:
    """Logs an error, updates the validation list, and returns the appropriate exit code."""
    format_name = os.path.basename(os.path.dirname(xml_path))
    
    #if isinstance(exc, XmlValidationError):
    #    logging.error(f"Skipping '{format_name}' due to a validation error.")
    #    validation_errors.append(format_name)
    #    return ExitCode.VALIDATION_ERROR
    #else:
    # For any other unexpected error, log the full traceback.
    logging.error(f"An unexpected error occurred while processing '{format_name}'.\n{traceback.format_exc()}")
    return ExitCode.UNEXPECTED_ERROR


def generate_classes(cfg: 'Config', formats: list[str] | None = None) -> ExitCode:
    start_time = time.monotonic()
    if cfg.silent:
        logging.disable(logging.ERROR)
    logging.info("Starting class generation", extra={'msg_id': LogMessageID.GENERATION_START})
    source_dir = os.path.join(cfg.root_dir, cfg.src_dir)
    target_dir = os.path.join(cfg.root_dir, cfg.gen_dir)
    formats_dir = os.path.join(source_dir, "formats")

    # Load XSD Schema
    xsd_schema = None
    if XMLSCHEMA_INSTALLED:
        schema_path = os.path.abspath(os.path.join(cfg.src_dir, "schema", "codegen_schema_11.xsd"))
        if os.path.exists(schema_path):
            logging.info("Loading and compiling XSD schema...", extra={'msg_id': LogMessageID.SCHEMA_LOAD_START})
            try:
                xsd_schema = xmlschema.XMLSchema11(schema_path)
                logging.info("Schema loaded successfully.", extra={'msg_id': LogMessageID.SCHEMA_LOAD_SUCCESS})
            except Exception as e:
                logging.error(f"Failed to load or parse XSD schema: {e}", extra={'msg_id': LogMessageID.SCHEMA_LOAD_FAIL})
                return ExitCode.INVALID_SCHEMA # Abort if the schema itself is invalid
        else:
            logging.warning(f"Schema file not found at {schema_path}, skipping validation.", extra={'msg_id': LogMessageID.SCHEMA_NOT_FOUND})

    # Run the discovery pass
    (namespaced_types,
    format_dependencies,
    validation_errors) = discovery_pass(formats_dir, cfg, xsd_schema, formats)
    logging.info(f"Discovery pass finished in {time.monotonic()-start_time:.2f} seconds.")
    
    if validation_errors and cfg.abort_on_error:
        logging.error("=" * 40)
        logging.error("Aborting before generation due to validation errors.")
        logging.error(f"Failed formats: {', '.join(validation_errors)}")
        logging.error("=" * 40)
        return ExitCode.VALIDATION_ERROR

    is_selective_run = formats is not None
    # Use the provided list for a selective run, or scan the directory for a full run.
    formats_to_process = formats if is_selective_run else os.listdir(formats_dir)
    # Exclude failed formats from all subsequent steps
    failed_formats = set(validation_errors)
    valid_formats_to_process = [fmt for fmt in formats_to_process if fmt not in failed_formats]

    # Build the list of full XML file paths from the format names
    files_to_generate = []
    for format_name in valid_formats_to_process:
        dir_path = os.path.join(formats_dir, format_name)
        if os.path.isdir(dir_path):
            xml_path = os.path.join(dir_path, f"{format_name}.xml")
            if os.path.isfile(xml_path):
                files_to_generate.append(xml_path)
    
    subfolders_to_process = []
    if is_selective_run:
        for format_name in formats:
            src_format_dir = os.path.join(formats_dir, format_name)
            trg_format_dir = os.path.join(target_dir, "formats", format_name)
            if os.path.isdir(src_format_dir):
                subfolders_to_process.append((src_format_dir, trg_format_dir))
        copy_src_to_generated(subfolders_to_process, cfg)
    else:
        # Full run copies the entire top-level directory
        copy_src_to_generated([(source_dir, target_dir)], cfg)

    fix_imports(target_dir)

    # Perform the generation pass
    parsed_xmls: dict[str, 'XmlParser'] = {}
    exit_code = ExitCode.VALIDATION_ERROR if validation_errors else ExitCode.SUCCESS
    is_running_sequentially = (
        "pytest" in sys.modules or not cfg.concurrent
    )
    if is_running_sequentially:
        # Sequential execution for tests, debugging, or profiling
        logging.info(f"Processing {len(files_to_generate)} formats in single-process mode...", extra={'msg_id': LogMessageID.PROCESSING_SINGLE})
        for xml_path in files_to_generate:
            try:
                process_single_format(
                    xml_path, cfg, namespaced_types, format_dependencies, parsed_xmls
                )
            except Exception as e:
                run_exit_code = _handle_error(e, xml_path)
                if run_exit_code > exit_code:
                    exit_code = run_exit_code
                if exit_code == ExitCode.UNEXPECTED_ERROR:
                    return exit_code
    else:  # pragma: no cover
        with ProcessPoolExecutor() as executor:
            # Submit each file to the executor to be processed
            futures = {
                # Pass the validation_cache to each worker
                executor.submit(
                    process_single_format, xml_path, cfg, namespaced_types, format_dependencies
                ): xml_path
                for xml_path in files_to_generate
            }

            logging.info(f"Processing {len(files_to_generate)} formats in parallel...",
                         extra={'msg_id': LogMessageID.PROCESSING_MULTI})

            # Process the results as they are completed.
            for future in as_completed(futures):
                xml_path = futures[future]
                try:
                    future.result()
                except Exception as e:
                    run_exit_code = _handle_error(e, xml_path)
                    if run_exit_code > exit_code:
                        exit_code = run_exit_code
                    if exit_code == ExitCode.UNEXPECTED_ERROR:
                        executor.shutdown(wait=False, cancel_futures=True)
                        return exit_code

    if validation_errors:
        logging.warning("=" * 40)
        logging.warning(f"Codegen finished with validation errors.", extra={'msg_id': LogMessageID.VALIDATION_ERRORS_HEADER})
        logging.warning(f"Total files skipped: {len(validation_errors)}")
        logging.warning(f"Validation errors: {', '.join(validation_errors)}")
        logging.warning("=" * 40)

    create_inits([target_dir])

    if cfg.silent:
        logging.disable(logging.NOTSET)

    end_time = time.monotonic()
    duration = end_time - start_time
    logging.info(f"Class generation finished in {duration:.2f} seconds.", extra={'msg_id': LogMessageID.GENERATION_FINISH_TIME})
        
    return exit_code


if __name__ == '__main__':  # pragma: no cover
    parser = argparse.ArgumentParser(prog='codegen')
    parser.add_argument('-g', '--generated-dir', default="generated")
    parser.add_argument('-s', '--source-dir', default="source")
    parser.add_argument(
        '-f', '--formats',
        nargs='+',
        help="A list of specific format names to generate (e.g. `fgm tex`). If not provided, all formats are processed."
    )
    parser.add_argument('--no-stubs', action='store_true', help="Disable generation of .pyi stub files")
    parser.add_argument('--copy-xml', action='store_true', help="Copy XML files from the source to the generated directory")
    parser.add_argument('--abort-on-error', action='store_true', help="Abort if there are any validation errors")
    parser.add_argument('--silent', action='store_true')

    args = parser.parse_args()

    config = Config(
        root_dir=os.getcwd(),
        gen_dir=args.generated_dir,
        src_dir=args.source_dir,
        silent=args.silent,
        write_stubs=not args.no_stubs,
        copy_xml=args.copy_xml,
        abort_on_error=args.abort_on_error,
        concurrent=False,  # No real speedup for now, set to True in the event it becomes worth it
    )

    exit_code = generate_classes(config, formats=args.formats)
    try:
        exit(exit_code)
    except NameError:
        pass
