import collections
from .BaseClass import BaseClass

from codegen.expression import Expression, Version
from .naming_conventions import clean_comment_str

FIELD_TYPES = ("add", "field")
VER = "stream.version"


class Compound(BaseClass):

	def read(self):
		"""Create a self.struct class"""
		super().read()

		field_unions_dict = collections.OrderedDict()
		for field in self.struct:
			if field.tag in FIELD_TYPES:
				field_name = field.attrib["name"]
				if field_name not in field_unions_dict:
					field_unions_dict[field_name] = []
				else:
					# field exists and we add to it, so we have an union and must import typing module
					self.imports.add("typing")
				field_unions_dict[field_name].append(field)

		# write to python file
		with open(self.out_file, "w") as f:
			# write the header stuff
			super().write(f)

			# check all fields/members in this class and write them as fields
			for field_name, union_members in field_unions_dict.items():
				field_types = []
				for field in union_members:
					field_type = field.attrib["type"]
					# todo - make consisten / merge with map_type()
					if field_type == "self.template":
						field_type = "typing.Any"
						self.imports.add("typing")
					elif field_type.lower() in ("byte", "ubyte", "short", "ushort", "int", "uint", "int64", "uint64"):
						field_type = "int"
					elif field_type.lower() in ("float", "hfloat"):
						field_type = "float"
					elif field_type.lower() in ("bool",):
						field_type = "bool"
					field_types.append(field_type)
					field_default = field.attrib.get("default")
					field_debug_str = clean_comment_str(field.text, indent="\t")

					if field_debug_str.strip():
						f.write(field_debug_str)
				field_types = set(field_types)
				if len(field_types) > 1:
					field_types_str = f"typing.Union[{', '.join(field_types)}]"
				else:
					field_types_str = field_type

				# write the field type
				# arrays
				if field.attrib.get("arr1"):
					f.write(f"\n\t{field_name}: typing.List[{field_types_str}]")
				# plain
				else:
					f.write(f"\n\t{field_name}: {field_types_str}")

				# write the field's default, if it exists
				if field_default:
					# we have to check if the default is an enum default value, in which case it has to be a member of that enum
					if self.parser.tag_dict[field_type.lower()] == "enum":
						field_default = field_type+"."+field_default
					f.write(f" = {field_default}")

				# todo - handle several defaults? maybe save as docstring
				# load defaults for this <field>
				# for default in field:
				#     if default.tag != "default":
				#         raise AttributeError("self.struct children's children must be 'default' tag")

			if "def __init__" not in self.src_code:
				f.write(f"\n\n\tdef __init__(self, arg=None, template=None):")
				# classes that this class inherits from have to be read first
				if self.class_basename:
					f.write(f"\n\t\tsuper().__init__(arg, template)")
				f.write(f"\n\t\tself.arg = arg")
				f.write(f"\n\t\tself.template = template")
				f.write(f"\n\t\tself.io_size = 0")

				for field in self.struct:
					if field.tag in FIELD_TYPES:
						field_name = field.attrib["name"]
						field_type = field.attrib["type"]
						field_default = field.attrib.get("default")
						if field_type.lower() in self.parser.tag_dict:
							type_of_field_type = self.parser.tag_dict[field_type.lower()]
							# write the field's default, if it exists
							if field_default:
								# we have to check if the default is an enum default value, in which case it has to be a member of that enum
								if type_of_field_type == "enum":
									field_default = field_type + "." + field_default
							# no default, so guess one
							else:
								if type_of_field_type in ("compound", "niobject"):
									field_default = f"{field_type}()"
						if not field_default:
							field_default = 0
						f.write(f"\n\t\tself.{field_name} = {field_default}")

			# write the load() method
			for method_type in ("read", "write"):
				# check all fields/members in this class and write them as fields
				if f"def {method_type}(" in self.src_code:
					continue
				f.write(f"\n\n\tdef {method_type}(self, stream):")
				f.write(f"\n\n\t\tio_start = stream.tell()")
				last_condition = ""
				# classes that this class inherits from have to be read first
				if self.class_basename:
					f.write(f"\n\t\tsuper().{method_type}(stream)")

				for field in self.struct:
					if field.tag in FIELD_TYPES:
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

						f.write(f"{indent}{self.parser.method_for_type(field_type, mode=method_type, attr=f'self.{field_name}', arr1=arr1, arg=arg)}")
						# store version related stuff on stream
						if "version" in field_name:
							f.write(f"{indent}stream.{field_name} = self.{field_name}")
				f.write(f"\n\n\t\tself.io_size = stream.tell() - io_start")

			if "def __repr__(" not in self.src_code:
				f.write(f"\n\n\tdef __repr__(self):")
				f.write(f"\n\t\ts = '{self.class_name} [Size: '+str(self.io_size)+']'")
				for field_name in field_unions_dict.keys():
					f.write(f"\n\t\ts += '\\n\t* {field_name} = ' + self.{field_name}.__repr__()")
				f.write(f"\n\t\ts += '\\n'")
				f.write(f"\n\t\treturn s")

			f.write(self.grab_src_snippet("# START_CLASS"))
			f.write(f"\n")

