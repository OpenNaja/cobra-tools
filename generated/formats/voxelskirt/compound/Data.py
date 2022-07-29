from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Uint64
from generated.struct import StructBase


class Data(StructBase):

	"""
	PZ and JWE only, describes a data layer image
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)

		# index into name list
		self.id = 0

		# 0 = ubyte, 2 = float
		self.type = 0

		# address of this data layer
		self.offset = 0

		# data size of this layer, in bytes
		self.dsize = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.id = 0
		self.type = 0
		self.offset = 0
		self.dsize = 0

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
		instance.id = stream.read_uint64()
		instance.type = stream.read_uint64()
		instance.offset = stream.read_uint64()
		instance.dsize = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.id)
		stream.write_uint64(instance.type)
		stream.write_uint64(instance.offset)
		stream.write_uint64(instance.dsize)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('id', Uint64, (0, None))
		yield ('type', Uint64, (0, None))
		yield ('offset', Uint64, (0, None))
		yield ('dsize', Uint64, (0, None))

	def get_info_str(self, indent=0):
		return f'Data [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* id = {fmt_member(self.id, indent+1)}'
		s += f'\n	* type = {fmt_member(self.type, indent+1)}'
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* dsize = {fmt_member(self.dsize, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
