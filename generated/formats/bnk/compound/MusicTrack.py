from generated.formats.base.basic import Uint
from generated.formats.bnk.compound.MusicTrackInitialValues import MusicTrackInitialValues
from generated.struct import StructBase


class MusicTrack(StructBase):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# seen 114
		self.length = 0
		self.id = 0
		self.data = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.length = 0
		self.id = 0
		self.data = MusicTrackInitialValues(self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.length = stream.read_uint()
		instance.id = stream.read_uint()
		instance.data = MusicTrackInitialValues.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.length)
		stream.write_uint(instance.id)
		MusicTrackInitialValues.to_stream(stream, instance.data)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('length', Uint, (0, None))
		yield ('id', Uint, (0, None))
		yield ('data', MusicTrackInitialValues, (0, None))

	def get_info_str(self, indent=0):
		return f'MusicTrack [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* length = {self.fmt_member(self.length, indent+1)}'
		s += f'\n	* id = {self.fmt_member(self.id, indent+1)}'
		s += f'\n	* data = {self.fmt_member(self.data, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
