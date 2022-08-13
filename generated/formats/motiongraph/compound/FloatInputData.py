from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class FloatInputData(MemStruct):

	"""
	16 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.float = 0
		self.optional_var_and_curve_count = 0
		self.optional_var_and_curve = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.float = 0.0
		self.optional_var_and_curve_count = 0
		self.optional_var_and_curve = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.float = stream.read_float()
		instance.optional_var_and_curve_count = stream.read_uint()
		instance.optional_var_and_curve = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_float(instance.float)
		stream.write_uint(instance.optional_var_and_curve_count)
		stream.write_uint64(instance.optional_var_and_curve)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('float', Float, (0, None))
		yield ('optional_var_and_curve_count', Uint, (0, None))
		yield ('optional_var_and_curve', Uint64, (0, None))

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
