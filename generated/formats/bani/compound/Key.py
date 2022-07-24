from source.formats.base.basic import fmt_member
from generated.formats.bani.compound.Vector3Short import Vector3Short
from generated.formats.bani.compound.Vector3Ushort import Vector3Ushort
from generated.struct import StructBase


class Key(StructBase):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.euler = 0
		self.translation = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.euler = Vector3Short(self.context, 0, None)
		self.translation = Vector3Ushort(self.context, 0, None)

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
		instance.euler = Vector3Short.from_stream(stream, instance.context, 0, None)
		instance.translation = Vector3Ushort.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Vector3Short.to_stream(stream, instance.euler)
		Vector3Ushort.to_stream(stream, instance.translation)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('euler', Vector3Short, (0, None))
		yield ('translation', Vector3Ushort, (0, None))

	def get_info_str(self, indent=0):
		return f'Key [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* euler = {fmt_member(self.euler, indent+1)}'
		s += f'\n	* translation = {fmt_member(self.translation, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
