from .BaseClass import BaseClass
from .naming_conventions import clean_comment_str

class Enum(BaseClass):

    def read(self):
        """Create a struct class"""
        super().read()

        storage = self.struct.attrib["storage"]
        # todo - handle case where storage is given as size instead of name
        # store storage format in dict so it can be accessed during compound writing
        self.class_basename = "BaseEnum"
        self.imports.add("BaseEnum")
        self.imports.add(storage)
        # write to python file
        with open(self.out_file, "w", encoding=self.parser.encoding) as f:
            # write the header stuff
            super().write(f)
            self.write_line(f, 1, f"_storage = {storage}")
            self.write_line(f)
            for option in self.struct:
                if option.text:
                    f.write(clean_comment_str(option.text, indent="\t"))
                f.write(f"\n\t{option.attrib['name']} = {option.attrib['value']}")
            f.write(f"\n")
