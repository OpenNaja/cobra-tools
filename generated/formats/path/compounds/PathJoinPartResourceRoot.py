from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class PathJoinPartResourceRoot(MemStruct):

	__name__ = 'PathJoinPartResourceRoot'

	_import_path = 'generated.formats.path.compounds.PathJoinPartResourceRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.num_res = 0
		self.resources_list = Pointer(self.context, self.num_res, PathJoinPartResourceRoot._import_path_map["generated.formats.path.compounds.PathJoinPartResourceList"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.num_res = 0
		self.resources_list = Pointer(self.context, self.num_res, PathJoinPartResourceRoot._import_path_map["generated.formats.path.compounds.PathJoinPartResourceList"])

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'resources_list', Pointer, (instance.num_res, PathJoinPartResourceRoot._import_path_map["generated.formats.path.compounds.PathJoinPartResourceList"]), (False, None)
		yield 'num_res', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'PathJoinPartResourceRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
