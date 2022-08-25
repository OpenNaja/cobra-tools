from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class FloatInputData(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'FloatInputData'

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
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.float = Float.from_stream(stream, instance.context, 0, None)
		instance.optional_var_and_curve_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.optional_var_and_curve = Uint64.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Float.to_stream(stream, instance.float)
		Uint.to_stream(stream, instance.optional_var_and_curve_count)
		Uint64.to_stream(stream, instance.optional_var_and_curve)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'float', Float, (0, None), (False, None)
		yield 'optional_var_and_curve_count', Uint, (0, None), (False, None)
		yield 'optional_var_and_curve', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'FloatInputData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* float = {self.fmt_member(self.float, indent+1)}'
		s += f'\n	* optional_var_and_curve_count = {self.fmt_member(self.optional_var_and_curve_count, indent+1)}'
		s += f'\n	* optional_var_and_curve = {self.fmt_member(self.optional_var_and_curve, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
