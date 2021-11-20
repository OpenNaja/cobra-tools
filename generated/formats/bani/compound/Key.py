from generated.context import ContextReference
from generated.formats.bani.compound.Vector3Short import Vector3Short
from generated.formats.bani.compound.Vector3Ushort import Vector3Ushort


class Key:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.euler = Vector3Short(self.context, 0, None)
		self.translation = Vector3Ushort(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.euler = Vector3Short(self.context, 0, None)
		self.translation = Vector3Ushort(self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.euler = stream.read_type(Vector3Short, (self.context, 0, None))
		self.translation = stream.read_type(Vector3Ushort, (self.context, 0, None))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.euler)
		stream.write_type(self.translation)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Key [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* euler = {self.euler.__repr__()}'
		s += f'\n	* translation = {self.translation.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
