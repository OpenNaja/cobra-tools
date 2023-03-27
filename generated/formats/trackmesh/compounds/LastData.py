from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class LastData(MemStruct):

	"""
	PC: 120 bytes
	"""

	__name__ = 'LastData'

	_import_key = 'trackmesh.compounds.LastData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.p_1_count = 0
		self.b = 0
		self.c = 0
		self.p_2_count = 0
		self.p_3_count = 0
		self.f = 0
		self.g = 0
		self.p_4_count = 0
		self.p_5_count = 0
		self.some_name = Pointer(self.context, 0, ZString)
		self.p_1 = Pointer(self.context, 0, None)
		self.p_2 = Pointer(self.context, 0, None)
		self.p_3 = Pointer(self.context, 0, None)
		self.p_4 = Pointer(self.context, 0, None)
		self.p_5 = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('some_name', Pointer, (0, ZString), (False, None), None)
		yield ('p_1', Pointer, (0, None), (False, None), None)
		yield ('p_1_count', Uint64, (0, None), (False, None), None)
		yield ('b', Uint64, (0, None), (False, None), None)
		yield ('c', Uint64, (0, None), (False, None), None)
		yield ('p_2', Pointer, (0, None), (False, None), None)
		yield ('p_2_count', Uint64, (0, None), (False, None), None)
		yield ('p_3', Pointer, (0, None), (False, None), None)
		yield ('p_3_count', Uint64, (0, None), (False, None), None)
		yield ('f', Uint64, (0, None), (False, None), None)
		yield ('g', Uint64, (0, None), (False, None), None)
		yield ('p_4', Pointer, (0, None), (False, None), None)
		yield ('p_4_count', Uint64, (0, None), (False, None), None)
		yield ('p_5', Pointer, (0, None), (False, None), None)
		yield ('p_5_count', Uint64, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'some_name', Pointer, (0, ZString), (False, None)
		yield 'p_1', Pointer, (0, None), (False, None)
		yield 'p_1_count', Uint64, (0, None), (False, None)
		yield 'b', Uint64, (0, None), (False, None)
		yield 'c', Uint64, (0, None), (False, None)
		yield 'p_2', Pointer, (0, None), (False, None)
		yield 'p_2_count', Uint64, (0, None), (False, None)
		yield 'p_3', Pointer, (0, None), (False, None)
		yield 'p_3_count', Uint64, (0, None), (False, None)
		yield 'f', Uint64, (0, None), (False, None)
		yield 'g', Uint64, (0, None), (False, None)
		yield 'p_4', Pointer, (0, None), (False, None)
		yield 'p_4_count', Uint64, (0, None), (False, None)
		yield 'p_5', Pointer, (0, None), (False, None)
		yield 'p_5_count', Uint64, (0, None), (False, None)


LastData.init_attributes()
