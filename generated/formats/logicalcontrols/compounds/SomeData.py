from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class SomeData(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'SomeData'

	_import_path = 'generated.formats.logicalcontrols.compounds.SomeData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.key = 0
		self.extra = 0
		self.a = 0.0
		self.b = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'key', Uint, (0, None), (False, None)
		yield 'extra', Uint, (0, None), (False, None)
		yield 'a', Float, (0, None), (False, None)
		yield 'b', Float, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'SomeData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
