from source.formats.base.basic import fmt_member
import generated.formats.base.basic
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class LuaModules(MemStruct):

	"""
	24 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.motion_graph = 0
		self.motion_graph_event_handling = 0
		self.motion_graph_actions = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.motion_graph = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.motion_graph_event_handling = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.motion_graph_actions = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.motion_graph = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.motion_graph_event_handling = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.motion_graph_actions = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.motion_graph.arg = 0
		instance.motion_graph_event_handling.arg = 0
		instance.motion_graph_actions.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.motion_graph)
		Pointer.to_stream(stream, instance.motion_graph_event_handling)
		Pointer.to_stream(stream, instance.motion_graph_actions)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'LuaModules [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* motion_graph = {fmt_member(self.motion_graph, indent+1)}'
		s += f'\n	* motion_graph_event_handling = {fmt_member(self.motion_graph_event_handling, indent+1)}'
		s += f'\n	* motion_graph_actions = {fmt_member(self.motion_graph_actions, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
