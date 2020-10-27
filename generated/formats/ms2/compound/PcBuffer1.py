import typing
from generated.array import Array
from generated.formats.ms2.compound.Onefiftytwo import Onefiftytwo


class PcBuffer1:

	"""
	cond="general info \ ms2 version == 32"
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.whatever = Array()
		self.model_infos = Array()

		# the padding between end of the modelinfo array and start of lodinfos
		self.some_zero = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.whatever.read(stream, 'Uint', 8, None)
		self.model_infos.read(stream, Onefiftytwo, self.arg.mdl_2_count, None)
		self.some_zero = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		self.whatever.write(stream, 'Uint', 8, None)
		self.model_infos.write(stream, Onefiftytwo, self.arg.mdl_2_count, None)
		stream.write_uint(self.some_zero)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'PcBuffer1 [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* whatever = ' + self.whatever.__repr__()
		s += '\n	* model_infos = ' + self.model_infos.__repr__()
		s += '\n	* some_zero = ' + self.some_zero.__repr__()
		s += '\n'
		return s
