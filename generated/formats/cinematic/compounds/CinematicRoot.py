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

	def set_defaults(self):
		super().set_defaults()
		self.u_0 = 0
		self.u_1 = 0
		self.data = Pointer(self.context, 0, CinematicRoot._import_path_map["generated.formats.cinematic.compounds.CinematicData"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.u_0 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.u_1 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.data = Pointer.from_stream(stream, instance.context, 0, CinematicRoot._import_path_map["generated.formats.cinematic.compounds.CinematicData"])
		if not isinstance(instance.data, int):
			instance.data.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.u_0)
		Uint64.to_stream(stream, instance.u_1)
		Pointer.to_stream(stream, instance.data)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'u_0', Uint64, (0, None), (False, None)
		yield 'u_1', Uint64, (0, None), (False, None)
		yield 'data', Pointer, (0, CinematicRoot._import_path_map["generated.formats.cinematic.compounds.CinematicData"]), (False, None)

	def get_info_str(self, indent=0):
		return f'CinematicRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
