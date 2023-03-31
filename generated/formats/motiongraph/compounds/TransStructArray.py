from generated.array import Array
from generated.formats.motiongraph.compounds.TransStruct import TransStruct
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class TransStructArray(MemStruct):

	__name__ = 'TransStructArray'

	_import_key = 'motiongraph.compounds.TransStructArray'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.array = Array(self.context, 0, None, (0,), TransStruct)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('array', Array, (0, None, (None,), TransStruct), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'array', Array, (0, None, (instance.arg,), TransStruct), (False, None)


TransStructArray.init_attributes()
