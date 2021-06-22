class Descriptor:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index into JointInfoList
		self.parent = 0

		# index into JointInfoList
		self.child = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.parent = stream.read_ushort()
		self.child = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_ushort(self.parent)
		stream.write_ushort(self.child)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Descriptor [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* parent = {self.parent.__repr__()}'
		s += f'\n	* child = {self.child.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
