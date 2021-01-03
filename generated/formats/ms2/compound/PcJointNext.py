import typing
from generated.array import Array
from generated.formats.ms2.compound.PcFFCounter import PcFFCounter


class PcJointNext:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 11, then 11 FFs
		self.eleven_ff_stuff = PcFFCounter()

		# usually 1F AA FF AA FF
		self.undecoded = Array()

		# start address in zstr buffer
		self.name_address = 0

		# 1, 0, 0, 0
		self.uints = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.eleven_ff_stuff = stream.read_type(PcFFCounter)
		self.undecoded = stream.read_bytes((5))
		self.name_address = stream.read_uint()
		self.uints = stream.read_uints((4))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.eleven_ff_stuff)
		stream.write_bytes(self.undecoded)
		stream.write_uint(self.name_address)
		stream.write_uints(self.uints)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'PcJointNext [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* eleven_ff_stuff = {self.eleven_ff_stuff.__repr__()}'
		s += f'\n	* undecoded = {self.undecoded.__repr__()}'
		s += f'\n	* name_address = {self.name_address.__repr__()}'
		s += f'\n	* uints = {self.uints.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
