from .BaseClass import BaseClass
import logging


class Bitfield(BaseClass):

    def map_pos(self):
        """Generate position if it does not exist"""
        pos = 0
        for field in self.struct:
            num_bits = field.attrib.get("numbits")
            if num_bits:
                field.attrib["pos"] = str(pos)
                pos += int(num_bits)

    def get_mask(self):
        """Generate position if it does not exist"""
        for field in self.struct:
            if not field.attrib.get('mask'):
                if "numbits" in field.attrib:
                    num_bits = int(field.attrib["numbits"])
                elif "width" in field.attrib:
                    num_bits = int(field.attrib["width"])
                elif "bit" in field.attrib:
                    num_bits = 1
                    field.attrib["pos"] = field.attrib["bit"]
                    field.attrib["type"] = "bool"
                else:
                    raise AttributeError(
                        f"Neither width, mask, bit or numbits are defined for {field.attrib['name']}"
                    )
                pos = int(field.attrib["pos"])

                mask = ~((~0) << (pos + num_bits)) & ((~0) << pos)
                field.attrib['mask'] = str(hex(mask))

    def read(self):
        """Create a self.struct class"""
        super().read()
        storage = self.struct.attrib["storage"]
        self.imports.add(storage)
        self.imports.add("BasicBitfield")
        self.imports.add("BitfieldMember")
        self.class_basename = "BasicBitfield"

        # write to python file
        with open(self.out_file, "w", encoding=self.parser.encoding) as f:
            # write the header stuff
            super().write(f)
            self.write_line(f, 1, f"_storage = {storage}")
            self.map_pos()
            self.get_mask()
            if self.struct.tag == 'bitflags':
                for field in self.struct:
                    self.write_line(
                        f, 1, f"{field.attrib['enum_name']} = 2 ** {field.attrib['bit']}"
                    )
            for field in self.struct:
                field_name = field.attrib["name"]
                field_type = field.attrib.get("type", "int")
                if field_type not in self.parser.builtin_literals:
                    field_type = f'{field_type}.from_value'
                self.write_line(
                    f, 1, f"{field_name} = BitfieldMember(pos={field.attrib['pos']}, mask={field.attrib['mask']}, return_type={field_type})"
                )

            self.write_line(f, 0)
            self.write_line(f, 1, f"def set_defaults(self):")
            defaults = []
            for field in self.struct:
                field_name = field.attrib["name"]
                field_type = field.attrib.get("type", "int")
                field_default = field.attrib.get("default")
                # write the field's default, if it exists
                if field_default:
                    # if the default is an enum default value, access member of that enum
                    if self.parser.tag_dict[field_type.lower()] == "enum":
                        field_default = f"{field_type}.{field_default}"
                    # If we're not an enum, we need to check if we're a boolean and capitalize
                    elif self.parser.tag_dict[field_type.lower()] == "basic" and \
                        field_type in self.parser.basics.booleans:
                        if field_default.capitalize() in ("True", "False"):
                            field_default = field_default.capitalize()

                    defaults.append((field_name, field_default))
            if defaults:
                for field_name, field_default in defaults:
                    self.write_line(f, 2, f"self.{field_name} = {field_default}")
            else:
                self.write_line(f, 2, f"pass")

            self.write_src_body(f)
            self.write_line(f)
