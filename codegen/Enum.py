from .BaseClass import BaseClass


class Enum(BaseClass):

    def read(self):
        """Create a struct class"""
        super().read()

        storage = self.struct.attrib["storage"]
        # todo - handle case where storage is given as size instead of name
        # store storage format in dict so it can be accessed during compound writing
        self.parser.storage_dict[self.class_name] = storage
        enum_base = self.base_from_storage(storage)
        self.class_basename = enum_base
        self.imports.add(enum_base)
        # write to python file
        with open(self.out_file, "w", encoding=self.parser.encoding) as f:
            # write the header stuff
            super().write(f)
            for option in self.struct:
                if option.text:
                    f.write(f"\n\t# {option.text}")
                f.write(f"\n\t{option.attrib['name']} = {option.attrib['value']}")
            f.write(f"\n")

    @staticmethod
    def base_from_storage(storage):
        return f"{storage.capitalize()}Enum"
