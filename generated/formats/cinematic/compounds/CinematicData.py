from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class CinematicData(MemStruct):

	__name__ = 'CinematicData'

	_import_key = 'cinematic.compounds.CinematicData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.next_level_count = 0
		self.default_name = Pointer(self.context, 0, ZString)
		self.next_levels = ArrayPointer(self.context, self.next_level_count, CinematicData._import_map["cinematic.compounds.State"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'default_name', Pointer, (0, ZString), (False, None)
		yield 'next_levels', ArrayPointer, (instance.next_level_count, CinematicData._import_map["cinematic.compounds.State"]), (False, None)
		yield 'next_level_count', Uint64, (0, None), (False, None)
