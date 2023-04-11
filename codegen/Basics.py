class Basics:

    def __init__(self, parser):
        self.parser = parser
        self.booleans = set()

    def read(self, xml_struct):
        basic_name = xml_struct.attrib["name"]

        self.parser.processed_types[basic_name] = None

        if xml_struct.attrib.get("boolean", "False") == "True":
            self.booleans.add(basic_name)

    def add_other_basics(self, other_basics):
        self.booleans.update(other_basics.booleans)

