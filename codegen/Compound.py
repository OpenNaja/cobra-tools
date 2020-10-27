import collections
from .BaseClass import BaseClass
from .Union import Union

FIELD_TYPES = ("add", "field")
VER = "stream.version"


class Compound(BaseClass):

	def read(self):
		"""Create a self.struct class"""
		super().read()

		self.field_unions_dict = collections.OrderedDict()
		for field in self.struct:
			if field.tag in FIELD_TYPES:
				field_name = field.attrib["name"]
				if field_name not in self.field_unions_dict:
					self.field_unions_dict[field_name] = Union(self, field_name)
				else:
					# field exists and we add to it, so we have an union and must import typing module
					self.imports.add("typing")
				self.field_unions_dict[field_name].append(field)

		# write to python file
		with open(self.out_file, "w") as f:
			# write the header stuff
			super().write(f)

			# check all fields/members in this class and write them as fields
			# for union in self.field_unions_dict.values():
			# 	union.write_declaration(f)

			if "def __init__" not in self.src_code:
				f.write(f"\n\n\tdef __init__(self, arg=None, template=None):")
				# classes that this class inherits from have to be read first
				if self.class_basename:
					f.write(f"\n\t\tsuper().__init__(arg, template)")
				f.write(f"\n\t\tself.arg = arg")
				f.write(f"\n\t\tself.template = template")
				f.write(f"\n\t\tself.io_size = 0")
				f.write(f"\n\t\tself.io_start = 0")

				for union in self.field_unions_dict.values():
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

				for union in self.field_unions_dict.values():
					last_condition = union.write_io(f, method_type, last_condition)

				f.write(f"\n\n\t\tself.io_size = stream.tell() - self.io_start")

			if "def __repr__(" not in self.src_code:
				f.write(f"\n\n\tdef __repr__(self):")
				f.write(f"\n\t\ts = '{self.class_name} [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'")
				for field_name in self.field_unions_dict.keys():
					f.write(f"\n\t\ts += '\\n\t* {field_name} = ' + self.{field_name}.__repr__()")
				f.write(f"\n\t\ts += '\\n'")
				f.write(f"\n\t\treturn s")

			f.write(self.grab_src_snippet("# START_CLASS"))
			f.write(f"\n")
		# self.get_static_dtype()

	def get_static_dtype(self):
		dtypes = [union.get_basic_type() for union in self.field_unions_dict.values()]
		if None not in dtypes:
			print(self.class_name, dtypes)
		else:
			print(self.class_name, "NOT static")
