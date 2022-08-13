import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Short


class PCJointThing(BaseStruct):

	"""
	8 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# -1
		self.shorts = numpy.zeros((4,), dtype=numpy.dtype('int16'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.shorts = numpy.zeros((4,), dtype=numpy.dtype('int16'))

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
		super().read_fields(stream, instance)
		instance.shorts = stream.read_shorts((4,))

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_shorts(instance.shorts)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('shorts', Array, ((4,), Short, 0, None))

	def get_info_str(self, indent=0):
		return f'PCJointThing [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* shorts = {self.fmt_member(self.shorts, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
