import typing
from generated.formats.ms2.compound.Onefiftytwo import Onefiftytwo


class PcBuffer1:

	"""
	cond="general info \ ms2 version == 32"
	"""
	whatever: typing.List[int]
	model_infos: typing.List[Onefiftytwo]

	# the padding between end of the modelinfo array and start of lodinfos
	some_zero: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.whatever = []
		self.model_infos = []
		self.some_zero = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.whatever = [stream.read_uint() for _ in range(8)]
		self.model_infos = [stream.read_type(Onefiftytwo) for _ in range(self.arg.mdl_2_count)]
		self.some_zero = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		for item in self.whatever: stream.write_uint(item)
		for item in self.model_infos: stream.write_type(item)
		stream.write_uint(self.some_zero)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'PcBuffer1 [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* whatever = ' + self.whatever.__repr__()
		s += '\n	* model_infos = ' + self.model_infos.__repr__()
		s += '\n	* some_zero = ' + self.some_zero.__repr__()
		s += '\n'
		return s
