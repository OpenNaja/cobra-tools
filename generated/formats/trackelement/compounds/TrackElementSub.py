from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TrackElementSub(MemStruct):

	"""
	PC: 32
	"""

	__name__ = 'TrackElementSub'

	_import_key = 'trackelement.compounds.TrackElementSub'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_0 = 0
		self.catwalk_right_lsm = Pointer(self.context, 0, ZString)
		self.catwalk_left_lsm = Pointer(self.context, 0, ZString)
		self.catwalk_both_lsm = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'catwalk_right_lsm', Pointer, (0, ZString), (False, None)
		yield 'catwalk_left_lsm', Pointer, (0, ZString), (False, None)
		yield 'catwalk_both_lsm', Pointer, (0, ZString), (False, None)
		yield 'unk_0', Uint64, (0, None), (False, None)
