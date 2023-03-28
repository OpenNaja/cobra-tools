from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Locomotion2AnimationInfo(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'Locomotion2AnimationInfo'

	_import_key = 'motiongraph.compounds.Locomotion2AnimationInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.phase_entry_window = 1.5
		self.priority = 0
		self.anim_type = 0
		self._pad = 0
		self.anim_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('anim_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('phase_entry_window', Float, (0, None), (False, 1.5), (None, None))
		yield ('priority', Ushort, (0, None), (False, None), (None, None))
		yield ('anim_type', Ubyte, (0, None), (False, None), (None, None))
		yield ('_pad', Ubyte, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'anim_name', Pointer, (0, ZString), (False, None)
		yield 'phase_entry_window', Float, (0, None), (False, 1.5)
		yield 'priority', Ushort, (0, None), (False, None)
		yield 'anim_type', Ubyte, (0, None), (False, None)
		yield '_pad', Ubyte, (0, None), (False, None)


Locomotion2AnimationInfo.init_attributes()
