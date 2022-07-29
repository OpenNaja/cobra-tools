from generated.formats.base.basic import fmt_member
import generated.formats.cinematic.compound.CinematicData
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class CinematicRoot(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.u_0 = 0
		self.u_1 = 0
		self.data = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.u_0 = 0
		self.u_1 = 0
		self.data = Pointer(self.context, 0, generated.formats.cinematic.compound.CinematicData.CinematicData)

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
		instance.u_0 = stream.read_uint64()
		instance.u_1 = stream.read_uint64()
		instance.data = Pointer.from_stream(stream, instance.context, 0, generated.formats.cinematic.compound.CinematicData.CinematicData)
		instance.data.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint64(instance.u_0)
		stream.write_uint64(instance.u_1)
		Pointer.to_stream(stream, instance.data)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('u_0', Uint64, (0, None))
		yield ('u_1', Uint64, (0, None))
		yield ('data', Pointer, (0, generated.formats.cinematic.compound.CinematicData.CinematicData))

	def get_info_str(self, indent=0):
		return f'CinematicRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* u_0 = {fmt_member(self.u_0, indent+1)}'
		s += f'\n	* u_1 = {fmt_member(self.u_1, indent+1)}'
		s += f'\n	* data = {fmt_member(self.data, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
