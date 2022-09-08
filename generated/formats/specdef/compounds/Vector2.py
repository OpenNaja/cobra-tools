from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Vector2(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'Vector2'

	_import_path = 'generated.formats.specdef.compounds.Vector2'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.x = 0.0
		self.y = 0.0
		self.ioptional = 0
		self.unused = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.x = 0.0
		self.y = 0.0
		self.ioptional = 0
		self.unused = 0

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'x', Float, (0, None), (False, None)
		yield 'y', Float, (0, None), (False, None)
		yield 'ioptional', Uint, (0, None), (False, None)
		yield 'unused', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Vector2 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
