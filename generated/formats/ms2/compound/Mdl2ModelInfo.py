from generated.formats.ms2.compound.CoreModelInfo import CoreModelInfo
from generated.formats.ms2.compound.Mdl2FourtyInfo import Mdl2FourtyInfo


class Mdl2ModelInfo:

	"""
	Wraps a CoreModelInfo
	"""
	fourty: Mdl2FourtyInfo
	info: CoreModelInfo

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.fourty = Mdl2FourtyInfo()
		self.info = CoreModelInfo()

	def read(self, stream):

		self.io_start = stream.tell()
		self.fourty = stream.read_type(Mdl2FourtyInfo)
		self.info = stream.read_type(CoreModelInfo)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.fourty)
		stream.write_type(self.info)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Mdl2ModelInfo [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* fourty = ' + self.fourty.__repr__()
		s += '\n	* info = ' + self.info.__repr__()
		s += '\n'
		return s
