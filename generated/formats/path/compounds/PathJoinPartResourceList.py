from generated.array import Array
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.path.compounds.PathJoinPartResource import PathJoinPartResource


class PathJoinPartResourceList(MemStruct):

	__name__ = 'PathJoinPartResourceList'

	_import_path = 'generated.formats.path.compounds.PathJoinPartResourceList'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.resources = Array((0,), PathJoinPartResource, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.resources = Array((self.arg,), PathJoinPartResource, self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.resources = Array.from_stream(stream, instance.context, 0, None, (instance.arg,), PathJoinPartResource)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.resources, (instance.arg,), PathJoinPartResource, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'resources', Array, ((instance.arg,), PathJoinPartResource, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'PathJoinPartResourceList [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* resources = {self.fmt_member(self.resources, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
