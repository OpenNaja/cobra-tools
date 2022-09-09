from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Uint32Data(MemStruct):

	"""
	32 in log with enum
	"""

	__name__ = 'Uint32Data'

	_import_path = 'generated.formats.specdef.compounds.Uint32Data'

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
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'imin', Uint, (0, None), (False, None)
		yield 'imax', Uint, (0, None), (False, None)
		yield 'ivalue', Uint, (0, None), (False, None)
		yield 'ioptional', Uint, (0, None), (False, None)
		yield 'enum', Pointer, (0, None), (False, None)
