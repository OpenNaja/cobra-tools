from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.path.compounds.PathJoinPartResourceList import PathJoinPartResourceList


class PathJoinPartResourceRoot(MemStruct):

	__name__ = 'PathJoinPartResourceRoot'

	_import_path = 'generated.formats.path.compounds.PathJoinPartResourceRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.num_res = 0
		self.resources_list = Pointer(self.context, self.num_res, PathJoinPartResourceList)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.num_res = 0
		self.resources_list = Pointer(self.context, self.num_res, PathJoinPartResourceList)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.resources_list = Pointer.from_stream(stream, instance.context, instance.num_res, PathJoinPartResourceList)
		instance.num_res = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.resources_list, int):
			instance.resources_list.arg = instance.num_res

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.resources_list)
		Uint64.to_stream(stream, instance.num_res)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'resources_list', Pointer, (instance.num_res, PathJoinPartResourceList), (False, None)
		yield 'num_res', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'PathJoinPartResourceRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* resources_list = {self.fmt_member(self.resources_list, indent+1)}'
		s += f'\n	* num_res = {self.fmt_member(self.num_res, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
