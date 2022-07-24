from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import numpy
from generated.array import Array
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class Attrib(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.attrib = 0
		self.padding = 0
		self.attrib_name = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.attrib = numpy.zeros((4,), dtype=numpy.dtype('int8'))
		self.padding = 0
		self.attrib_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.attrib_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.attrib = stream.read_bytes((4,))
		instance.padding = stream.read_uint()
		instance.attrib_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.attrib_name)
		stream.write_bytes(instance.attrib)
		stream.write_uint(instance.padding)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('attrib_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('attrib', Array, ((4,), Byte, 0, None))
		yield ('padding', Uint, (0, None))

	def get_info_str(self, indent=0):
		return f'Attrib [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* attrib_name = {fmt_member(self.attrib_name, indent+1)}'
		s += f'\n	* attrib = {fmt_member(self.attrib, indent+1)}'
		s += f'\n	* padding = {fmt_member(self.padding, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
