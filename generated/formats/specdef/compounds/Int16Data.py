from generated.formats.base.basic import Short
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Int16Data(MemStruct):

	"""
	8 bytes
	"""

	__name__ = 'Int16Data'

	_import_path = 'generated.formats.specdef.compounds.Int16Data'

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
		yield 'imin', Short, (0, None), (False, None)
		yield 'imax', Short, (0, None), (False, None)
		yield 'ivalue', Short, (0, None), (False, None)
		yield 'ioptional', Short, (0, None), (False, None)
		yield 'enum', Pointer, (0, None), (False, None)
