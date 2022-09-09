import numpy
from generated.array import Array
from generated.formats.base.basic import Ubyte
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Uint8Data(MemStruct):

	"""
	24 bytes in log
	"""

	__name__ = 'Uint8Data'

	_import_key = 'specdef.compounds.Uint8Data'

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
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'imin', Ubyte, (0, None), (False, None)
		yield 'imax', Ubyte, (0, None), (False, None)
		yield 'ivalue', Ubyte, (0, None), (False, None)
		yield 'ioptional', Ubyte, (0, None), (False, None)
		yield 'unused', Array, (0, None, (4,), Ubyte), (False, None)
		yield 'enum', Pointer, (0, None), (False, None)
