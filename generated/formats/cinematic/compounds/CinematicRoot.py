from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class CinematicRoot(MemStruct):

	__name__ = 'CinematicRoot'

	_import_key = 'cinematic.compounds.CinematicRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_0 = 0
		self.u_1 = 0
		self.data = Pointer(self.context, 0, CinematicRoot._import_map["cinematic.compounds.CinematicData"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('u_0', Uint64, (0, None), (False, None), (None, None))
		yield ('u_1', Uint64, (0, None), (False, None), (None, None))
		yield ('data', Pointer, (0, CinematicRoot._import_map["cinematic.compounds.CinematicData"]), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'u_0', Uint64, (0, None), (False, None)
		yield 'u_1', Uint64, (0, None), (False, None)
		yield 'data', Pointer, (0, CinematicRoot._import_map["cinematic.compounds.CinematicData"]), (False, None)


CinematicRoot.init_attributes()
