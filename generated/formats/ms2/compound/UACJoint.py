from source.formats.base.basic import fmt_member
import numpy
from generated.context import ContextReference


class UACJoint:

	"""
	36 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# variable
		self.unk = 0

		# some at least
		self.floats = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.unk = numpy.zeros((6,), dtype=numpy.dtype('uint16'))
		self.floats = numpy.zeros((6,), dtype=numpy.dtype('float32'))

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		instance.unk = stream.read_ushorts((6,))
		instance.floats = stream.read_floats((6,))

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_ushorts(instance.unk)
		stream.write_floats(instance.floats)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'UACJoint [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* unk = {fmt_member(self.unk, indent+1)}'
		s += f'\n	* floats = {fmt_member(self.floats, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
