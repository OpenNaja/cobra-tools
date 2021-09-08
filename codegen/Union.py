from codegen.expression import Expression, Version
from codegen.Versions import Versions
from .naming_conventions import clean_comment_str

VER = "self.context.version"


def get_attr_with_backups(field, attribute_keys):
	# return the value of the first attribute in the list that is not empty or
	# missing
	for key in attribute_keys:
		attr_value = field.attrib.get(key)
		if attr_value:
			return attr_value
	else:
		return None

def get_conditions(field):
	conditionals = []
	ver1 = get_attr_with_backups(field, ["ver1", "since"])
	if ver1:
		ver1 = Version(ver1)
	ver2 = get_attr_with_backups(field, ["ver2", "until"])

	if ver2:
		ver2 = Version(ver2)
	vercond = field.attrib.get("vercond")
	versions = field.attrib.get("versions")
	if versions:
		versions = [Versions.format_id(version) for version in versions.split(" ")]
	cond = field.attrib.get("cond")
	onlyT = field.attrib.get("onlyT")
	excludeT = field.attrib.get("excludeT")
	if ver1 and ver2:
		conditionals.append(f"{ver1} <= {VER} <= {ver2}")
	elif ver1:
		conditionals.append(f"{VER} >= {ver1}")
	elif ver2:
		conditionals.append(f"{VER} <= {ver2}")
	if vercond:
		vercond = Expression(vercond)
		conditionals.append(f"{vercond}")
	if versions:
		conditionals.append(f"({' or '.join([f'is_{version}(self.context)' for version in versions])})")
	if cond:
		cond = Expression(cond)
		conditionals.append(f"{cond}")
	if onlyT:
		conditionals.append(f"isinstance(self, {onlyT})")
	if excludeT:
		conditionals.append(f"not isinstance(self, {excludeT})")
	return conditionals

def get_params(field):
	# parse all attributes and return the python-evaluatable string

	field_name = field.attrib["name"]
	field_type = field.attrib["type"]
	pad_mode = field.attrib.get("padding")
	template = field.attrib.get("template")

	conditionals = get_conditions(field)

	arg = field.attrib.get("arg")
	arr1 = get_attr_with_backups(field, ["arr1", "length"])
	arr2 = get_attr_with_backups(field, ["arr2", "width"])
	if arg:
		arg = Expression(arg)
	if arr1:
		arr1 = Expression(arr1)
	if arr2:
		arr2 = Expression(arr2)
	return arg, template, arr1, arr2, conditionals, field_name, field_type, pad_mode

def condition_indent(base_indent, conditionals, last_condition=""):
	# determine the python condition and indentation level based on whether the
	# last used condition was the same.
	if conditionals:
		new_condition = f"if {' and '.join(conditionals)}:"
		# merge subsequent fields that have the same condition
		if last_condition != new_condition:
			last_condition = new_condition
		else:
			new_condition=""
		indent = base_indent + "\t"
	else:
		indent = base_indent
		new_condition = ""

	return indent, new_condition, last_condition

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
			# todo - make consistent / merge with map_type()
			if field_type.lower() in ("byte", "ubyte", "short", "ushort", "int", "uint", "int64", "uint64"):
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

	def get_basic_type(self):
		"""If this union has just one field, return its dtype if it is basic"""
		# types = set(field.attrib["type"] for field in self.members)
		if len(self.members) == 1:
			field = self.members[0]
			t = field.attrib["type"]
			if self.compound.parser.tag_dict[t.lower()] == "basic":
				return t

	def get_default_string(self, default_string, arg, template, arr1, arr2, field_name, field_type):
		# get the default (or the best guess of it)
		field_type_lower = field_type.lower()
		if field_type_lower in self.compound.parser.tag_dict:
			type_of_field_type = self.compound.parser.tag_dict[field_type_lower]
			# get the field's default, if it exists
			if default_string:
				# we have to check if the default is an enum default value, in which case it has to be a member of that enum
				if type_of_field_type == "enum":
					default_string = f'{field_type}.{default_string}'
			# no default, so guess one
			else:
				if type_of_field_type in ("compound", "struct", "niobject", "enum", "bitfield", "bitflags", "bitstruct"):
					if type_of_field_type in self.compound.parser.struct_types:
						arguments = f"context, {arg}, {template}"
					else:
						arguments = ""
					default_string = f"{field_type}({arguments})"
				else:
					default_string = 0

		if arr1:
			default_string = "Array()"
			if self.compound.parser.tag_dict[field_type_lower] == "basic":
				valid_arrs = tuple(str(arr) for arr in (arr1, arr2) if arr and ".arg" not in str(arr))
				arr_str = ", ".join(valid_arrs)
				if field_type_lower in ("ubyte", "byte", "short", "ushort", "int", "uint", "uint64", "int64", "float"):
					default_string = f"numpy.zeros(({arr_str}), dtype='{field_type_lower}')"
				# todo - if we do this, it breaks when arg is used in array
				# default_string = f"[{default_string} for _ in range({Expression(arr1)})]"
		return default_string

	def default_assigns(self, field, arg, template, arr1, arr2, field_name, field_type, base_indent):
		field_default = self.get_default_string(field.attrib.get('default'), arg, template, arr1, arr2, field_name, field_type)
		default_children = field.findall("default")
		if default_children:
			defaults = [(f'{base_indent}else:', f'{base_indent}\tself.{field_name} = {field_default}')]
			last_default = len(default_children)-1
			last_condition = ""
			for i, default_element in enumerate(default_children):

				# get the condition
				conditions = get_conditions(default_element)
				indent, condition, last_condition = condition_indent(base_indent, conditions, last_condition)
				if not condition:
					raise AttributeError(f"Default tag without or with overlapping conditions on {field.attrib['name']} {condition} {default_element.get('value')}")
				if i != last_default:
					condition = f'{base_indent}el{condition}'
				else:
					condition = f'{base_indent}{condition}'

				default = self.get_default_string(default_element.attrib.get("value"), arg, template, arr1, arr2, field_name, field_type)
				defaults.append((condition, f'{indent}self.{field_name} = {default}'))

			defaults = defaults[::-1]
		else:
			defaults = [("", f'{base_indent}self.{field_name} = {field_default}')]
		return defaults

	def write_init(self, f):
		last_condition=""
		base_indent = "\n\t\t"
		for field in self.members:
			field_debug_str = clean_comment_str(field.text, indent="\t\t")
			arg, template, arr1, arr2, conditionals, field_name, field_type, pad_mode = get_params(field)
			if field_debug_str.strip():
				f.write(field_debug_str)

			indent, new_condition, last_condition = condition_indent(base_indent, conditionals, last_condition)
			if new_condition:
				f.write(f"{base_indent}{new_condition}")

			defaults = self.default_assigns(field, arg, template, arr1, arr2, field_name, field_type, indent)
			for condition, default in defaults:
				if condition:
					f.write(condition)
				f.write(default)

	def write_io(self, f, method_type, last_condition=""):
		base_indent = "\n\t\t"
		for field in self.members:
			arg, template, arr1, arr2, conditionals, field_name, field_type, pad_mode = get_params(field)
			indent, new_condition, last_condition = condition_indent(base_indent, conditionals, last_condition)
			if new_condition:
				f.write(f"{base_indent}{new_condition}")
			if arr1:
				if self.compound.parser.tag_dict[field_type.lower()] == "basic":
					valid_arrs = tuple(str(arr) for arr in (arr1, arr2) if arr)
					arr_str = ", ".join(valid_arrs)
					if method_type == "read":
						f.write(f"{indent}self.{field_name} = stream.{method_type}_{field_type.lower()}s(({arr_str}))")
					else:
						if pad_mode:
							# resize numpy arrays that represent padding so we need not worry about them
							f.write(f"{indent}self.{field_name}.resize(({arr_str}))")
						f.write(f"{indent}stream.{method_type}_{field_type.lower()}s(self.{field_name})")
				else:
					f.write(f"{indent}self.{field_name}.{method_type}(stream, {field_type}, {arr1}, {arr2})")
			else:
				f.write(
					f"{indent}{self.compound.parser.method_for_type(field_type, mode=method_type, attr=f'self.{field_name}', arg=arg, template=template)}")
			# store version related stuff on stream
			if "version" in field_name:
				f.write(f"{indent}stream.{field_name} = self.{field_name}")
		return last_condition
