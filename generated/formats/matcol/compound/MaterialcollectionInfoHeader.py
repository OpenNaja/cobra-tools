import numpy
from generated.context import ContextReference
from generated.formats.matcol.compound.LayeredWrapper import LayeredWrapper
from generated.formats.matcol.compound.Root0 import Root0
from generated.formats.matcol.compound.Root1 import Root1
from generated.formats.matcol.compound.Root1Pad import Root1Pad
from generated.formats.matcol.compound.TextureWrapper import TextureWrapper
from generated.formats.matcol.compound.VariantWrapper import VariantWrapper


class MaterialcollectionInfoHeader:

	"""
	Custom header struct
	
	This reads a whole custom Matcol file
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 'FGM '
		self.magic = numpy.zeros((4,), dtype=numpy.dtype('int8'))
		self.version = 0
		self.user_version = 0

		# bool
		self.has_texture_list = 0
		self.root_0 = Root0(self.context, 0, None)
		self.root_1 = Root1(self.context, 0, None)
		self.root_1_pad = Root1Pad(self.context, 0, None)
		self.texture_wrapper = TextureWrapper(self.context, 0, None)
		self.variant_wrapper = VariantWrapper(self.context, 0, None)
		self.layered_wrapper = LayeredWrapper(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.magic = numpy.zeros((4,), dtype=numpy.dtype('int8'))
		self.version = 0
		self.user_version = 0
		self.has_texture_list = 0
		self.root_0 = Root0(self.context, 0, None)
		self.root_1 = Root1(self.context, 0, None)
		if self.has_texture_list == 0:
			self.root_1_pad = Root1Pad(self.context, 0, None)
		if self.has_texture_list == 1:
			self.texture_wrapper = TextureWrapper(self.context, 0, None)
		if self.root_1.flag == 3:
			self.variant_wrapper = VariantWrapper(self.context, 0, None)
		if self.root_1.flag == 2:
			self.layered_wrapper = LayeredWrapper(self.context, 0, None)

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
		instance.magic = stream.read_bytes((4,))
		instance.version = stream.read_uint()
		instance.context.version = instance.version
		instance.user_version = stream.read_uint()
		instance.context.user_version = instance.user_version
		instance.has_texture_list = stream.read_ubyte()
		instance.root_0 = Root0.from_stream(stream, instance.context, 0, None)
		instance.root_1 = Root1.from_stream(stream, instance.context, 0, None)
		if instance.has_texture_list == 0:
			instance.root_1_pad = Root1Pad.from_stream(stream, instance.context, 0, None)
		if instance.has_texture_list == 1:
			instance.texture_wrapper = TextureWrapper.from_stream(stream, instance.context, 0, None)
		if instance.root_1.flag == 3:
			instance.variant_wrapper = VariantWrapper.from_stream(stream, instance.context, 0, None)
		if instance.root_1.flag == 2:
			instance.layered_wrapper = LayeredWrapper.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_bytes(instance.magic)
		stream.write_uint(instance.version)
		stream.write_uint(instance.user_version)
		stream.write_ubyte(instance.has_texture_list)
		Root0.to_stream(stream, instance.root_0)
		Root1.to_stream(stream, instance.root_1)
		if instance.has_texture_list == 0:
			Root1Pad.to_stream(stream, instance.root_1_pad)
		if instance.has_texture_list == 1:
			TextureWrapper.to_stream(stream, instance.texture_wrapper)
		if instance.root_1.flag == 3:
			VariantWrapper.to_stream(stream, instance.variant_wrapper)
		if instance.root_1.flag == 2:
			LayeredWrapper.to_stream(stream, instance.layered_wrapper)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self):
		return f'MaterialcollectionInfoHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* magic = {self.magic.__repr__()}'
		s += f'\n	* version = {self.version.__repr__()}'
		s += f'\n	* user_version = {self.user_version.__repr__()}'
		s += f'\n	* has_texture_list = {self.has_texture_list.__repr__()}'
		s += f'\n	* root_0 = {self.root_0.__repr__()}'
		s += f'\n	* root_1 = {self.root_1.__repr__()}'
		s += f'\n	* root_1_pad = {self.root_1_pad.__repr__()}'
		s += f'\n	* texture_wrapper = {self.texture_wrapper.__repr__()}'
		s += f'\n	* variant_wrapper = {self.variant_wrapper.__repr__()}'
		s += f'\n	* layered_wrapper = {self.layered_wrapper.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
