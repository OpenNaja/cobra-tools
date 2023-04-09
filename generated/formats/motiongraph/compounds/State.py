from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class State(MemStruct):

	"""
	name uncertain
	40 bytes
	"""

	__name__ = 'State'

	_import_key = 'motiongraph.compounds.State'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk = 0
		self.activities_count = 0
		self.count_2 = 0
		self.activities = Pointer(self.context, self.activities_count, State._import_map["motiongraph.compounds.PtrList"])
		self.array_2 = Pointer(self.context, self.count_2, State._import_map["motiongraph.compounds.TransStructStopList"])
		self.id = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('unk', Uint, (0, None), (False, None), (None, None))
		yield ('activities_count', Uint, (0, None), (False, None), (None, None))
		yield ('activities', Pointer, (None, State._import_map["motiongraph.compounds.PtrList"]), (False, None), (None, None))
		yield ('count_2', Uint64, (0, None), (False, None), (None, None))
		yield ('array_2', Pointer, (None, State._import_map["motiongraph.compounds.TransStructStopList"]), (False, None), (None, None))
		yield ('id', Pointer, (0, ZString), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk', Uint, (0, None), (False, None)
		yield 'activities_count', Uint, (0, None), (False, None)
		yield 'activities', Pointer, (instance.activities_count, State._import_map["motiongraph.compounds.PtrList"]), (False, None)
		yield 'count_2', Uint64, (0, None), (False, None)
		yield 'array_2', Pointer, (instance.count_2, State._import_map["motiongraph.compounds.TransStructStopList"]), (False, None)
		yield 'id', Pointer, (0, ZString), (False, None)
