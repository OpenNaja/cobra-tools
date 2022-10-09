from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class SomeData(MemStruct):

	"""
	PC: 64 bytes
	"""

	__name__ = 'SomeData'

	_import_key = 'trackmesh.compounds.SomeData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.z_0 = 0
		self.z_1 = 0
		self.float_0 = 0.0
		self.float_1 = 0.0
		self.float_2 = 0.0
		self.float_3 = 0.0
		self.one = 0
		self.z_2 = 0
		self.z_3 = 0
		self.count = 0
		self.z_4 = 0
		self.z_5 = 0
		self.some_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'some_name', Pointer, (0, ZString), (False, None)
		yield 'z_0', Uint64, (0, None), (False, None)
		yield 'z_1', Uint64, (0, None), (False, None)
		yield 'float_0', Float, (0, None), (False, None)
		yield 'float_1', Float, (0, None), (False, None)
		yield 'float_2', Float, (0, None), (False, None)
		yield 'float_3', Float, (0, None), (False, None)
		yield 'one', Uint, (0, None), (False, None)
		yield 'z_2', Uint, (0, None), (False, None)
		yield 'z_3', Uint, (0, None), (False, None)
		yield 'count', Uint, (0, None), (False, None)
		yield 'z_4', Uint, (0, None), (False, None)
		yield 'z_5', Uint, (0, None), (False, None)
