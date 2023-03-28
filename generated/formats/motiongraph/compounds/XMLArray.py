from generated.array import Array
from generated.formats.motiongraph.compounds.XMLEntry import XMLEntry
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class XMLArray(MemStruct):

	__name__ = 'XMLArray'

	_import_key = 'motiongraph.compounds.XMLArray'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.xmls = Array(self.context, 0, None, (0,), XMLEntry)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('xmls', Array, (0, None, (None,), XMLEntry), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'xmls', Array, (0, None, (instance.arg,), XMLEntry), (False, None)


XMLArray.init_attributes()
