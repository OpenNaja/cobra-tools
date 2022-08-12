from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Int
from generated.struct import StructBase


class BufferPresence(StructBase):

	"""
	in DLA and JWE2, this can be a dependency to a model2stream
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# -1 for a static buffer, 0 for streamed buffer; may be stream index
		self.pool_index = 0
		self.data_offset = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.pool_index = 0
		self.data_offset = 0

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
		instance.pool_index = stream.read_int()
		instance.data_offset = stream.read_int()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_int(instance.pool_index)
		stream.write_int(instance.data_offset)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('pool_index', Int, (0, None))
		yield ('data_offset', Int, (0, None))

	def get_info_str(self, indent=0):
		return f'BufferPresence [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* pool_index = {fmt_member(self.pool_index, indent+1)}'
		s += f'\n	* data_offset = {fmt_member(self.data_offset, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
