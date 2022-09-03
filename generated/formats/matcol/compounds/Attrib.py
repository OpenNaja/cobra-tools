import generated.formats.base.basic
import numpy
from generated.array import Array
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Attrib(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.attrib = Array((0,), Byte, self.context, 0, None)
		self.padding = 0
		self.attrib_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.attrib = numpy.zeros((4,), dtype=numpy.dtype('int8'))
		self.padding = 0
		self.attrib_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.attrib_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.attrib = Array.from_stream(stream, instance.context, 0, None, (4,), Byte)
		instance.padding = Uint.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.attrib_name, int):
			instance.attrib_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.attrib_name)
		Array.to_stream(stream, instance.attrib, (4,), Byte, instance.context, 0, None)
		Uint.to_stream(stream, instance.padding)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'attrib_name', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'attrib', Array, ((4,), Byte, 0, None), (False, None)
		yield 'padding', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Attrib [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* attrib_name = {self.fmt_member(self.attrib_name, indent+1)}'
		s += f'\n	* attrib = {self.fmt_member(self.attrib, indent+1)}'
		s += f'\n	* padding = {self.fmt_member(self.padding, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
