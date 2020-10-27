import typing
from generated.array import Array
from generated.formats.ms2.compound.PcFFCounter import PcFFCounter


class PcJointNext:

	def __init__(self, arg=None, template=None):
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
		self.undecoded.read(stream, 'Byte', 5, None)
		self.name_address = stream.read_uint()
		self.uints.read(stream, 'Uint', 4, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.eleven_ff_stuff)
		self.undecoded.write(stream, 'Byte', 5, None)
		stream.write_uint(self.name_address)
		self.uints.write(stream, 'Uint', 4, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'PcJointNext [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* eleven_ff_stuff = ' + self.eleven_ff_stuff.__repr__()
		s += '\n	* undecoded = ' + self.undecoded.__repr__()
		s += '\n	* name_address = ' + self.name_address.__repr__()
		s += '\n	* uints = ' + self.uints.__repr__()
		s += '\n'
		return s
