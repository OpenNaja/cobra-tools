from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Sixtyfour(MemStruct):

	"""
	64 bytes
	"""

	__name__ = 'Sixtyfour'

	_import_key = 'motiongraph.compounds.Sixtyfour'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.count_3 = 0
		self.ptr_0 = Pointer(self.context, 0, None)
		self.ptr_1 = Pointer(self.context, 0, None)
		self.ptr_2 = Pointer(self.context, 0, None)
		self.ptr_3 = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('count_0', Uint64, (0, None), (False, None), None),
		('ptr_0', Pointer, (0, None), (False, None), None),
		('ptr_1', Pointer, (0, None), (False, None), None),
		('count_1', Uint64, (0, None), (False, None), None),
		('count_2', Uint64, (0, None), (False, None), None),
		('ptr_2', Pointer, (0, None), (False, None), None),
		('ptr_3', Pointer, (0, None), (False, None), None),
		('count_3', Uint64, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'count_0', Uint64, (0, None), (False, None)
		yield 'ptr_0', Pointer, (0, None), (False, None)
		yield 'ptr_1', Pointer, (0, None), (False, None)
		yield 'count_1', Uint64, (0, None), (False, None)
		yield 'count_2', Uint64, (0, None), (False, None)
		yield 'ptr_2', Pointer, (0, None), (False, None)
		yield 'ptr_3', Pointer, (0, None), (False, None)
		yield 'count_3', Uint64, (0, None), (False, None)
