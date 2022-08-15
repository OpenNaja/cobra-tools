import generated.formats.base.basic
import numpy
from generated.array import Array
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Info(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.flags = numpy.zeros((4,), dtype=numpy.dtype('int8'))
		self.value = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		self.padding = 0
		self.info_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.flags = numpy.zeros((4,), dtype=numpy.dtype('int8'))
		self.value = numpy.zeros((4,), dtype=numpy.dtype('float32'))
		self.padding = 0
		self.info_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.info_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.flags = stream.read_bytes((4,))
		instance.value = stream.read_floats((4,))
		instance.padding = stream.read_uint()
		if not isinstance(instance.info_name, int):
			instance.info_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.info_name)
		stream.write_bytes(instance.flags)
		stream.write_floats(instance.value)
		stream.write_uint(instance.padding)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'info_name', Pointer, (0, generated.formats.base.basic.ZString)
		yield 'flags', Array, ((4,), Byte, 0, None)
		yield 'value', Array, ((4,), Float, 0, None)
		yield 'padding', Uint, (0, None)

	def get_info_str(self, indent=0):
		return f'Info [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* info_name = {self.fmt_member(self.info_name, indent+1)}'
		s += f'\n	* flags = {self.fmt_member(self.flags, indent+1)}'
		s += f'\n	* value = {self.fmt_member(self.value, indent+1)}'
		s += f'\n	* padding = {self.fmt_member(self.padding, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
