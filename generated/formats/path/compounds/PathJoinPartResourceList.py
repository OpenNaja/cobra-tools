from generated.array import Array
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.path.compounds.PathJoinPartResource import PathJoinPartResource


class PathJoinPartResourceList(MemStruct):

	__name__ = 'PathJoinPartResourceList'

	_import_key = 'path.compounds.PathJoinPartResourceList'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.resources = Array(self.context, 0, None, (0,), PathJoinPartResource)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'resources', Array, (0, None, (instance.arg,), PathJoinPartResource), (False, None)
