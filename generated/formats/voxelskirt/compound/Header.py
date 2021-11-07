from generated.formats.ovl_base.compound.GenericHeader import GenericHeader
from generated.formats.voxelskirt.compound.SizedStrData import SizedStrData


class Header(GenericHeader):

	"""
	Found at the beginning of every OVL file
	"""

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		super().__init__(context, arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# always = 0
		self.info = SizedStrData(self.context, None, None)
		self.set_defaults()

	def set_defaults(self):
		self.info = SizedStrData(self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		super().read(stream)
		self.info = stream.read_type(SizedStrData, (self.context, None, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		super().write(stream)
		stream.write_type(self.info)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Header [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* info = {self.info.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
