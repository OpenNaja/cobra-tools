from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Uint16Data(MemStruct):

	"""
	24 bytes in log
	"""

	__name__ = 'Uint16Data'

	_import_key = 'specdef.compounds.Uint16Data'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.imin = 0
		self.imax = 0
		self.ivalue = 0
		self.ioptional = 0
		self.enum = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('imin', Ushort, (0, None), (False, None), (None, None))
		yield ('imax', Ushort, (0, None), (False, None), (None, None))
		yield ('ivalue', Ushort, (0, None), (False, None), (None, None))
		yield ('ioptional', Ushort, (0, None), (False, None), (None, None))
		yield ('enum', Pointer, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'imin', Ushort, (0, None), (False, None)
		yield 'imax', Ushort, (0, None), (False, None)
		yield 'ivalue', Ushort, (0, None), (False, None)
		yield 'ioptional', Ushort, (0, None), (False, None)
		yield 'enum', Pointer, (0, None), (False, None)


Uint16Data.init_attributes()
