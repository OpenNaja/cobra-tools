import typing
from generated.formats.matcol.compound.Layer import Layer
from generated.formats.matcol.compound.MaterialInfo import MaterialInfo


class LayeredWrapper:
	info: MaterialInfo
	layers: typing.List[Layer]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.info = MaterialInfo()
		self.layers = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.info = stream.read_type(MaterialInfo)
		self.layers = [stream.read_type(Layer) for _ in range(self.info.material_count)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.info)
		for item in self.layers: stream.write_type(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'LayeredWrapper [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* info = ' + self.info.__repr__()
		s += '\n	* layers = ' + self.layers.__repr__()
		s += '\n'
		return s
