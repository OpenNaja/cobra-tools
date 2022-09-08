from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class CinematicRoot(MemStruct):

	__name__ = 'CinematicRoot'

	_import_path = 'generated.formats.cinematic.compounds.CinematicRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_0 = 0
		self.u_1 = 0
		self.data = Pointer(self.context, 0, CinematicRoot._import_path_map["generated.formats.cinematic.compounds.CinematicData"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'u_0', Uint64, (0, None), (False, None)
		yield 'u_1', Uint64, (0, None), (False, None)
		yield 'data', Pointer, (0, CinematicRoot._import_path_map["generated.formats.cinematic.compounds.CinematicData"]), (False, None)

	def get_info_str(self, indent=0):
		return f'CinematicRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
