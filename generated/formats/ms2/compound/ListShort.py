from generated.formats.ms2.compound.Descriptor import Descriptor
from generated.formats.ms2.compound.Vector3 import Vector3


class ListShort(Descriptor):

	"""
	used in JWE dinos
	"""

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# location of the joint
		self.loc = Vector3(self.context, None, None)

		# normalized
		self.direction = Vector3(self.context, None, None)

		# min, le 0
		self.min = 0

		# max, ge 0
		self.max = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.loc = Vector3(self.context, None, None)
		self.direction = Vector3(self.context, None, None)
		self.min = 0
		self.max = 0

	def read(self, stream):
		super().read(stream)
		self.loc = stream.read_type(Vector3, (self.context, None, None))
		self.direction = stream.read_type(Vector3, (self.context, None, None))
		self.min = stream.read_float()
		self.max = stream.read_float()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		super().write(stream)
		stream.write_type(self.loc)
		stream.write_type(self.direction)
		stream.write_float(self.min)
		stream.write_float(self.max)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ListShort [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* loc = {self.loc.__repr__()}'
		s += f'\n	* direction = {self.direction.__repr__()}'
		s += f'\n	* min = {self.min.__repr__()}'
		s += f'\n	* max = {self.max.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
