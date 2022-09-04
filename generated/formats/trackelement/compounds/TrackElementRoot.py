from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class TrackElementRoot(MemStruct):

	"""
	PC: 32 bytes
	"""

	__name__ = 'TrackElementRoot'

	_import_path = 'generated.formats.trackelement.compounds.TrackElementRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.unk_0 = 0
		self.unk_1 = 0
		self.track_data = ArrayPointer(self.context, self.count, TrackElementRoot._import_path_map["generated.formats.trackelement.compounds.TrackElementData"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count = 0
		self.unk_0 = 0
		self.unk_1 = 0
		self.track_data = ArrayPointer(self.context, self.count, TrackElementRoot._import_path_map["generated.formats.trackelement.compounds.TrackElementData"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.track_data = ArrayPointer.from_stream(stream, instance.context, instance.count, TrackElementRoot._import_path_map["generated.formats.trackelement.compounds.TrackElementData"])
		instance.count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.unk_0 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.unk_1 = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.track_data, int):
			instance.track_data.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		ArrayPointer.to_stream(stream, instance.track_data)
		Uint64.to_stream(stream, instance.count)
		Uint64.to_stream(stream, instance.unk_0)
		Uint64.to_stream(stream, instance.unk_1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'track_data', ArrayPointer, (instance.count, TrackElementRoot._import_path_map["generated.formats.trackelement.compounds.TrackElementData"]), (False, None)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'unk_0', Uint64, (0, None), (False, 0)
		yield 'unk_1', Uint64, (0, None), (False, 0)

	def get_info_str(self, indent=0):
		return f'TrackElementRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
