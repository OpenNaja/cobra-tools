from source.formats.base.basic import fmt_member
from generated.context import ContextReference
from generated.formats.bnk.compound.MusicTrack import MusicTrack
from generated.formats.bnk.compound.SoundSfxVoice import SoundSfxVoice
from generated.formats.bnk.compound.TypeOther import TypeOther
from generated.formats.bnk.enum.HircType import HircType


class HircPointer:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.id = HircType(self.context, 0, None)
		self.data = SoundSfxVoice(self.context, 0, None)
		self.data = MusicTrack(self.context, 0, None)
		self.data = TypeOther(self.context, 0, None)
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
		instance.id = HircType.from_value(stream.read_ubyte())
		if instance.id == 2:
			instance.data = SoundSfxVoice.from_stream(stream, instance.context, 0, None)
		if instance.id == 11:
			instance.data = MusicTrack.from_stream(stream, instance.context, 0, None)
		if (instance.id != 2) and (instance.id != 11):
			instance.data = TypeOther.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_ubyte(instance.id.value)
		if instance.id == 2:
			SoundSfxVoice.to_stream(stream, instance.data)
		if instance.id == 11:
			MusicTrack.to_stream(stream, instance.data)
		if (instance.id != 2) and (instance.id != 11):
			TypeOther.to_stream(stream, instance.data)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'HircPointer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* id = {fmt_member(self.id, indent+1)}'
		s += f'\n	* data = {fmt_member(self.data, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
