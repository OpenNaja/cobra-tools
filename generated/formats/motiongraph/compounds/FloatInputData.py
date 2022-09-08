from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class FloatInputData(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'FloatInputData'

	_import_path = 'generated.formats.motiongraph.compounds.FloatInputData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.float = 0.0
		self.optional_var_and_curve_count = 0
		self.optional_var_and_curve = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.float = 0.0
		self.optional_var_and_curve_count = 0
		self.optional_var_and_curve = 0

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'float', Float, (0, None), (False, None)
		yield 'optional_var_and_curve_count', Uint, (0, None), (False, None)
		yield 'optional_var_and_curve', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'FloatInputData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
