from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.trackedridecar.compounds.Vector3 import Vector3


class TrackedRideCarSub(MemStruct):

	"""
	32 bytes
	"""

	__name__ = 'TrackedRideCarSub'

	_import_path = 'generated.formats.trackedridecar.compounds.TrackedRideCarSub'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.float = 0.0
		self.u_0 = 0
		self.vecs_count = 0
		self.zero_1 = 0
		self.vectors = ArrayPointer(self.context, self.vecs_count, Vector3)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.float = 0.0
		self.u_0 = 0
		self.vecs_count = 0
		self.zero_1 = 0
		self.vectors = ArrayPointer(self.context, self.vecs_count, Vector3)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.float = Float.from_stream(stream, instance.context, 0, None)
		instance.u_0 = Uint.from_stream(stream, instance.context, 0, None)
		instance.vectors = ArrayPointer.from_stream(stream, instance.context, instance.vecs_count, Vector3)
		instance.vecs_count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.zero_1 = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.vectors, int):
			instance.vectors.arg = instance.vecs_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Float.to_stream(stream, instance.float)
		Uint.to_stream(stream, instance.u_0)
		ArrayPointer.to_stream(stream, instance.vectors)
		Uint64.to_stream(stream, instance.vecs_count)
		Uint64.to_stream(stream, instance.zero_1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'float', Float, (0, None), (False, None)
		yield 'u_0', Uint, (0, None), (False, None)
		yield 'vectors', ArrayPointer, (instance.vecs_count, Vector3), (False, None)
		yield 'vecs_count', Uint64, (0, None), (False, None)
		yield 'zero_1', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'TrackedRideCarSub [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* float = {self.fmt_member(self.float, indent+1)}'
		s += f'\n	* u_0 = {self.fmt_member(self.u_0, indent+1)}'
		s += f'\n	* vectors = {self.fmt_member(self.vectors, indent+1)}'
		s += f'\n	* vecs_count = {self.fmt_member(self.vecs_count, indent+1)}'
		s += f'\n	* zero_1 = {self.fmt_member(self.zero_1, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
