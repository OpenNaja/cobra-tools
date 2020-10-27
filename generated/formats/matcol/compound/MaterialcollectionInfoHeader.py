import typing
from generated.array import Array
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

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 'FGM '
		self.magic = Array()
		self.version = 0
		self.flag_2 = 0

		# bool
		self.has_texture_list = 0
		self.root_0 = Root0()
		self.root_1 = Root1()
		self.root_1_pad = Root1Pad()
		self.texture_wrapper = TextureWrapper()
		self.variant_wrapper = VariantWrapper()
		self.layered_wrapper = LayeredWrapper()

	def read(self, stream):

		self.io_start = stream.tell()
		self.magic.read(stream, 'Byte', 4, None)
		self.version = stream.read_uint()
		stream.version = self.version
		self.flag_2 = stream.read_uint()
		self.has_texture_list = stream.read_ubyte()
		self.root_0 = stream.read_type(Root0)
		self.root_1 = stream.read_type(Root1)
		if self.has_texture_list == 0:
			self.root_1_pad = stream.read_type(Root1Pad)
		if self.has_texture_list == 1:
			self.texture_wrapper = stream.read_type(TextureWrapper)
		if self.root_1.flag == 3:
			self.variant_wrapper = stream.read_type(VariantWrapper)
		if self.root_1.flag == 2:
			self.layered_wrapper = stream.read_type(LayeredWrapper)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		self.magic.write(stream, 'Byte', 4, None)
		stream.write_uint(self.version)
		stream.version = self.version
		stream.write_uint(self.flag_2)
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

	def __repr__(self):
		s = 'MaterialcollectionInfoHeader [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* magic = ' + self.magic.__repr__()
		s += '\n	* version = ' + self.version.__repr__()
		s += '\n	* flag_2 = ' + self.flag_2.__repr__()
		s += '\n	* has_texture_list = ' + self.has_texture_list.__repr__()
		s += '\n	* root_0 = ' + self.root_0.__repr__()
		s += '\n	* root_1 = ' + self.root_1.__repr__()
		s += '\n	* root_1_pad = ' + self.root_1_pad.__repr__()
		s += '\n	* texture_wrapper = ' + self.texture_wrapper.__repr__()
		s += '\n	* variant_wrapper = ' + self.variant_wrapper.__repr__()
		s += '\n	* layered_wrapper = ' + self.layered_wrapper.__repr__()
		s += '\n'
		return s
