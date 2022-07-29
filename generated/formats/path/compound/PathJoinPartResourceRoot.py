from generated.formats.base.basic import fmt_member
import generated.formats.path.compound.PathJoinPartResourceList
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class PathJoinPartResourceRoot(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.num_res = 0
		self.resources_list = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.num_res = 0
		self.resources_list = Pointer(self.context, self.num_res, generated.formats.path.compound.PathJoinPartResourceList.PathJoinPartResourceList)

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
		instance.resources_list = Pointer.from_stream(stream, instance.context, instance.num_res, generated.formats.path.compound.PathJoinPartResourceList.PathJoinPartResourceList)
		instance.num_res = stream.read_uint64()
		instance.resources_list.arg = instance.num_res

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.resources_list)
		stream.write_uint64(instance.num_res)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('resources_list', Pointer, (instance.num_res, generated.formats.path.compound.PathJoinPartResourceList.PathJoinPartResourceList))
		yield ('num_res', Uint64, (0, None))

	def get_info_str(self, indent=0):
		return f'PathJoinPartResourceRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* resources_list = {fmt_member(self.resources_list, indent+1)}'
		s += f'\n	* num_res = {fmt_member(self.num_res, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
