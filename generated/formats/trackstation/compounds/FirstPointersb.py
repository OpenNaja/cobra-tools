from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.trackstation.compounds.CommonChunk import CommonChunk


class FirstPointersb(MemStruct):

	"""
	PZ and PC: 112 bytes
	"""

	__name__ = 'FirstPointersb'

	_import_key = 'trackstation.compounds.FirstPointersb'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.pointer_stuff = CommonChunk(self.context, 0, None)
		self.zero = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('pointer_stuff', CommonChunk, (0, None), (False, None), None)
		yield ('zero', Uint64, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'pointer_stuff', CommonChunk, (0, None), (False, None)
		yield 'zero', Uint64, (0, None), (False, None)


FirstPointersb.init_attributes()
