from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class BuildingSetRoot(MemStruct):

	"""
	# needs to be transformed into readable: 4260428428::CvjmejohTfu
	#                                        djbhash::BuildingSet
	"""

	__name__ = 'BuildingSetRoot'

	_import_key = 'buildingset.compounds.BuildingSetRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.set_count_or_type = 0
		self.unk_1_found_as_0 = 0
		self.unk_2_found_as_0 = 0
		self.set_id_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('set_id_name', Pointer, (0, ZString), (False, None), None),
		('set_count_or_type', Uint64, (0, None), (False, None), None),
		('unk_1_found_as_0', Uint64, (0, None), (False, None), None),
		('unk_2_found_as_0', Uint64, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'set_id_name', Pointer, (0, ZString), (False, None)
		yield 'set_count_or_type', Uint64, (0, None), (False, None)
		yield 'unk_1_found_as_0', Uint64, (0, None), (False, None)
		yield 'unk_2_found_as_0', Uint64, (0, None), (False, None)
