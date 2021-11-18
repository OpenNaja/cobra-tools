from generated.array import Array
from generated.context import ContextReference
from generated.formats.matcol.compound.Layer import Layer
from generated.formats.matcol.compound.MaterialInfo import MaterialInfo


class LayeredWrapper:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.info = MaterialInfo(self.context, None, None)
		self.layers = Array(self.context)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.info = MaterialInfo(self.context, None, None)
		self.layers = Array(self.context)

	def read(self, stream):
		self.io_start = stream.tell()
		self.info = stream.read_type(MaterialInfo, (self.context, None, None))
		self.layers.read(stream, Layer, self.info.material_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.info)
		self.layers.write(stream, Layer, self.info.material_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'LayeredWrapper [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* info = {self.info.__repr__()}'
		s += f'\n	* layers = {self.layers.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
