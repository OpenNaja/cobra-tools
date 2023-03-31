import numpy
from generated.array import Array
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Ubyte
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Int8Data(MemStruct):

	"""
	8 bytes
	"""

	__name__ = 'Int8Data'

	_import_key = 'specdef.compounds.Int8Data'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.imin = 0
		self.imax = 0
		self.ivalue = 0
		self.ioptional = 0
		self.unused = Array(self.context, 0, None, (0,), Ubyte)
		self.enum = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('imin', Byte, (0, None), (False, None), None)
		yield ('imax', Byte, (0, None), (False, None), None)
		yield ('ivalue', Byte, (0, None), (False, None), None)
		yield ('ioptional', Byte, (0, None), (False, None), None)
		yield ('unused', Array, (0, None, (4,), Ubyte), (False, None), None)
		yield ('enum', Pointer, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'imin', Byte, (0, None), (False, None)
		yield 'imax', Byte, (0, None), (False, None)
		yield 'ivalue', Byte, (0, None), (False, None)
		yield 'ioptional', Byte, (0, None), (False, None)
		yield 'unused', Array, (0, None, (4,), Ubyte), (False, None)
		yield 'enum', Pointer, (0, None), (False, None)


Int8Data.init_attributes()
