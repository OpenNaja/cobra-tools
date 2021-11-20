from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.InfoZTMemPool import InfoZTMemPool
from generated.formats.ms2.compound.SmartPadding import SmartPadding


class Ms2BufferInfoZTHeader:

	"""
	Data describing a MS2 buffer giving the size of the whole vertex and tri buffer.
	266 bytes
	very end of buffer 0 after the names list
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# sometimes 00 byte
		self.weird_padding = SmartPadding(self.context, None, None)
		self.unks = Array((), InfoZTMemPool, self.context, None, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.weird_padding = SmartPadding(self.context, None, None)
		self.unks = Array((), InfoZTMemPool, self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.weird_padding = stream.read_type(SmartPadding, (self.context, None, None))
		self.unks.read(stream, InfoZTMemPool, self.arg.unk_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.weird_padding)
		self.unks.write(stream, InfoZTMemPool, self.arg.unk_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Ms2BufferInfoZTHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* weird_padding = {self.weird_padding.__repr__()}'
		s += f'\n	* unks = {self.unks.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
