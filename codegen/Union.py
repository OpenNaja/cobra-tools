from codegen.expression import Expression, Version
from .naming_conventions import clean_comment_str

VER = "stream.version"


class Union:
	def __init__(self, compound, union_name):
		self.compound = compound
		self.name = union_name
		self.members = []
	
	def append(self, member):
		self.members.append(member)
	
	def write_declaration(self, f):

		field_types = []
		for field in self.members:
			field_type = field.attrib["type"]
			# todo - make consisten / merge with map_type()
			if field_type == "self.template":
				field_type = "typing.Any"
				self.compound.imports.add("typing")
			elif field_type.lower() in ("byte", "ubyte", "short", "ushort", "int", "uint", "int64", "uint64"):
				field_type = "int"
			elif field_type.lower() in ("float", "hfloat"):
				field_type = "float"
			elif field_type.lower() in ("bool",):
				field_type = "bool"
			elif field_type.lower() in ("zstring", "string", "sizedstring"):
				field_type = "str"
			field_types.append(field_type)
			field_default = field.attrib.get("default")
			field_debug_str = clean_comment_str(field.text, indent="\t")
	
			if field_debug_str.strip():
				f.write(field_debug_str)
		field_types = set(field_types)
		if len(field_types) > 1:
			field_types_str = f"typing.Union[{', '.join(sorted(field_types))}]"
		else:
			field_types_str = field_type
	
		# write the field type
		# arrays
		if field.attrib.get("arr1"):
			f.write(f"\n\t{self.name}: typing.List[{field_types_str}]")
		# plain
		else:
			f.write(f"\n\t{self.name}: {field_types_str}")
	
		# write the field's default, if it exists
		if field_default:
			# we have to check if the default is an enum default value, in which case it has to be a member of that enum
			if self.compound.parser.tag_dict[field_type.lower()] == "enum":
				field_default = field_type + "." + field_default
			f.write(f" = {field_default}")
	
	# todo - handle several defaults? maybe save as docstring
	# load defaults for this <field>
	# for default in field:
	#     if default.tag != "default":
	#         raise AttributeError("self.struct children's children must be 'default' tag")

	def get_basic_type(self):
		"""If this union has just one field, return its dtype if it is basic"""
		# types = set(field.attrib["type"] for field in self.members)
		if len(self.members) == 1:
			field = self.members[0]
			t = field.attrib["type"]
			if self.compound.parser.tag_dict[t.lower()] == "basic":
				return t

	def write_init(self, f):
		for field in self.members:
			field_debug_str = clean_comment_str(field.text, indent="\t\t")

			if field_debug_str.strip():
				f.write(field_debug_str)
			field_name = field.attrib["name"]
			field_type = field.attrib["type"]
			field_default = field.attrib.get("default")
			if field_type.lower() in self.compound.parser.tag_dict:
				type_of_field_type = self.compound.parser.tag_dict[field_type.lower()]
				# write the field's default, if it exists
				if field_default:
					# we have to check if the default is an enum default value, in which case it has to be a member of that enum
					if type_of_field_type == "enum":
						field_default = field_type + "." + field_default
				# no default, so guess one
				else:
					if type_of_field_type in (
					"compound", "struct", "niobject", "enum", "bitfield", "bitflags", "bitstruct"):
						field_default = f"{field_type}()"
			if not field_default:
				field_default = 0
			arr1 = field.attrib.get("arr1")
			if arr1:
				field_default = "Array()"
			# todo - if we do this, it breaks when arg is used in array
			# field_default = f"[{field_default} for _ in range({Expression(arr1)})]"
			f.write(f"\n\t\tself.{field_name} = {field_default}")

	def write_io(self, f, method_type, last_condition=""):

		for field in self.members:
			field_name = field.attrib["name"]
			field_type = field.attrib["type"]

			# parse all conditions
			conditionals = []
			ver1 = field.attrib.get("ver1")
			ver2 = field.attrib.get("ver2")
			if ver1:
				ver1 = Version(ver1)
			if ver2:
				ver2 = Version(ver2)
			vercond = field.attrib.get("vercond")
			cond = field.attrib.get("cond")

			if ver1 and ver2:
				conditionals.append(f"{ver1} <= {VER} < {ver2}")
			elif ver1:
				conditionals.append(f"{VER} >= {ver1}")
			elif ver2:
				conditionals.append(f"{VER} < {ver2}")
			if vercond:
				vercond = Expression(vercond)
				conditionals.append(f"{vercond}")
			if cond:
				cond = Expression(cond)
				conditionals.append(f"{cond}")
			if conditionals:
				new_condition = f"if {' and '.join(conditionals)}:"
				# merge subsequent fields that have the same condition
				if last_condition != new_condition:
					f.write(f"\n\t\t{new_condition}")
				indent = "\n\t\t\t"
			else:
				indent = "\n\t\t"
				new_condition = ""
			last_condition = new_condition
			template = field.attrib.get("template")
			if template:
				template_str = f"template={template}"
				f.write(f"{indent}# TEMPLATE: {template_str}")
			else:
				template_str = ""
			arr1 = field.attrib.get("arr1")
			arr2 = field.attrib.get("arr2")
			arg = field.attrib.get("arg")
			if arg:
				arg = Expression(arg)

			if arr1:
				arr1 = Expression(arr1)
			if arr2:
				arr2 = Expression(arr2)
			if arr1:
				if self.compound.parser.tag_dict[field_type.lower()] == "basic":
					ftype = f"'{field_type}'"
				else:
					ftype = field_type
				f.write(f"{indent}self.{field_name}.{method_type}(stream, {ftype}, {arr1}, {arr2})")
			else:
				f.write(
				f"{indent}{self.compound.parser.method_for_type(field_type, mode=method_type, attr=f'self.{field_name}', arr1=arr1, arg=arg)}")
			# store version related stuff on stream
			if "version" in field_name:
				f.write(f"{indent}stream.{field_name} = self.{field_name}")
		return last_condition
