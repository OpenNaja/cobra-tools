from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class PathJoinPartResource(MemStruct):

	__name__ = 'PathJoinPartResource'

	_import_path = 'generated.formats.path.compounds.PathJoinPartResource'

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
		self.unk_points_1 = Pointer(self.context, self.num_points_1, PathJoinPartResource._import_path_map["generated.formats.path.compounds.PointsList"])
		self.unk_points_2 = Pointer(self.context, self.num_points_2, PathJoinPartResource._import_path_map["generated.formats.path.compounds.PointsList"])
		self.unk_vector = ArrayPointer(self.context, 1, PathJoinPartResource._import_path_map["generated.formats.path.compounds.Vector4"])
		self.unk_shorts = ArrayPointer(self.context, 8, Ushort)
		self.unk_points_3 = Pointer(self.context, self.num_points_3, PathJoinPartResource._import_path_map["generated.formats.path.compounds.PointsList"])
		self.pathresource = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
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
		self.unk_points_1 = Pointer(self.context, self.num_points_1, PathJoinPartResource._import_path_map["generated.formats.path.compounds.PointsList"])
		self.unk_points_2 = Pointer(self.context, self.num_points_2, PathJoinPartResource._import_path_map["generated.formats.path.compounds.PointsList"])
		self.unk_vector = ArrayPointer(self.context, 1, PathJoinPartResource._import_path_map["generated.formats.path.compounds.Vector4"])
		self.unk_shorts = ArrayPointer(self.context, 8, Ushort)
		self.unk_points_3 = Pointer(self.context, self.num_points_3, PathJoinPartResource._import_path_map["generated.formats.path.compounds.PointsList"])
		self.pathresource = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.unk_points_1 = Pointer.from_stream(stream, instance.context, instance.num_points_1, PathJoinPartResource._import_path_map["generated.formats.path.compounds.PointsList"])
		instance.unk_points_2 = Pointer.from_stream(stream, instance.context, instance.num_points_2, PathJoinPartResource._import_path_map["generated.formats.path.compounds.PointsList"])
		instance.unk_vector = ArrayPointer.from_stream(stream, instance.context, 1, PathJoinPartResource._import_path_map["generated.formats.path.compounds.Vector4"])
		instance.unk_shorts = ArrayPointer.from_stream(stream, instance.context, 8, Ushort)
		instance.unk_points_3 = Pointer.from_stream(stream, instance.context, instance.num_points_3, PathJoinPartResource._import_path_map["generated.formats.path.compounds.PointsList"])
		instance.padding_1 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.pathresource = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.unk_byte_1 = Byte.from_stream(stream, instance.context, 0, None)
		instance.unk_byte_2 = Byte.from_stream(stream, instance.context, 0, None)
		instance.unk_byte_3 = Byte.from_stream(stream, instance.context, 0, None)
		instance.num_points_1 = Byte.from_stream(stream, instance.context, 0, None)
		instance.num_points_1_copy = Byte.from_stream(stream, instance.context, 0, None)
		instance.num_points_2 = Byte.from_stream(stream, instance.context, 0, None)
		instance.num_points_2_copy = Byte.from_stream(stream, instance.context, 0, None)
		instance.num_points_3 = Byte.from_stream(stream, instance.context, 0, None)
		instance.padding_2 = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.unk_points_1, int):
			instance.unk_points_1.arg = instance.num_points_1
		if not isinstance(instance.unk_points_2, int):
			instance.unk_points_2.arg = instance.num_points_2
		if not isinstance(instance.unk_vector, int):
			instance.unk_vector.arg = 1
		if not isinstance(instance.unk_shorts, int):
			instance.unk_shorts.arg = 8
		if not isinstance(instance.unk_points_3, int):
			instance.unk_points_3.arg = instance.num_points_3
		if not isinstance(instance.pathresource, int):
			instance.pathresource.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.unk_points_1)
		Pointer.to_stream(stream, instance.unk_points_2)
		ArrayPointer.to_stream(stream, instance.unk_vector)
		ArrayPointer.to_stream(stream, instance.unk_shorts)
		Pointer.to_stream(stream, instance.unk_points_3)
		Uint64.to_stream(stream, instance.padding_1)
		Pointer.to_stream(stream, instance.pathresource)
		Byte.to_stream(stream, instance.unk_byte_1)
		Byte.to_stream(stream, instance.unk_byte_2)
		Byte.to_stream(stream, instance.unk_byte_3)
		Byte.to_stream(stream, instance.num_points_1)
		Byte.to_stream(stream, instance.num_points_1_copy)
		Byte.to_stream(stream, instance.num_points_2)
		Byte.to_stream(stream, instance.num_points_2_copy)
		Byte.to_stream(stream, instance.num_points_3)
		Uint64.to_stream(stream, instance.padding_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'unk_points_1', Pointer, (instance.num_points_1, PathJoinPartResource._import_path_map["generated.formats.path.compounds.PointsList"]), (False, None)
		yield 'unk_points_2', Pointer, (instance.num_points_2, PathJoinPartResource._import_path_map["generated.formats.path.compounds.PointsList"]), (False, None)
		yield 'unk_vector', ArrayPointer, (1, PathJoinPartResource._import_path_map["generated.formats.path.compounds.Vector4"]), (False, None)
		yield 'unk_shorts', ArrayPointer, (8, Ushort), (False, None)
		yield 'unk_points_3', Pointer, (instance.num_points_3, PathJoinPartResource._import_path_map["generated.formats.path.compounds.PointsList"]), (False, None)
		yield 'padding_1', Uint64, (0, None), (True, 0)
		yield 'pathresource', Pointer, (0, ZString), (False, None)
		yield 'unk_byte_1', Byte, (0, None), (False, None)
		yield 'unk_byte_2', Byte, (0, None), (False, None)
		yield 'unk_byte_3', Byte, (0, None), (False, None)
		yield 'num_points_1', Byte, (0, None), (False, None)
		yield 'num_points_1_copy', Byte, (0, None), (False, None)
		yield 'num_points_2', Byte, (0, None), (False, None)
		yield 'num_points_2_copy', Byte, (0, None), (False, None)
		yield 'num_points_3', Byte, (0, None), (False, None)
		yield 'padding_2', Uint64, (0, None), (True, 0)

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
