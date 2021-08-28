import collections
from .BaseClass import BaseClass
from .Union import Union, get_params

FIELD_TYPES = ("add", "field")
VER = "self.context.version"


class Compound(BaseClass):

	def read(self):
		"""Create a self.struct class"""
		super().read()

		self.field_unions = []
		for field in self.struct:
			if field.tag in FIELD_TYPES:
				field_name = field.attrib["name"]
				if self.field_unions and self.field_unions[-1].name == field_name:
					union = self.field_unions[-1]
				else:
					union = Union(self, field_name)
					self.field_unions.append(union)
				union.append(field)
			arg, template, arr1, arr2, conditionals, field_name, field_type, pad_mode = get_params(field)
			if arr1:
				self.imports.add("numpy")

		# write to python file
		with open(self.out_file, "w") as f:
			# write the header stuff
			super().write(f)

			if not self.class_basename:
				f.write(f"\n\n\tcontext = ContextReference()")

			# check all fields/members in this class and write them as fields
			# for union in self.field_unions.values():
			# 	union.write_declaration(f)

			if "def __init__" not in self.src_code:
				f.write(f"\n\n\tdef __init__(self, context, arg=None, template=None):")
				f.write(f"\n\t\tself.name = ''")
				# classes that this class inherits from have to be read first
				if self.class_basename:
					f.write(f"\n\t\tsuper().__init__(context, arg, template)")
				else:
					f.write(f"\n\t\tself._context = context")
				f.write(f"\n\t\tself.arg = arg")
				f.write(f"\n\t\tself.template = template")
				f.write(f"\n\t\tself.io_size = 0")
				f.write(f"\n\t\tself.io_start = 0")

				for union in self.field_unions:
					union.write_init(f)

			# write the load() method
			for method_type in ("read", "write"):
				# check all fields/members in this class and write them as fields
				if f"def {method_type}(" in self.src_code:
					continue
				f.write(f"\n\n\tdef {method_type}(self, stream):")
				f.write(f"\n\n\t\tself.io_start = stream.tell()")
				last_condition = ""
				# classes that this class inherits from have to be read first
				if self.class_basename:
					f.write(f"\n\t\tsuper().{method_type}(stream)")
				for union in self.field_unions:
					last_condition = union.write_io(f, method_type, last_condition)

				f.write(f"\n\n\t\tself.io_size = stream.tell() - self.io_start")

			if "def __repr__(" not in self.src_code:
				f.write(f"\n\n\tdef get_info_str(self):")
				f.write(f"\n\t\treturn f'{self.class_name} [Size: {{self.io_size}}, Address: {{self.io_start}}] {{self.name}}'")

				f.write(f"\n\n\tdef get_fields_str(self):")
				f.write(f"\n\t\ts = ''")
				if self.class_basename:
					f.write(f"\n\t\ts += super().get_fields_str()")
				for union in self.field_unions:
					rep = f"self.{union.name}.__repr__()"
					f.write(f"\n\t\ts += f'\\n\t* {union.name} = {{{rep}}}'")
				f.write(f"\n\t\treturn s")

				f.write(f"\n\n\tdef __repr__(self):")
				f.write(f"\n\t\ts = self.get_info_str()")
				f.write(f"\n\t\ts += self.get_fields_str()")
				f.write(f"\n\t\ts += '\\n'")
				f.write(f"\n\t\treturn s")

			f.write(self.grab_src_snippet("# START_CLASS"))
			f.write(f"\n")
		# self.get_static_dtype()

	def get_static_dtype(self):
		dtypes = [union.get_basic_type() for union in self.field_unions]
		if None not in dtypes:
			print(self.class_name, dtypes)
		else:
			print(self.class_name, "NOT static")
