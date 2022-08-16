import generated.formats.base.basic
import generated.formats.trackedridecar.compounds.TrackedRideCarSub
import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TrackedRideCarRoot(MemStruct):

	"""
	48 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.sub_count = 0
		self.total_vecs_count = 0
		self.vec = numpy.zeros((3,), dtype=numpy.dtype('float32'))
		self.zero_0 = 0
		self.zero_1 = 0
		self.sub = ArrayPointer(self.context, self.sub_count, generated.formats.trackedridecar.compounds.TrackedRideCarSub.TrackedRideCarSub)
		self.some_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.sub_count = 0
		self.total_vecs_count = 0
		self.vec = numpy.zeros((3,), dtype=numpy.dtype('float32'))
		self.zero_0 = 0
		self.zero_1 = 0
		self.sub = ArrayPointer(self.context, self.sub_count, generated.formats.trackedridecar.compounds.TrackedRideCarSub.TrackedRideCarSub)
		self.some_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.sub = ArrayPointer.from_stream(stream, instance.context, instance.sub_count, generated.formats.trackedridecar.compounds.TrackedRideCarSub.TrackedRideCarSub)
		instance.sub_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.total_vecs_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.vec = Array.from_stream(stream, instance.context, 0, None, (3,), Float)
		instance.zero_0 = Uint.from_stream(stream, instance.context, 0, None)
		instance.some_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
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
		Array.to_stream(stream, instance.vec, (3,), Float, instance.context, 0, None)
		Uint.to_stream(stream, instance.zero_0)
		Pointer.to_stream(stream, instance.some_name)
		Uint64.to_stream(stream, instance.zero_1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'sub', ArrayPointer, (instance.sub_count, generated.formats.trackedridecar.compounds.TrackedRideCarSub.TrackedRideCarSub), (False, None)
		yield 'sub_count', Uint, (0, None), (False, None)
		yield 'total_vecs_count', Uint, (0, None), (False, None)
		yield 'vec', Array, ((3,), Float, 0, None), (False, None)
		yield 'zero_0', Uint, (0, None), (False, None)
		yield 'some_name', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'zero_1', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'TrackedRideCarRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* sub = {self.fmt_member(self.sub, indent+1)}'
		s += f'\n	* sub_count = {self.fmt_member(self.sub_count, indent+1)}'
		s += f'\n	* total_vecs_count = {self.fmt_member(self.total_vecs_count, indent+1)}'
		s += f'\n	* vec = {self.fmt_member(self.vec, indent+1)}'
		s += f'\n	* zero_0 = {self.fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* some_name = {self.fmt_member(self.some_name, indent+1)}'
		s += f'\n	* zero_1 = {self.fmt_member(self.zero_1, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
