from source.formats.base.basic import fmt_member
import generated.formats.wsm.compound.Vector3
import generated.formats.wsm.compound.Vector4
import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class WsmHeader(MemStruct):

	"""
	56 bytes for JWE2
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.duration = 0

		# likely
		self.frame_count = 0

		# unk
		self.unknowns = 0
		self.locs = 0
		self.quats = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.duration = 0.0
		self.frame_count = 0
		self.unknowns = numpy.zeros((8,), dtype=numpy.dtype('float32'))
		self.locs = ArrayPointer(self.context, self.frame_count, generated.formats.wsm.compound.Vector3.Vector3)
		self.quats = ArrayPointer(self.context, self.frame_count, generated.formats.wsm.compound.Vector4.Vector4)

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
		instance.duration = stream.read_float()
		instance.frame_count = stream.read_uint()
		instance.unknowns = stream.read_floats((8,))
		instance.locs = ArrayPointer.from_stream(stream, instance.context, instance.frame_count, generated.formats.wsm.compound.Vector3.Vector3)
		instance.quats = ArrayPointer.from_stream(stream, instance.context, instance.frame_count, generated.formats.wsm.compound.Vector4.Vector4)
		instance.locs.arg = instance.frame_count
		instance.quats.arg = instance.frame_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_float(instance.duration)
		stream.write_uint(instance.frame_count)
		stream.write_floats(instance.unknowns)
		ArrayPointer.to_stream(stream, instance.locs)
		ArrayPointer.to_stream(stream, instance.quats)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('duration', Float, (0, None))
		yield ('frame_count', Uint, (0, None))
		yield ('unknowns', Array, ((8,), Float, 0, None))
		yield ('locs', ArrayPointer, (instance.frame_count, generated.formats.wsm.compound.Vector3.Vector3))
		yield ('quats', ArrayPointer, (instance.frame_count, generated.formats.wsm.compound.Vector4.Vector4))

	def get_info_str(self, indent=0):
		return f'WsmHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* duration = {fmt_member(self.duration, indent+1)}'
		s += f'\n	* frame_count = {fmt_member(self.frame_count, indent+1)}'
		s += f'\n	* unknowns = {fmt_member(self.unknowns, indent+1)}'
		s += f'\n	* locs = {fmt_member(self.locs, indent+1)}'
		s += f'\n	* quats = {fmt_member(self.quats, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
