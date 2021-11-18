from generated.context import ContextReference
from generated.formats.ms2.compound.CoreModelInfo import CoreModelInfo
from generated.formats.ms2.compound.Mdl2FourtyInfo import Mdl2FourtyInfo


class Mdl2ModelInfo:

	"""
	Wraps a CoreModelInfo
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.fourty = Mdl2FourtyInfo(self.context, None, None)
		self.info = CoreModelInfo(self.context, None, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.fourty = Mdl2FourtyInfo(self.context, None, None)
		self.info = CoreModelInfo(self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.fourty = stream.read_type(Mdl2FourtyInfo, (self.context, None, None))
		self.info = stream.read_type(CoreModelInfo, (self.context, None, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.fourty)
		stream.write_type(self.info)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Mdl2ModelInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* fourty = {self.fourty.__repr__()}'
		s += f'\n	* info = {self.info.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
