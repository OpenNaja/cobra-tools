from generated.formats.base.basic import fmt_member
import generated.formats.base.basic
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class UnlockState(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.entity_name = 0
		self.level_name = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.entity_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.level_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.entity_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.level_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.entity_name.arg = 0
		instance.level_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.entity_name)
		Pointer.to_stream(stream, instance.level_name)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('entity_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('level_name', Pointer, (0, generated.formats.base.basic.ZString))

	def get_info_str(self, indent=0):
		return f'UnlockState [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* entity_name = {fmt_member(self.entity_name, indent+1)}'
		s += f'\n	* level_name = {fmt_member(self.level_name, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
