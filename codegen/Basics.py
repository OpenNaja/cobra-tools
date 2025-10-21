from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Config, Element
    from .XmlParser import XmlParser


class Basics:

    def __init__(self, parser: 'XmlParser') -> None:
        self.parser: XmlParser = parser
        self.booleans: set[str] = set()
        self.integrals: set[str] = set()
        self.floats: set[str] = set()
        self.strings: set[str] = set()

    def read(self, xml_struct: 'Element') -> None:
        basic_name: str = xml_struct.attrib["name"]

        self.parser.processed_types[basic_name] = None

        # Refined classification logic
        if xml_struct.attrib.get("boolean", "False") == "True":
            self.booleans.add(basic_name)
        elif "String" in basic_name:
            self.strings.add(basic_name)
        elif xml_struct.attrib.get("integral", "False") == "True":
            self.integrals.add(basic_name)
        else:
            # The remaining non-integral, non-string basics are float-like
            self.floats.add(basic_name)

    def add_other_basics(self, other_basics: 'Basics') -> None:
        self.booleans.update(other_basics.booleans)
        self.integrals.update(other_basics.integrals)
        self.floats.update(other_basics.floats)
        self.strings.update(other_basics.strings)

