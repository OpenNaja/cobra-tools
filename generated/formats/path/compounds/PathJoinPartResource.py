from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class PathJoinPartResource(MemStruct):

	__name__ = 'PathJoinPartResource'

	_import_key = 'path.compounds.PathJoinPartResource'

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
		self.unk_points_1 = Pointer(self.context, self.num_points_1, PathJoinPartResource._import_map["path.compounds.PointsList"])
		self.unk_points_2 = Pointer(self.context, self.num_points_2, PathJoinPartResource._import_map["path.compounds.PointsList"])
		self.unk_vector = ArrayPointer(self.context, 1, PathJoinPartResource._import_map["path.compounds.Vector4"])
		self.unk_shorts = ArrayPointer(self.context, 8, Ushort)
		self.unk_points_3 = Pointer(self.context, self.num_points_3, PathJoinPartResource._import_map["path.compounds.PointsList"])
		self.pathresource = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('unk_points_1', Pointer, (None, PathJoinPartResource._import_map["path.compounds.PointsList"]), (False, None), (None, None))
		yield ('unk_points_2', Pointer, (None, PathJoinPartResource._import_map["path.compounds.PointsList"]), (False, None), (None, None))
		yield ('unk_vector', ArrayPointer, (1, PathJoinPartResource._import_map["path.compounds.Vector4"]), (False, None), (None, None))
		yield ('unk_shorts', ArrayPointer, (8, Ushort), (False, None), (None, None))
		yield ('unk_points_3', Pointer, (None, PathJoinPartResource._import_map["path.compounds.PointsList"]), (False, None), (None, None))
		yield ('padding_1', Uint64, (0, None), (True, 0), (None, None))
		yield ('pathresource', Pointer, (0, ZString), (False, None), (None, None))
		yield ('unk_byte_1', Byte, (0, None), (False, None), (None, None))
		yield ('unk_byte_2', Byte, (0, None), (False, None), (None, None))
		yield ('unk_byte_3', Byte, (0, None), (False, None), (None, None))
		yield ('num_points_1', Byte, (0, None), (False, None), (None, None))
		yield ('num_points_1_copy', Byte, (0, None), (False, None), (None, None))
		yield ('num_points_2', Byte, (0, None), (False, None), (None, None))
		yield ('num_points_2_copy', Byte, (0, None), (False, None), (None, None))
		yield ('num_points_3', Byte, (0, None), (False, None), (None, None))
		yield ('padding_2', Uint64, (0, None), (True, 0), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_points_1', Pointer, (instance.num_points_1, PathJoinPartResource._import_map["path.compounds.PointsList"]), (False, None)
		yield 'unk_points_2', Pointer, (instance.num_points_2, PathJoinPartResource._import_map["path.compounds.PointsList"]), (False, None)
		yield 'unk_vector', ArrayPointer, (1, PathJoinPartResource._import_map["path.compounds.Vector4"]), (False, None)
		yield 'unk_shorts', ArrayPointer, (8, Ushort), (False, None)
		yield 'unk_points_3', Pointer, (instance.num_points_3, PathJoinPartResource._import_map["path.compounds.PointsList"]), (False, None)
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


PathJoinPartResource.init_attributes()
