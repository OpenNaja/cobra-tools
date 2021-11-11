import numpy
from generated.array import Array
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

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 'FGM '
		self.magic = numpy.zeros((4), dtype='byte')
		self.version = 0
		self.user_version = 0

		# bool
		self.has_texture_list = 0
		self.root_0 = Root0(self.context, None, None)
		self.root_1 = Root1(self.context, None, None)
		self.root_1_pad = Root1Pad(self.context, None, None)
		self.texture_wrapper = TextureWrapper(self.context, None, None)
		self.variant_wrapper = VariantWrapper(self.context, None, None)
		self.layered_wrapper = LayeredWrapper(self.context, None, None)
		self.set_defaults()

	def set_defaults(self):
		self.magic = numpy.zeros((4), dtype='byte')
		self.version = 0
		self.user_version = 0
		self.has_texture_list = 0
		self.root_0 = Root0(self.context, None, None)
		self.root_1 = Root1(self.context, None, None)
		if self.has_texture_list == 0:
			self.root_1_pad = Root1Pad(self.context, None, None)
		if self.has_texture_list == 1:
			self.texture_wrapper = TextureWrapper(self.context, None, None)
		if self.root_1.flag == 3:
			self.variant_wrapper = VariantWrapper(self.context, None, None)
		if self.root_1.flag == 2:
			self.layered_wrapper = LayeredWrapper(self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.magic = stream.read_bytes((4))
		self.version = stream.read_uint()
		self.context.version = self.version
		self.user_version = stream.read_uint()
		self.context.user_version = self.user_version
		self.has_texture_list = stream.read_ubyte()
		self.root_0 = stream.read_type(Root0, (self.context, None, None))
		self.root_1 = stream.read_type(Root1, (self.context, None, None))
		if self.has_texture_list == 0:
			self.root_1_pad = stream.read_type(Root1Pad, (self.context, None, None))
		if self.has_texture_list == 1:
			self.texture_wrapper = stream.read_type(TextureWrapper, (self.context, None, None))
		if self.root_1.flag == 3:
			self.variant_wrapper = stream.read_type(VariantWrapper, (self.context, None, None))
		if self.root_1.flag == 2:
			self.layered_wrapper = stream.read_type(LayeredWrapper, (self.context, None, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_bytes(self.magic)
		stream.write_uint(self.version)
		stream.write_uint(self.user_version)
		stream.write_ubyte(self.has_texture_list)
		stream.write_type(self.root_0)
		stream.write_type(self.root_1)
		if self.has_texture_list == 0:
			stream.write_type(self.root_1_pad)
		if self.has_texture_list == 1:
			stream.write_type(self.texture_wrapper)
		if self.root_1.flag == 3:
			stream.write_type(self.variant_wrapper)
		if self.root_1.flag == 2:
			stream.write_type(self.layered_wrapper)

		self.io_size = stream.tell() - self.io_start

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
