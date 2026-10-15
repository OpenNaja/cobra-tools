from copy import deepcopy
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ppuipkg.imports import name_type_map


class PPUIPKGRoot(MemStruct):

	__name__ = 'PPUIPKGRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.files_count = name_type_map['Uint64'](self.context, 0, None)
		self.icondata_count = name_type_map['Uint64'](self.context, 0, None)
		self.basic_path = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.files = name_type_map['ArrayPointer'](self.context, self.files_count, name_type_map['Ppuipkgfile'])
		self.icondata = name_type_map['ArrayPointer'](self.context, self.icondata_count, name_type_map['UserInterfaceIconData'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'basic_path', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'files_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'files', name_type_map['ArrayPointer'], (None, name_type_map['Ppuipkgfile']), (False, None), (None, None)
		yield 'icondata_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'icondata', name_type_map['ArrayPointer'], (None, name_type_map['UserInterfaceIconData']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'basic_path', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'files_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'files', name_type_map['ArrayPointer'], (instance.files_count, name_type_map['Ppuipkgfile']), (False, None)
		yield 'icondata_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'icondata', name_type_map['ArrayPointer'], (instance.icondata_count, name_type_map['UserInterfaceIconData']), (False, None)

	XML_ATTRIBUTE_ALIASES = {
		"file_count": "files_count",
	}
	XML_ELEMENT_ALIASES = {
		"types": "icondata",
	}
	XML_ICON_ELEMENT_ALIASES = {
		"asset_package": "ovs",
		"assetPackage": "ovs",
	}

	@staticmethod
	def _rename_xml_children(elem, aliases):
		"""Normalize legacy child names; an existing canonical child wins."""
		for old, new in aliases.items():
			for child in list(elem.findall(old)):
				if elem.find(new) is None:
					child.tag = new
				else:
					elem.remove(child)

	@classmethod
	def _from_xml(cls, instance, elem):
		# Preserve the caller's XML, including its original spellings.
		elem = deepcopy(elem)
		for old, new in cls.XML_ATTRIBUTE_ALIASES.items():
			if old in elem.attrib:
				value = elem.attrib.pop(old)
				elem.attrib.setdefault(new, value)

		cls._rename_xml_children(elem, cls.XML_ELEMENT_ALIASES)
		icons = elem.find("icondata")
		if icons is not None:
			for icon in icons:
				cls._rename_xml_children(icon, cls.XML_ICON_ELEMENT_ALIASES)

		return super()._from_xml(instance, elem)

