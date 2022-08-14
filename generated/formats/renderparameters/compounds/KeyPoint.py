from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class KeyPoint(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.time = 0.0
		self.value = 0.0
		self.tangent_before = 0.0
		self.tangent_after = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.time = 0.0
		self.value = 0.0
		self.tangent_before = 0.0
		self.tangent_after = 0.0

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
		instance.tangent_before = stream.read_float()
		instance.tangent_after = stream.read_float()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_float(instance.time)
		stream.write_float(instance.value)
		stream.write_float(instance.tangent_before)
		stream.write_float(instance.tangent_after)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield 'time', Float, (0, None)
		yield 'value', Float, (0, None)
		yield 'tangent_before', Float, (0, None)
		yield 'tangent_after', Float, (0, None)

	def get_info_str(self, indent=0):
		return f'KeyPoint [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* time = {self.fmt_member(self.time, indent+1)}'
		s += f'\n	* value = {self.fmt_member(self.value, indent+1)}'
		s += f'\n	* tangent_before = {self.fmt_member(self.tangent_before, indent+1)}'
		s += f'\n	* tangent_after = {self.fmt_member(self.tangent_after, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
