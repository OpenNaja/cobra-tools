import generated.formats.base.basic
import generated.formats.path.compound.PointsList
import generated.formats.path.compound.Vector4
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class PathJoinPartResource(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.padding_1 = 0
		self.unk_byte_1 = 0
		self.unk_byte_2 = 0
		self.unk_byte_3 = 0
		self.num_points_1 = 0
		self.num_points_1_copy = 0
		self.num_points_2 = 0
		self.num_points_2_copy = 0
		self.num_points_3 = 0
		self.padding_2 = 0
		self.unk_points_1 = 0
		self.unk_points_2 = 0
		self.unk_vector = 0
		self.unk_shorts = 0
		self.unk_points_3 = 0
		self.pathresource = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.padding_1 = 0
		self.unk_byte_1 = 0
		self.unk_byte_2 = 0
		self.unk_byte_3 = 0
		self.num_points_1 = 0
		self.num_points_1_copy = 0
		self.num_points_2 = 0
		self.num_points_2_copy = 0
		self.num_points_3 = 0
		self.padding_2 = 0
		self.unk_points_1 = Pointer(self.context, self.num_points_1, generated.formats.path.compound.PointsList.PointsList)
		self.unk_points_2 = Pointer(self.context, self.num_points_2, generated.formats.path.compound.PointsList.PointsList)
		self.unk_vector = ArrayPointer(self.context, 1, generated.formats.path.compound.Vector4.Vector4)
		self.unk_shorts = ArrayPointer(self.context, 8, generated.formats.base.basic.Ushort)
		self.unk_points_3 = Pointer(self.context, self.num_points_3, generated.formats.path.compound.PointsList.PointsList)
		self.pathresource = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.unk_points_1 = Pointer.from_stream(stream, instance.context, instance.num_points_1, generated.formats.path.compound.PointsList.PointsList)
		instance.unk_points_2 = Pointer.from_stream(stream, instance.context, instance.num_points_2, generated.formats.path.compound.PointsList.PointsList)
		instance.unk_vector = ArrayPointer.from_stream(stream, instance.context, 1, generated.formats.path.compound.Vector4.Vector4)
		instance.unk_shorts = ArrayPointer.from_stream(stream, instance.context, 8, generated.formats.base.basic.Ushort)
		instance.unk_points_3 = Pointer.from_stream(stream, instance.context, instance.num_points_3, generated.formats.path.compound.PointsList.PointsList)
		instance.padding_1 = stream.read_uint64()
		instance.pathresource = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.unk_byte_1 = stream.read_byte()
		instance.unk_byte_2 = stream.read_byte()
		instance.unk_byte_3 = stream.read_byte()
		instance.num_points_1 = stream.read_byte()
		instance.num_points_1_copy = stream.read_byte()
		instance.num_points_2 = stream.read_byte()
		instance.num_points_2_copy = stream.read_byte()
		instance.num_points_3 = stream.read_byte()
		instance.padding_2 = stream.read_uint64()
		instance.unk_points_1.arg = instance.num_points_1
		instance.unk_points_2.arg = instance.num_points_2
		instance.unk_vector.arg = 1
		instance.unk_shorts.arg = 8
		instance.unk_points_3.arg = instance.num_points_3
		instance.pathresource.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.unk_points_1)
		Pointer.to_stream(stream, instance.unk_points_2)
		ArrayPointer.to_stream(stream, instance.unk_vector)
		ArrayPointer.to_stream(stream, instance.unk_shorts)
		Pointer.to_stream(stream, instance.unk_points_3)
		stream.write_uint64(instance.padding_1)
		Pointer.to_stream(stream, instance.pathresource)
		stream.write_byte(instance.unk_byte_1)
		stream.write_byte(instance.unk_byte_2)
		stream.write_byte(instance.unk_byte_3)
		stream.write_byte(instance.num_points_1)
		stream.write_byte(instance.num_points_1_copy)
		stream.write_byte(instance.num_points_2)
		stream.write_byte(instance.num_points_2_copy)
		stream.write_byte(instance.num_points_3)
		stream.write_uint64(instance.padding_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('unk_points_1', Pointer, (instance.num_points_1, generated.formats.path.compound.PointsList.PointsList))
		yield ('unk_points_2', Pointer, (instance.num_points_2, generated.formats.path.compound.PointsList.PointsList))
		yield ('unk_vector', ArrayPointer, (1, generated.formats.path.compound.Vector4.Vector4))
		yield ('unk_shorts', ArrayPointer, (8, generated.formats.base.basic.Ushort))
		yield ('unk_points_3', Pointer, (instance.num_points_3, generated.formats.path.compound.PointsList.PointsList))
		yield ('padding_1', Uint64, (0, None))
		yield ('pathresource', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('unk_byte_1', Byte, (0, None))
		yield ('unk_byte_2', Byte, (0, None))
		yield ('unk_byte_3', Byte, (0, None))
		yield ('num_points_1', Byte, (0, None))
		yield ('num_points_1_copy', Byte, (0, None))
		yield ('num_points_2', Byte, (0, None))
		yield ('num_points_2_copy', Byte, (0, None))
		yield ('num_points_3', Byte, (0, None))
		yield ('padding_2', Uint64, (0, None))

	def get_info_str(self, indent=0):
		return f'PathJoinPartResource [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* unk_points_1 = {self.fmt_member(self.unk_points_1, indent+1)}'
		s += f'\n	* unk_points_2 = {self.fmt_member(self.unk_points_2, indent+1)}'
		s += f'\n	* unk_vector = {self.fmt_member(self.unk_vector, indent+1)}'
		s += f'\n	* unk_shorts = {self.fmt_member(self.unk_shorts, indent+1)}'
		s += f'\n	* unk_points_3 = {self.fmt_member(self.unk_points_3, indent+1)}'
		s += f'\n	* padding_1 = {self.fmt_member(self.padding_1, indent+1)}'
		s += f'\n	* pathresource = {self.fmt_member(self.pathresource, indent+1)}'
		s += f'\n	* unk_byte_1 = {self.fmt_member(self.unk_byte_1, indent+1)}'
		s += f'\n	* unk_byte_2 = {self.fmt_member(self.unk_byte_2, indent+1)}'
		s += f'\n	* unk_byte_3 = {self.fmt_member(self.unk_byte_3, indent+1)}'
		s += f'\n	* num_points_1 = {self.fmt_member(self.num_points_1, indent+1)}'
		s += f'\n	* num_points_1_copy = {self.fmt_member(self.num_points_1_copy, indent+1)}'
		s += f'\n	* num_points_2 = {self.fmt_member(self.num_points_2, indent+1)}'
		s += f'\n	* num_points_2_copy = {self.fmt_member(self.num_points_2_copy, indent+1)}'
		s += f'\n	* num_points_3 = {self.fmt_member(self.num_points_3, indent+1)}'
		s += f'\n	* padding_2 = {self.fmt_member(self.padding_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
