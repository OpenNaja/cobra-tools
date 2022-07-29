from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class Pair(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.value_0 = 0
		self.value_1 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.value_0 = 0
		self.value_1 = 0.0

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
		instance.value_0 = stream.read_uint()
		instance.value_1 = stream.read_float()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.value_0)
		stream.write_float(instance.value_1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('value_0', Uint, (0, None))
		yield ('value_1', Float, (0, None))

	def get_info_str(self, indent=0):
		return f'Pair [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* value_0 = {fmt_member(self.value_0, indent+1)}'
		s += f'\n	* value_1 = {fmt_member(self.value_1, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
