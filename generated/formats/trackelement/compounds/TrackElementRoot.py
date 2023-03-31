from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TrackElementRoot(MemStruct):

	"""
	PC: 32 bytes
	"""

	__name__ = 'TrackElementRoot'

	_import_key = 'trackelement.compounds.TrackElementRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.track_data = ArrayPointer(self.context, self.count, TrackElementRoot._import_map["trackelement.compounds.TrackElementData"])
		self.unk_string_1 = Pointer(self.context, 0, ZString)
		self.unk_string_2 = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('track_data', ArrayPointer, (None, TrackElementRoot._import_map["trackelement.compounds.TrackElementData"]), (False, None), (None, None))
		yield ('count', Uint64, (0, None), (False, None), (None, None))
		yield ('unk_string_1', Pointer, (0, ZString), (False, None), (None, None))
		yield ('unk_string_2', Pointer, (0, ZString), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'track_data', ArrayPointer, (instance.count, TrackElementRoot._import_map["trackelement.compounds.TrackElementData"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'unk_string_1', Pointer, (0, ZString), (False, None)
		yield 'unk_string_2', Pointer, (0, ZString), (False, None)


TrackElementRoot.init_attributes()
