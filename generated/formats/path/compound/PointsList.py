from generated.formats.base.basic import fmt_member
from generated.array import Array
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.path.compound.Vector3 import Vector3


class PointsList(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.points = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.points = Array((self.arg,), Vector3, self.context, 0, None)

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
		instance.points = Array.from_stream(stream, (instance.arg,), Vector3, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.points, (instance.arg,), Vector3, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('points', Array, ((instance.arg,), Vector3, 0, None))

	def get_info_str(self, indent=0):
		return f'PointsList [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* points = {fmt_member(self.points, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
