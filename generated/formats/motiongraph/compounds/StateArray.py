from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class StateArray(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'StateArray'

	_import_key = 'motiongraph.compounds.StateArray'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.ptr = Pointer(self.context, self.count, StateArray._import_map["motiongraph.compounds.StateList"])
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('count', Uint64, (0, None), (False, None), None),
		('ptr', Pointer, (None, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'ptr', Pointer, (instance.count, StateArray._import_map["motiongraph.compounds.StateList"]), (False, None)
