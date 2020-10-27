import typing
from generated.array import Array
from generated.formats.matcol.compound.Texture import Texture
from generated.formats.matcol.compound.TextureInfo import TextureInfo


class TextureWrapper:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.info = TextureInfo()
		self.textures = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.info = stream.read_type(TextureInfo)
		self.textures.read(stream, Texture, self.info.texture_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.info)
		self.textures.write(stream, Texture, self.info.texture_count, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'TextureWrapper [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* info = ' + self.info.__repr__()
		s += '\n	* textures = ' + self.textures.__repr__()
		s += '\n'
		return s
