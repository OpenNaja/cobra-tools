import copy
from html import unescape
import os
import xml.etree.ElementTree as ET

from .expression import Expression 

# filter the nif xml based on a given version
# everything will be removed except main_tags that have matching versions, main_types that have matching versions
# and any type or module that they contain


main_tags = ("niobject")
main_types = ("Header", "Footer")


struct_types = ("compound", "niobject", "struct")
bitstruct_types = ("bitfield", "bitflags", "bitstruct")
type_tags = struct_types + bitstruct_types + ("enum", "basic")


def possible_value_combos(possible_values):
	if len(possible_values) <= 1:
		return possible_values
	else:
		possible_combos = []
		for value in possible_values[0]:
			for combo in possible_value_combos(possible_values[1:]):
				possible_combos.append((value,) + combo)
		return tuple(possible_combos)


class XmlVersionFilter:
	"""No support for xmlInclude as of yet."""


	def __init__(self, version):
		"""If version is a string, it is interpreted as a version ID. Otherwise, it is assumed to be an iterator of
		possible verattr values. For example, you could pass 
		'V20_2_0_7__11_8'
		or
		((0x14020007,), (11,), (30, 31, 32, 33))
		for the same effect.
		For a simple run:
		test = XmlVersionFilter('VersionID')
		test.read_xml(in_xml_path)
		test.process_types()
		test.write_xml(out_xml_path)"""
		# if version is a string, it is a version ID
		# else, interpret an iterator as verattrs
		self.version_name = version if isinstance(version, str) else None
		# tuple of verattrs ints for the passed version
		self.version_tuple = None if isinstance(version, str) else tuple(tuple(int(i) for i in value) for value in version)
		# all possible combinations that could be the result of that
		self.version_combinations = None if isinstance(version, str) else possible_value_combos(version)

		# python-converted variables
        # ordered (!) list of tuples ([tokens], (target_attribs)) for each <token>
		self.token_list = []
		# map of versions to their tuple
		self.version_map = {}
		# ordered list of verattrs, verattrs with unspecified index are last
		# items in this list are (verattr_name, verattr_access, verattr_index)
		self.verattrs_list = []
		# version IDs of all versions which match the verattr
		self.matching_versions = [version] if isinstance(version, str) else []

		# root element
		self.root = None

		# tags which can be filtered as you read the xml or don't need filtering
		self.tokens = []
		self.verattrs = []
		self.versions = []

		# tags which must be filtered after going through the whole xml
		self.all_modules = {}
		self.maintained_modules = {}
		self.all_types = {}
		self.maintained_types = {}

		pass

	def read_xml(self, xml_path):
		tree = ET.parse(xml_path)
		self.root = tree.getroot()
		
		for child in self.root:
			if child.tag == "token":
				self.read_token(child)
			elif child.tag == "verattr":
				self.read_verattr(child)
			elif child.tag == "version":
				self.read_version(child)
			elif child.tag == "module":
				self.read_module(child)
			elif child.tag in type_tags:
				self.read_type(child)
			else:
				raise AttributeError(f"Unknown tag {child.tag}")
		self.process_types()
		self.process_modules()

	def write_xml(self, out_path):
		# create root
		root = ET.Element(self.root.tag, attrib=self.root.attrib)
		# add tokens
		for token in self.tokens:
			root.append(token)
		# add verattrs
		for verattr in self.verattrs:
			root.append(verattr)
		# add versions
		for version in self.versions:
			root.append(version)
		# add modules - go by original order
		for module_name in self.all_modules:
			if module_name in self.maintained_modules:
				root.append(self.maintained_modules[module_name])
		# add types - go by original order
		for type_name in self.all_types:
			if type_name in self.maintained_types:
				root.append(self.maintained_types[type_name])
		# write the xml
		tree = ET.ElementTree(root)
		tree.write(out_path)

	def read_token(self, token_element):
		# do other things
		self.tokens.append(token_element)
		# do the processing
		token_attribs = token_element.get("attrs").split()
		tokens = []
		for child_token in token_element:
			tokens.append((child_token.get("token"), child_token.get("string")))
		self.token_list.append((tokens, token_attribs))

	def read_verattr(self, verattr_elem):
		self.verattrs.append(verattr_elem)
		verattr_name = self.get_attrib(verattr_elem, "name")
		verattr_access = self.get_attrib(verattr_elem, "access")
		verattr_index = self.get_attrib(verattr_elem, "index")
		verattr_index = Expression(verattr_index).eval() if verattr_index is not None else float("inf")
		verattr_tuple = (verattr_name, verattr_access, verattr_index)
		self.verattrs_list.append(verattr_tuple)
		self.verattrs_list = sorted(self.verattrs_list, key=lambda x: x[2])

	def read_version(self, version_elem):
		if version_elem.tag in main_tags:
			self.versions.append(version_elem)
		version_name = self.get_attrib(version_elem, "id")
		value_list = []
		for attr_name, attr_access, attr_index in self.verattrs_list:
			attr_value = self.get_attrib(version_elem, attr_name, "0")
			value_list.append(tuple(Expression(value).eval() for value in attr_value.split()))
		value_list = tuple(value_list)
		self.version_map[version_name] = value_list
		if self.version_name is not None:
			if version_name == self.version_name:
				if version_elem not in self.versions:
					self.versions.append(version_elem)
				# create the version tuple
				self.version_tuple = value_list
				self.version_combinations = possible_value_combos(self.version_tuple)
				return True
			return False
		else:
			for elem_values, self_values in zip(value_list, self.version_tuple):
				if not any(i in self_values for i in elem_values):
					return False
			else:
				self.matching_versions.append(version_name)
				if version_elem not in self.versions:
					self.versions.append(version_elem)
				return True

	def read_module(self, module_elem):
		module_name = self.get_attrib(module_elem, "name")
		self.all_modules[module_name] = module_elem

	def is_matching(self, elem):
		"""Return True if this element's can occur with the given versions."""
		matching = True

		# check versions
		possible_versions = self.get_attrib(elem, "versions")
		if possible_versions is not None:
			matching &= any(version in self.matching_versions for version in possible_versions.split())

		# check since and until
		since = self.get_attrib(elem, "since")
		if since is not None:
			# since for a type is a version ID, but for a field it's version literal
			if since in self.version_map:
				for i, values in enumerate(self.version_map[since]):
					matching &= self.version_tuple[i][-1] >= values[0]
			else:
				for i, value in enumerate(since.split()):
					matching &= self.version_tuple[i][-1] >= Expression(value).eval()
		until = self.get_attrib(elem, "until")
		if until is not None:
			# until for a type is a version ID, but for a field it's version literal
			if until in self.version_map:
				for i, values in enumerate(self.version_map[until]):
					matching &= self.version_tuple[i][0] <= values[-1]
			else:
				for i, value in enumerate(until.split()):
					matching &= self.version_tuple[i][0] <= Expression(value).eval()

		# check vercond
		vercond = self.get_attrib(elem, "vercond")
		if vercond is not None:
			ver_expr = Expression(vercond)
			matching &= any(bool(ver_expr.eval(namespace)) for namespace in self.verattr_namespaces)
		return matching

	def strip_attributes(self, elem):
		"""Remove every conditioning attribute which is always True for self's versions."""
		# check versions
		possible_versions = self.get_attrib(elem, "versions")
		if possible_versions is not None:
			if all(version in self.matching_versions for version in possible_versions.split()):
				elem.attrib.pop("versions")

		# check since and until
		since = self.get_attrib(elem, "since")
		if since is not None:
			strict_match = True
			# since for a type is a version ID, but for a field it's version literal
			if since in self.version_map:
				for i, values in enumerate(self.version_map[since]):
					strict_match &= self.version_tuple[i][0] >= values[-1]
			else:
				for i, value in enumerate(since.split()):
					strict_match &= self.version_tuple[i][0] >= Expression(value).eval()
			if strict_match:
				# matches in all existing cases
				elem.attrib.pop("since")
		until = self.get_attrib(elem, "until")
		if until is not None:
			strict_match = True
			# until for a type is a version ID, but for a field it's version literal
			if until in self.version_map:
				for i, values in enumerate(self.version_map[until]):
					strict_match &= self.version_tuple[i][-1] <= values[0]
			else:
				for i, value in enumerate(until.split()):
					strict_match &= self.version_tuple[i][-1] <= Expression(value).eval()
			if strict_match:
				# matches in all existing cases
				elem.attrib.pop("until")

		# check vercond
		vercond = self.get_attrib(elem, "vercond")
		if vercond is not None:
			ver_expr = Expression(vercond)
			if all(bool(ver_expr.eval(namespace)) for namespace in self.verattr_namespaces):
				elem.attrib.pop("vercond")
		return elem

	def read_type(self, type_elem):
		type_name = self.get_attrib(type_elem, "name")
		# filter on the copy
		self.all_types[type_name] = type_elem

	def filter_subelem(self, type_elem):
		for sub_elem in list(type_elem):
			if not self.is_matching(sub_elem):
				type_elem.remove(sub_elem)
			else:
				self.strip_attributes(sub_elem)
				self.filter_subelem(sub_elem)

	def process_type(self, type_elem):
		type_name = self.get_attrib(type_elem, "name")
		type_elem = copy.deepcopy(type_elem)
		self.maintained_types[type_name] = type_elem
		# remove unused attributes
		self.strip_attributes(type_elem)
		# remove any non-used fields for this version
		self.filter_subelem(type_elem)
		# scan fields to see if they use other types
		if type_elem.tag in struct_types or type_elem.tag in bitstruct_types:
			for field in type_elem:
				for field_type in (self.get_attrib(field, "type"), self.get_attrib(field, "template")):
					if field_type is not None and field_type != "#T#":
						if field_type not in self.maintained_types:
							self.process_type(self.all_types[field_type])

	def process_types(self):
		"""Go through all_types and fill maintained_types with the filtered equivalent xml Elements"""
		# create the namespaces to be used for verattr checking
		version_combinations = possible_value_combos(self.version_tuple)
		self.verattr_namespaces = []
		for combo in version_combinations:
			namespace_dict = {str(Expression(verattr[1])): value for verattr, value in zip(self.verattrs_list, combo)}
			self.verattr_namespaces.append(namespace_dict)
		# go through every type and add it and its matching fields if it exists
		for name, type_elem in self.all_types.items():
			if type_elem.tag in main_tags or name in main_types:
				if self.is_matching(type_elem):
					self.process_type(type_elem)
		# at the very end, process onlyT and excludeT, because only then do we know which types occur
		for name, type_elem in self.maintained_types.items():
			for field in list(type_elem):
				onlyT = self.get_attrib(field, "onlyT")
				if onlyT is not None:
					if onlyT not in self.maintained_types:
						type_elem.remove(field)
						continue
				excludeT = self.get_attrib(field, "excludeT")
				if excludeT is not None and excludeT not in self.maintained_types:
					field.attrib.pop("excludeT")
				for default in list(field):
					onlyT = self.get_attrib(default, "onlyT")
					if onlyT is not None:
						if onlyT not in self.maintained_types:
							field.remove(default)
							continue
					excludeT = self.get_attrib(default, "excludeT")
					if excludeT is not None and excludeT not in self.maintained_types:
						default.attrib.pop("excludeT")

	def maintain_module(self, module_name):
		if module_name in self.maintained_modules: return
		module_elem = self.all_modules[module_name]
		self.maintained_modules[module_name] = module_elem
		depend_modules = self.get_attrib(module_elem, 'depends', '').split()
		for d_module in depend_modules:
			self.maintain_module(d_module)

	def process_modules(self):
		"""Go through all maintained types to see which modules to maintain."""
		for class_elem in self.maintained_types.values():
			module_name = self.get_attrib(class_elem, 'module')
			if module_name:
				self.maintain_module(module_name)

	def apply_tokens(self, attrib_text, attrib_name):
		for tokens, target_attribs in self.token_list:
			if attrib_name in target_attribs:
				for op_token, op_str in tokens:
					attrib_text = attrib_text.replace(op_token, op_str)
		attrib_text = unescape(attrib_text)
		return attrib_text

	def get_attrib(self, element, attrib_name, default=None):
		attrib_text = element.get(attrib_name, default)
		# apply tokens
		if isinstance(attrib_text, str):
			return self.apply_tokens(attrib_text, attrib_name)
		else:
			return attrib_text

