from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class FloatData(MemStruct):

	"""
	16 bytes in log
	"""

	__name__ = 'FloatData'

	_import_path = 'generated.formats.specdef.compounds.FloatData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.imin = 0.0
		self.imax = 0.0
		self.ivalue = 0.0
		self.ioptional = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.imin = 0.0
		self.imax = 0.0
		self.ivalue = 0.0
		self.ioptional = 0

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'imin', Float, (0, None), (False, None)
		yield 'imax', Float, (0, None), (False, None)
		yield 'ivalue', Float, (0, None), (False, None)
		yield 'ioptional', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'FloatData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
