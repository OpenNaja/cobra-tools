import typing
from generated.array import Array
from generated.formats.ms2.compound.CoreModelInfo import CoreModelInfo


class Onefiftytwo:

	"""
	# equivalent to 38 uints, 152 bytes
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.model_info = CoreModelInfo()
		self.some = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.model_info = stream.read_type(CoreModelInfo)
		self.some.read(stream, 'Uint64', 7, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.model_info)
		self.some.write(stream, 'Uint64', 7, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Onefiftytwo [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* model_info = ' + self.model_info.__repr__()
		s += '\n	* some = ' + self.some.__repr__()
		s += '\n'
		return s
