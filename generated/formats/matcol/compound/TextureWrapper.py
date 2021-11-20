from generated.array import Array
from generated.context import ContextReference
from generated.formats.matcol.compound.Texture import Texture
from generated.formats.matcol.compound.TextureInfo import TextureInfo


class TextureWrapper:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.info = TextureInfo(self.context, None, None)
		self.textures = Array((self.info.texture_count), Texture, self.context, None, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.info = TextureInfo(self.context, None, None)
		self.textures = Array((self.info.texture_count), Texture, self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.info = stream.read_type(TextureInfo, (self.context, None, None))
		self.textures.read(stream, Texture, self.info.texture_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.info)
		self.textures.write(stream, Texture, self.info.texture_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'TextureWrapper [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* info = {self.info.__repr__()}'
		s += f'\n	* textures = {self.textures.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
