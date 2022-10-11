from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class NextData(MemStruct):

	"""
	PC: 48 bytes
	"""

	__name__ = 'NextData'

	_import_key = 'trackmesh.compounds.NextData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = 0
		self.b = 0
		self.c = 0
		self.d = 0
		self.name_0 = Pointer(self.context, 0, ZString)
		self.name_1 = Pointer(self.context, 0, ZString)
		self.name_2 = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('name_0', Pointer, (0, ZString), (False, None), None),
		('name_1', Pointer, (0, ZString), (False, None), None),
		('a', Uint, (0, None), (False, None), None),
		('b', Uint, (0, None), (False, None), None),
		('c', Uint64, (0, None), (False, None), None),
		('name_2', Pointer, (0, ZString), (False, None), None),
		('d', Uint64, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'name_0', Pointer, (0, ZString), (False, None)
		yield 'name_1', Pointer, (0, ZString), (False, None)
		yield 'a', Uint, (0, None), (False, None)
		yield 'b', Uint, (0, None), (False, None)
		yield 'c', Uint64, (0, None), (False, None)
		yield 'name_2', Pointer, (0, ZString), (False, None)
		yield 'd', Uint64, (0, None), (False, None)
