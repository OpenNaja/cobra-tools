from source.formats.base.basic import fmt_member
from generated.formats.bnk.compound.MusicTrack import MusicTrack
from generated.formats.bnk.compound.SoundSfxVoice import SoundSfxVoice
from generated.formats.bnk.compound.TypeOther import TypeOther
from generated.formats.bnk.enum.HircType import HircType
from generated.struct import StructBase


class HircPointer(StructBase):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.id = 0
		self.data = 0
		self.data = 0
		self.data = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.id = HircType(self.context, 0, None)
		if self.id == 2:
			self.data = SoundSfxVoice(self.context, 0, None)
		if self.id == 11:
			self.data = MusicTrack(self.context, 0, None)
		if (self.id != 2) and (self.id != 11):
			self.data = TypeOther(self.context, 0, None)

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
		instance.id = HircType.from_value(stream.read_ubyte())
		if instance.id == 2:
			instance.data = SoundSfxVoice.from_stream(stream, instance.context, 0, None)
		if instance.id == 11:
			instance.data = MusicTrack.from_stream(stream, instance.context, 0, None)
		if (instance.id != 2) and (instance.id != 11):
			instance.data = TypeOther.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_ubyte(instance.id.value)
		if instance.id == 2:
			SoundSfxVoice.to_stream(stream, instance.data)
		if instance.id == 11:
			MusicTrack.to_stream(stream, instance.data)
		if (instance.id != 2) and (instance.id != 11):
			TypeOther.to_stream(stream, instance.data)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('id', HircType, (0, None))
		if instance.id == 2:
			yield ('data', SoundSfxVoice, (0, None))
		if instance.id == 11:
			yield ('data', MusicTrack, (0, None))
		if (instance.id != 2) and (instance.id != 11):
			yield ('data', TypeOther, (0, None))

	def get_info_str(self, indent=0):
		return f'HircPointer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* id = {fmt_member(self.id, indent+1)}'
		s += f'\n	* data = {fmt_member(self.data, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
