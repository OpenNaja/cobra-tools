import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TrackedRideCarRoot(MemStruct):

	"""
	48 bytes
	"""

	__name__ = 'TrackedRideCarRoot'

	_import_path = 'generated.formats.trackedridecar.compounds.TrackedRideCarRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.sub_count = 0
		self.total_vecs_count = 0
		self.vec = Array(self.context, 0, None, (0,), Float)
		self.zero_0 = 0
		self.zero_1 = 0
		self.sub = ArrayPointer(self.context, self.sub_count, TrackedRideCarRoot._import_path_map["generated.formats.trackedridecar.compounds.TrackedRideCarSub"])
		self.some_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.sub_count = 0
		self.total_vecs_count = 0
		self.vec = numpy.zeros((3,), dtype=numpy.dtype('float32'))
		self.zero_0 = 0
		self.zero_1 = 0
		self.sub = ArrayPointer(self.context, self.sub_count, TrackedRideCarRoot._import_path_map["generated.formats.trackedridecar.compounds.TrackedRideCarSub"])
		self.some_name = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.sub = ArrayPointer.from_stream(stream, instance.context, instance.sub_count, TrackedRideCarRoot._import_path_map["generated.formats.trackedridecar.compounds.TrackedRideCarSub"])
		instance.sub_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.total_vecs_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.vec = Array.from_stream(stream, instance.context, 0, None, (3,), Float)
		instance.zero_0 = Uint.from_stream(stream, instance.context, 0, None)
		instance.some_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.zero_1 = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.sub, int):
			instance.sub.arg = instance.sub_count
		if not isinstance(instance.some_name, int):
			instance.some_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		ArrayPointer.to_stream(stream, instance.sub)
		Uint.to_stream(stream, instance.sub_count)
		Uint.to_stream(stream, instance.total_vecs_count)
		Array.to_stream(stream, instance.vec, instance.context, 0, None, (3,), Float)
		Uint.to_stream(stream, instance.zero_0)
		Pointer.to_stream(stream, instance.some_name)
		Uint64.to_stream(stream, instance.zero_1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'sub', ArrayPointer, (instance.sub_count, TrackedRideCarRoot._import_path_map["generated.formats.trackedridecar.compounds.TrackedRideCarSub"]), (False, None)
		yield 'sub_count', Uint, (0, None), (False, None)
		yield 'total_vecs_count', Uint, (0, None), (False, None)
		yield 'vec', Array, (0, None, (3,), Float), (False, None)
		yield 'zero_0', Uint, (0, None), (False, None)
		yield 'some_name', Pointer, (0, ZString), (False, None)
		yield 'zero_1', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'TrackedRideCarRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
