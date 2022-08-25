import generated.formats.base.basic
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class LuaModules(MemStruct):

	"""
	24 bytes
	"""

	__name__ = LuaModules

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.motion_graph = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.motion_graph_event_handling = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.motion_graph_actions = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.motion_graph = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.motion_graph_event_handling = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.motion_graph_actions = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.motion_graph = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.motion_graph_event_handling = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.motion_graph_actions = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		if not isinstance(instance.motion_graph, int):
			instance.motion_graph.arg = 0
		if not isinstance(instance.motion_graph_event_handling, int):
			instance.motion_graph_event_handling.arg = 0
		if not isinstance(instance.motion_graph_actions, int):
			instance.motion_graph_actions.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.motion_graph)
		Pointer.to_stream(stream, instance.motion_graph_event_handling)
		Pointer.to_stream(stream, instance.motion_graph_actions)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'motion_graph', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'motion_graph_event_handling', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'motion_graph_actions', Pointer, (0, generated.formats.base.basic.ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'LuaModules [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* motion_graph = {self.fmt_member(self.motion_graph, indent+1)}'
		s += f'\n	* motion_graph_event_handling = {self.fmt_member(self.motion_graph_event_handling, indent+1)}'
		s += f'\n	* motion_graph_actions = {self.fmt_member(self.motion_graph_actions, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
