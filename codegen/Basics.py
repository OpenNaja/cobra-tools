class Basics:

    def __init__(self, parser, basics_file, ):
        self.parser = parser
        self.basic_map = {}
        self.booleans = set()
        self.basics_file = basics_file
        self.imports = []

    def read(self, xml_struct):
        basic_name = xml_struct.attrib["name"]

        self.parser.processed_types[basic_name] = None

        self.basic_map[basic_name] = None

        if xml_struct.attrib.get("boolean", "False") == "True":
            self.booleans.add(basic_name)

    def add_other_basics(self, other_basics):
        for basic, cls in other_basics.basic_map.items():
            if basic not in self.basic_map:
                self.basic_map[basic] = cls
        self.booleans.update(other_basics.booleans)

