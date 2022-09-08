from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class LuaModules(MemStruct):

	"""
	24 bytes
	"""

	__name__ = 'LuaModules'

	_import_path = 'generated.formats.motiongraph.compounds.LuaModules'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.motion_graph = Pointer(self.context, 0, ZString)
		self.motion_graph_event_handling = Pointer(self.context, 0, ZString)
		self.motion_graph_actions = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'motion_graph', Pointer, (0, ZString), (False, None)
		yield 'motion_graph_event_handling', Pointer, (0, ZString), (False, None)
		yield 'motion_graph_actions', Pointer, (0, ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'LuaModules [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
