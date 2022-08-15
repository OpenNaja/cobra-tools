import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint


class SoundSfxVoice(BaseStruct):

	def set_defaults(self):
		super().set_defaults()
		self.length = 0
		self.id = 0
		self.const_a = 0
		self.const_b = 0
		self.didx_id = 0
		self.wem_length = 0
		self.extra = numpy.zeros((self.length - 17,), dtype=numpy.dtype('int8'))

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.length = stream.read_uint()
		instance.id = stream.read_uint()
		instance.const_a = stream.read_uint()
		instance.const_b = stream.read_byte()
		instance.didx_id = stream.read_uint()
		instance.wem_length = stream.read_uint()
		instance.extra = stream.read_bytes((instance.length - 17,))

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.length)
		stream.write_uint(instance.id)
		stream.write_uint(instance.const_a)
		stream.write_byte(instance.const_b)
		stream.write_uint(instance.didx_id)
		stream.write_uint(instance.wem_length)
		stream.write_bytes(instance.extra)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'length', Uint, (0, None)
		yield 'id', Uint, (0, None)
		yield 'const_a', Uint, (0, None)
		yield 'const_b', Byte, (0, None)
		yield 'didx_id', Uint, (0, None)
		yield 'wem_length', Uint, (0, None)
		yield 'extra', Array, ((instance.length - 17,), Byte, 0, None)

	def get_info_str(self, indent=0):
		return f'SoundSfxVoice [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* length = {self.fmt_member(self.length, indent+1)}'
		s += f'\n	* id = {self.fmt_member(self.id, indent+1)}'
		s += f'\n	* const_a = {self.fmt_member(self.const_a, indent+1)}'
		s += f'\n	* const_b = {self.fmt_member(self.const_b, indent+1)}'
		s += f'\n	* didx_id = {self.fmt_member(self.didx_id, indent+1)}'
		s += f'\n	* wem_length = {self.fmt_member(self.wem_length, indent+1)}'
		s += f'\n	* extra = {self.fmt_member(self.extra, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

	def __init__(self, context, arg=0, template=None, set_default=True):
		self._context = context
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of this section
		self.length = 0

		# id of this Sound SFX object
		self.sfx_id = 0

		# ?
		self.const_a = 0

		# ?
		self.const_b = 0

		# ?
		self.didx_id = 0

		# ?
		self.wem_length = 0

		# include this here so that numpy doesn't choke
		# self.extra = numpy.zeros((self.length - 17), dtype='byte')

