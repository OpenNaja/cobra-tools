# START_GLOBALS
from copy import deepcopy
# END_GLOBALS


class PPUIPKGRoot:
	# START_CLASS

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
