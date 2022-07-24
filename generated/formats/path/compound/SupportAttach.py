from source.formats.base.basic import fmt_member
import generated.formats.base.basic
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer
from generated.formats.path.compound.Vector2 import Vector2


class SupportAttach(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.unk_int_1 = 0
		self.unk_int_2 = 0
		self.unk_vector = 0
		self.model_name = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.unk_int_1 = 0
		self.unk_int_2 = 0
		self.unk_vector = Vector2(self.context, 0, None)
		self.model_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.model_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.unk_int_1 = stream.read_uint64()
		instance.unk_int_2 = stream.read_uint64()
		instance.unk_vector = Vector2.from_stream(stream, instance.context, 0, None)
		instance.model_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.model_name)
		stream.write_uint64(instance.unk_int_1)
		stream.write_uint64(instance.unk_int_2)
		Vector2.to_stream(stream, instance.unk_vector)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('model_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('unk_int_1', Uint64, (0, None))
		yield ('unk_int_2', Uint64, (0, None))
		yield ('unk_vector', Vector2, (0, None))

	def get_info_str(self, indent=0):
		return f'SupportAttach [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* model_name = {fmt_member(self.model_name, indent+1)}'
		s += f'\n	* unk_int_1 = {fmt_member(self.unk_int_1, indent+1)}'
		s += f'\n	* unk_int_2 = {fmt_member(self.unk_int_2, indent+1)}'
		s += f'\n	* unk_vector = {fmt_member(self.unk_vector, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
