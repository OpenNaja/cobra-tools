from generated.formats.voxelskirt.compound.Material import Material


class PosInfo(Material):

	def __init__(self, arg=None, template=None):
		self.name = ''
		super().__init__(arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# -1
		self.ff = 0

		# -1, 0 for PC
		self.ff_or_zero = 0

	def read(self, stream):

		self.io_start = stream.tell()
		super().read(stream)
		self.ff = stream.read_int()
		self.ff_or_zero = stream.read_int()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		super().write(stream)
		stream.write_int(self.ff)
		stream.write_int(self.ff_or_zero)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'PosInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* ff = {self.ff.__repr__()}'
		s += f'\n	* ff_or_zero = {self.ff_or_zero.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
