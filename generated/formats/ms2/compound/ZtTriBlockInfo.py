from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Short
from generated.formats.base.basic import Uint
from generated.struct import StructBase


class ZtTriBlockInfo(StructBase):

	"""
	8 bytes total
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.tri_index_count = 0
		self.a = 0
		self.unk_index = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.tri_index_count = 0
		self.a = 0
		self.unk_index = 0

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
		instance.tri_index_count = stream.read_uint()
		instance.a = stream.read_short()
		instance.unk_index = stream.read_short()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.tri_index_count)
		stream.write_short(instance.a)
		stream.write_short(instance.unk_index)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('tri_index_count', Uint, (0, None))
		yield ('a', Short, (0, None))
		yield ('unk_index', Short, (0, None))

	def get_info_str(self, indent=0):
		return f'ZtTriBlockInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* tri_index_count = {fmt_member(self.tri_index_count, indent+1)}'
		s += f'\n	* a = {fmt_member(self.a, indent+1)}'
		s += f'\n	* unk_index = {fmt_member(self.unk_index, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
