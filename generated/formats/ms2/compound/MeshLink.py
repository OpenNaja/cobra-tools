from generated.context import ContextReference


class MeshLink:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index into material name array
		self.material_index = 0

		# index into models array
		self.model_index = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.material_index = stream.read_ushort()
		self.model_index = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_ushort(self.material_index)
		stream.write_ushort(self.model_index)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'MeshLink [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* material_index = {self.material_index.__repr__()}'
		s += f'\n	* model_index = {self.model_index.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
