import numpy
from generated.array import Array
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Attrib(MemStruct):

	__name__ = 'Attrib'

	_import_key = 'matcol.compounds.Attrib'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.attrib = Array(self.context, 0, None, (0,), Byte)
		self.padding = 0
		self.attrib_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'attrib_name', Pointer, (0, ZString), (False, None)
		yield 'attrib', Array, (0, None, (4,), Byte), (False, None)
		yield 'padding', Uint, (0, None), (False, None)
