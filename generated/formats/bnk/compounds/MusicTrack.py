from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.bnk.compounds.MusicTrackInitialValues import MusicTrackInitialValues


class MusicTrack(BaseStruct):

	__name__ = 'MusicTrack'

	_import_path = 'generated.formats.bnk.compounds.MusicTrack'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# seen 114
		self.length = 0
		self.id = 0
		self.data = MusicTrackInitialValues(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.length = 0
		self.id = 0
		self.data = MusicTrackInitialValues(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.length = Uint.from_stream(stream, instance.context, 0, None)
		instance.id = Uint.from_stream(stream, instance.context, 0, None)
		instance.data = MusicTrackInitialValues.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.length)
		Uint.to_stream(stream, instance.id)
		MusicTrackInitialValues.to_stream(stream, instance.data)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'length', Uint, (0, None), (False, None)
		yield 'id', Uint, (0, None), (False, None)
		yield 'data', MusicTrackInitialValues, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'MusicTrack [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
