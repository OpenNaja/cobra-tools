from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TrackElementData(MemStruct):

	"""
	PC: 80
	"""

	__name__ = 'TrackElementData'

	_import_key = 'trackelement.compounds.TrackElementData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_0 = 0
		self.unk_1 = 0
		self.unk_2 = 0
		self.unk_3 = 32
		self.unk_4 = 1024
		self.unk_5 = 1
		self.unk_6 = 1
		self.unk_7 = 0
		self.loop_name = Pointer(self.context, 0, ZString)
		self.ovl_name = Pointer(self.context, 0, ZString)
		self.catwalk = Pointer(self.context, 0, TrackElementData._import_map["trackelement.compounds.TrackElementSub"])
		self.optional_catwalk = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'loop_name', Pointer, (0, ZString), (False, None)
		yield 'ovl_name', Pointer, (0, ZString), (False, None)
		yield 'catwalk', Pointer, (0, TrackElementData._import_map["trackelement.compounds.TrackElementSub"]), (False, None)
		yield 'unk_0', Uint64, (0, None), (False, None)
		yield 'optional_catwalk', Pointer, (0, ZString), (False, None)
		yield 'unk_1', Uint64, (0, None), (False, None)
		yield 'unk_2', Ushort, (0, None), (False, 0)
		yield 'unk_3', Ushort, (0, None), (False, 32)
		yield 'unk_4', Uint, (0, None), (False, 1024)
		yield 'unk_5', Uint, (0, None), (False, 1)
		yield 'unk_6', Uint, (0, None), (False, 1)
		yield 'unk_7', Uint64, (0, None), (False, None)
