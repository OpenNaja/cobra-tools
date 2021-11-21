from generated.array import Array
from generated.context import ContextReference
from generated.formats.matcol.compound.Layer import Layer
from generated.formats.matcol.compound.MaterialInfo import MaterialInfo


class LayeredWrapper:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.info = MaterialInfo(self.context, 0, None)
		self.layers = Array((self.info.material_count,), Layer, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.info = MaterialInfo(self.context, 0, None)
		self.layers = Array((self.info.material_count,), Layer, self.context, 0, None)

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
		instance.info = MaterialInfo.from_stream(stream, instance.context, 0, None)
		instance.layers = Array.from_stream(stream, (instance.info.material_count,), Layer, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		MaterialInfo.to_stream(stream, instance.info)
		Array.to_stream(stream, instance.layers, (instance.info.material_count,),Layer, instance.context, 0, None)

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
