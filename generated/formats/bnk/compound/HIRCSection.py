from generated.formats.base.basic import fmt_member
from generated.array import Array
from generated.formats.base.basic import Uint
from generated.formats.bnk.compound.HircPointer import HircPointer
from generated.struct import StructBase


class HIRCSection(StructBase):

	"""
	The HIRC section contains all the Wwise objects, including the events, the containers to group sounds, and the references to the sound files.
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# length of following data
		self.length = 0
		self.count = 0
		self.hirc_pointers = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.length = 0
		self.count = 0
		self.hirc_pointers = Array((self.count,), HircPointer, self.context, 0, None)

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
		instance.length = stream.read_uint()
		instance.count = stream.read_uint()
		instance.hirc_pointers = Array.from_stream(stream, (instance.count,), HircPointer, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.length)
		stream.write_uint(instance.count)
		Array.to_stream(stream, instance.hirc_pointers, (instance.count,), HircPointer, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('length', Uint, (0, None))
		yield ('count', Uint, (0, None))
		yield ('hirc_pointers', Array, ((instance.count,), HircPointer, 0, None))

	def get_info_str(self, indent=0):
		return f'HIRCSection [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* length = {fmt_member(self.length, indent+1)}'
		s += f'\n	* count = {fmt_member(self.count, indent+1)}'
		s += f'\n	* hirc_pointers = {fmt_member(self.hirc_pointers, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
