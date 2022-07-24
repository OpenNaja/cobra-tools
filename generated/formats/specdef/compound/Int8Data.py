from source.formats.base.basic import fmt_member
import numpy
from generated.array import Array
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Ubyte
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class Int8Data(MemStruct):

	"""
	8 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.imin = 0
		self.imax = 0
		self.ivalue = 0
		self.ioptional = 0
		self.unused = 0
		self.enum = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.imin = 0
		self.imax = 0
		self.ivalue = 0
		self.ioptional = 0
		self.unused = numpy.zeros((4,), dtype=numpy.dtype('uint8'))
		self.enum = Pointer(self.context, 0, None)

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
		instance.imin = stream.read_byte()
		instance.imax = stream.read_byte()
		instance.ivalue = stream.read_byte()
		instance.ioptional = stream.read_byte()
		instance.unused = stream.read_ubytes((4,))
		instance.enum = Pointer.from_stream(stream, instance.context, 0, None)
		instance.enum.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_byte(instance.imin)
		stream.write_byte(instance.imax)
		stream.write_byte(instance.ivalue)
		stream.write_byte(instance.ioptional)
		stream.write_ubytes(instance.unused)
		Pointer.to_stream(stream, instance.enum)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('imin', Byte, (0, None))
		yield ('imax', Byte, (0, None))
		yield ('ivalue', Byte, (0, None))
		yield ('ioptional', Byte, (0, None))
		yield ('unused', Array, ((4,), Ubyte, 0, None))
		yield ('enum', Pointer, (0, None))

	def get_info_str(self, indent=0):
		return f'Int8Data [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* imin = {fmt_member(self.imin, indent+1)}'
		s += f'\n	* imax = {fmt_member(self.imax, indent+1)}'
		s += f'\n	* ivalue = {fmt_member(self.ivalue, indent+1)}'
		s += f'\n	* ioptional = {fmt_member(self.ioptional, indent+1)}'
		s += f'\n	* unused = {fmt_member(self.unused, indent+1)}'
		s += f'\n	* enum = {fmt_member(self.enum, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
