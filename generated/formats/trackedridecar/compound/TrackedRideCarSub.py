from source.formats.base.basic import fmt_member
import generated.formats.trackedridecar.compound.Vector3
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class TrackedRideCarSub(MemStruct):

	"""
	32 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.float = 0
		self.u_0 = 0
		self.vecs_count = 0
		self.zero_1 = 0
		self.vectors = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.float = 0.0
		self.u_0 = 0
		self.vecs_count = 0
		self.zero_1 = 0
		self.vectors = ArrayPointer(self.context, self.vecs_count, generated.formats.trackedridecar.compound.Vector3.Vector3)

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
		instance.float = stream.read_float()
		instance.u_0 = stream.read_uint()
		instance.vectors = ArrayPointer.from_stream(stream, instance.context, instance.vecs_count, generated.formats.trackedridecar.compound.Vector3.Vector3)
		instance.vecs_count = stream.read_uint64()
		instance.zero_1 = stream.read_uint64()
		instance.vectors.arg = instance.vecs_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_float(instance.float)
		stream.write_uint(instance.u_0)
		ArrayPointer.to_stream(stream, instance.vectors)
		stream.write_uint64(instance.vecs_count)
		stream.write_uint64(instance.zero_1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('float', Float, (0, None))
		yield ('u_0', Uint, (0, None))
		yield ('vectors', ArrayPointer, (instance.vecs_count, generated.formats.trackedridecar.compound.Vector3.Vector3))
		yield ('vecs_count', Uint64, (0, None))
		yield ('zero_1', Uint64, (0, None))

	def get_info_str(self, indent=0):
		return f'TrackedRideCarSub [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* float = {fmt_member(self.float, indent+1)}'
		s += f'\n	* u_0 = {fmt_member(self.u_0, indent+1)}'
		s += f'\n	* vectors = {fmt_member(self.vectors, indent+1)}'
		s += f'\n	* vecs_count = {fmt_member(self.vecs_count, indent+1)}'
		s += f'\n	* zero_1 = {fmt_member(self.zero_1, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
