import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint


class SoundSfxVoice(BaseStruct):

	__name__ = 'SoundSfxVoice'

	_import_path = 'generated.formats.bnk.compounds.SoundSfxVoice'

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
		instance.length = Uint.from_stream(stream, instance.context, 0, None)
		instance.id = Uint.from_stream(stream, instance.context, 0, None)
		instance.const_a = Uint.from_stream(stream, instance.context, 0, None)
		instance.const_b = Byte.from_stream(stream, instance.context, 0, None)
		instance.didx_id = Uint.from_stream(stream, instance.context, 0, None)
		instance.wem_length = Uint.from_stream(stream, instance.context, 0, None)
		instance.extra = Array.from_stream(stream, instance.context, 0, None, (instance.length - 17,), Byte)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.length)
		Uint.to_stream(stream, instance.id)
		Uint.to_stream(stream, instance.const_a)
		Byte.to_stream(stream, instance.const_b)
		Uint.to_stream(stream, instance.didx_id)
		Uint.to_stream(stream, instance.wem_length)
		Array.to_stream(stream, instance.extra, (instance.length - 17,), Byte, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'length', Uint, (0, None), (False, None)
		yield 'id', Uint, (0, None), (False, None)
		yield 'const_a', Uint, (0, None), (False, None)
		yield 'const_b', Byte, (0, None), (False, None)
		yield 'didx_id', Uint, (0, None), (False, None)
		yield 'wem_length', Uint, (0, None), (False, None)
		yield 'extra', Array, ((instance.length - 17,), Byte, 0, None), (False, None)

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

