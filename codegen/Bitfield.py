from .BaseClass import BaseClass
from . import naming_conventions as convention

FIELD_TYPES = ("add", "field")
VER = "stream.version"


class Bitfield(BaseClass):

    def read(self):
        """Create a self.struct class"""
        super().read()

        # write to python file
        with open(self.out_file, "w") as f:
            # write the header stuff
            super().write(f)

            for field in self.struct:
                field_name = convention.name_attribute(field.attrib["name"])
                print(field_name)
                _, field_type = self.parser.map_type(convention.name_class(field.attrib["type"]))
                f.write(f"\n\t{field_name} = BitfieldMember(pos={field.attrib['pos']}, mask={field.attrib['mask']}, return_type={field_type})")

            f.write("\n\n\tdef set_defaults(self):")
            defaults = []
            for field in self.struct:
                field_name = convention.name_attribute(field.attrib["name"])
                field_type = convention.name_class(field.attrib["type"])
                field_default = field.attrib.get("default")
                # write the field's default, if it exists
                if field_default:
                    # we have to check if the default is an enum default value, in which case it has to be a member of that enum
                    if self.parser.tag_dict[field_type.lower()] == "enum":
                        field_default = field_type+"."+field_default
                    defaults.append((field_name, field_default))
            if defaults:
                for field_name, field_default in defaults:
                    f.write(f"\n\t\tself.{field_name} = {field_default}")
            else:
                f.write(f"\n\t\tpass")

            self.parser.write_storage_io_methods(f, storage)
