import os
import logging
from . import Config, FormatDependencies, NamespacedTypes, LogMessageID
from .XmlParser import XmlParser


def process_single_format(xml_path: str, cfg: Config, namespaced_types: NamespacedTypes,
                          format_dependencies: FormatDependencies, parsed_xmls: dict[str, 'XmlParser'] | None = None) -> str:
    """
    Worker function to validate and parse a single XML format.
    Able to be run in a separate process.
    """
    # Configure logging for this worker
    log_level = logging.DEBUG if not cfg.silent else logging.WARNING
    logging.basicConfig(
        level=log_level,
        format='[%(levelname)s] %(message)s'
    )

    format_name = os.path.basename(os.path.dirname(xml_path))

    format_path_dict: dict[str, str] = {}
    scopes_to_check = [format_name] + format_dependencies.get(format_name, [])
    for scope in scopes_to_check:
        for type_name, path in namespaced_types.get(scope, {}).items():
            if type_name not in format_path_dict:
                format_path_dict[type_name] = path
    if parsed_xmls and os.path.realpath(xml_path) in parsed_xmls:
        logging.info(f"Already read {format_name}, skipping", extra={'msg_id': LogMessageID.ALREADY_READ_SKIP})
        return format_name
    logging.info(f"Generating '{format_name}' format", extra={'msg_id': LogMessageID.GENERATING_FROM_FORMAT})
    xmlp = XmlParser(format_name, cfg, path_dict=format_path_dict)
    xmlp.load_xml(xml_path, parsed_xmls)

    return format_name
