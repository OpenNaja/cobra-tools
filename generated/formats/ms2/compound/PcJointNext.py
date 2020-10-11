import typing
from generated.formats.ms2.compound.PcFFCounter import PcFFCounter


class PcJointNext:

	# 11, then 11 FFs
	eleven_ff_stuff: PcFFCounter

	# usually 1F AA FF AA FF
	undecoded: typing.List[int]

	# start address in zstr buffer
	name_address: int

	# 1, 0, 0, 0
	uints: typing.List[int]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.eleven_ff_stuff = PcFFCounter()
		self.undecoded = []
		self.name_address = 0
		self.uints = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.eleven_ff_stuff = stream.read_type(PcFFCounter)
		self.undecoded = [stream.read_byte() for _ in range(5)]
		self.name_address = stream.read_uint()
		self.uints = [stream.read_uint() for _ in range(4)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.eleven_ff_stuff)
		for item in self.undecoded: stream.write_byte(item)
		stream.write_uint(self.name_address)
		for item in self.uints: stream.write_uint(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'PcJointNext [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* eleven_ff_stuff = ' + self.eleven_ff_stuff.__repr__()
		s += '\n	* undecoded = ' + self.undecoded.__repr__()
		s += '\n	* name_address = ' + self.name_address.__repr__()
		s += '\n	* uints = ' + self.uints.__repr__()
		s += '\n'
		return s
