import generated.formats.base.basic
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class AxisValue(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_0 = 0
		self.u_1 = 0
		self.u_2 = 0
		self.u_3 = 0
		self.u_4 = 0
		self.axis_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.value_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.u_0 = 0
		self.u_1 = 0
		self.u_2 = 0
		self.u_3 = 0
		self.u_4 = 0
		self.axis_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.value_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.axis_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.u_0 = stream.read_uint64()
		instance.u_1 = stream.read_uint64()
		instance.u_2 = stream.read_uint64()
		instance.value_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.u_3 = stream.read_uint64()
		instance.u_4 = stream.read_uint64()
		if not isinstance(instance.axis_name, int):
			instance.axis_name.arg = 0
		if not isinstance(instance.value_name, int):
			instance.value_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.axis_name)
		stream.write_uint64(instance.u_0)
		stream.write_uint64(instance.u_1)
		stream.write_uint64(instance.u_2)
		Pointer.to_stream(stream, instance.value_name)
		stream.write_uint64(instance.u_3)
		stream.write_uint64(instance.u_4)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'axis_name', Pointer, (0, generated.formats.base.basic.ZString)
		yield 'u_0', Uint64, (0, None)
		yield 'u_1', Uint64, (0, None)
		yield 'u_2', Uint64, (0, None)
		yield 'value_name', Pointer, (0, generated.formats.base.basic.ZString)
		yield 'u_3', Uint64, (0, None)
		yield 'u_4', Uint64, (0, None)

	def get_info_str(self, indent=0):
		return f'AxisValue [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* axis_name = {self.fmt_member(self.axis_name, indent+1)}'
		s += f'\n	* u_0 = {self.fmt_member(self.u_0, indent+1)}'
		s += f'\n	* u_1 = {self.fmt_member(self.u_1, indent+1)}'
		s += f'\n	* u_2 = {self.fmt_member(self.u_2, indent+1)}'
		s += f'\n	* value_name = {self.fmt_member(self.value_name, indent+1)}'
		s += f'\n	* u_3 = {self.fmt_member(self.u_3, indent+1)}'
		s += f'\n	* u_4 = {self.fmt_member(self.u_4, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
