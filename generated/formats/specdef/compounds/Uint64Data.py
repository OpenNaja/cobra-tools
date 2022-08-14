from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Uint64Data(MemStruct):

	"""
	48 bytes in log
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.imin = 0
		self.imax = 0
		self.ivalue = 0
		self.ioptional = 0
		self.enum = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.imin = 0
		self.imax = 0
		self.ivalue = 0
		self.ioptional = 0
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
		instance.imin = stream.read_uint64()
		instance.imax = stream.read_uint64()
		instance.ivalue = stream.read_uint64()
		instance.ioptional = stream.read_uint64()
		instance.enum = Pointer.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.enum, int):
			instance.enum.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.imin)
		stream.write_uint64(instance.imax)
		stream.write_uint64(instance.ivalue)
		stream.write_uint64(instance.ioptional)
		Pointer.to_stream(stream, instance.enum)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'imin', Uint64, (0, None)
		yield 'imax', Uint64, (0, None)
		yield 'ivalue', Uint64, (0, None)
		yield 'ioptional', Uint64, (0, None)
		yield 'enum', Pointer, (0, None)

	def get_info_str(self, indent=0):
		return f'Uint64Data [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* imin = {self.fmt_member(self.imin, indent+1)}'
		s += f'\n	* imax = {self.fmt_member(self.imax, indent+1)}'
		s += f'\n	* ivalue = {self.fmt_member(self.ivalue, indent+1)}'
		s += f'\n	* ioptional = {self.fmt_member(self.ioptional, indent+1)}'
		s += f'\n	* enum = {self.fmt_member(self.enum, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
