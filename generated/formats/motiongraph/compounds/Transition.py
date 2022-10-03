from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Transition(MemStruct):

	"""
	40 bytes
	only used if transition is in 'id'
	"""

	__name__ = 'Transition'

	_import_key = 'motiongraph.compounds.Transition'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.ptr_0 = Pointer(self.context, self.count_1, Transition._import_map["motiongraph.compounds.PtrList"])
		self.ptr_1 = Pointer(self.context, self.count_2, Transition._import_map["motiongraph.compounds.TransStructArray"])
		self.id = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('count_0', Uint, (0, None), (False, None), None),
		('count_1', Uint, (0, None), (False, None), None),
		('ptr_0', Pointer, (None, None), (False, None), None),
		('count_2', Uint64, (0, None), (False, None), None),
		('ptr_1', Pointer, (None, None), (False, None), None),
		('id', Pointer, (0, ZString), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'count_0', Uint, (0, None), (False, None)
		yield 'count_1', Uint, (0, None), (False, None)
		yield 'ptr_0', Pointer, (instance.count_1, Transition._import_map["motiongraph.compounds.PtrList"]), (False, None)
		yield 'count_2', Uint64, (0, None), (False, None)
		yield 'ptr_1', Pointer, (instance.count_2, Transition._import_map["motiongraph.compounds.TransStructArray"]), (False, None)
		yield 'id', Pointer, (0, ZString), (False, None)
