from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Float
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class Key(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.time = 0
		self.value = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.time = 0.0
		self.value = 0.0

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
		instance.time = stream.read_float()
		instance.value = stream.read_float()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_float(instance.time)
		stream.write_float(instance.value)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('time', Float, (0, None))
		yield ('value', Float, (0, None))

	def get_info_str(self, indent=0):
		return f'Key [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* time = {fmt_member(self.time, indent+1)}'
		s += f'\n	* value = {fmt_member(self.value, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
