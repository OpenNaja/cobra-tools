import generated.formats.base.basic
import generated.formats.motiongraph.compounds.Transition
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MRFMember2(MemStruct):

	"""
	72 bytes
	only used if transition is in 'id'
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.count_3 = 0
		self.count_4 = 0
		self.count_5 = 0
		self.count_6 = 0
		self.transition = 0
		self.id = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.count_3 = 0
		self.count_4 = 0
		self.count_5 = 0
		self.count_6 = 0
		self.transition = Pointer(self.context, 0, generated.formats.motiongraph.compounds.Transition.Transition)
		self.id = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.transition = Pointer.from_stream(stream, instance.context, 0, generated.formats.motiongraph.compounds.Transition.Transition)
		instance.count_0 = stream.read_uint64()
		instance.count_1 = stream.read_uint64()
		instance.count_2 = stream.read_uint64()
		instance.count_3 = stream.read_uint64()
		instance.count_4 = stream.read_uint64()
		instance.count_5 = stream.read_uint64()
		instance.count_6 = stream.read_uint64()
		instance.id = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		if not isinstance(instance.transition, int):
			instance.transition.arg = 0
		if not isinstance(instance.id, int):
			instance.id.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.transition)
		stream.write_uint64(instance.count_0)
		stream.write_uint64(instance.count_1)
		stream.write_uint64(instance.count_2)
		stream.write_uint64(instance.count_3)
		stream.write_uint64(instance.count_4)
		stream.write_uint64(instance.count_5)
		stream.write_uint64(instance.count_6)
		Pointer.to_stream(stream, instance.id)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('transition', Pointer, (0, generated.formats.motiongraph.compounds.Transition.Transition))
		yield ('count_0', Uint64, (0, None))
		yield ('count_1', Uint64, (0, None))
		yield ('count_2', Uint64, (0, None))
		yield ('count_3', Uint64, (0, None))
		yield ('count_4', Uint64, (0, None))
		yield ('count_5', Uint64, (0, None))
		yield ('count_6', Uint64, (0, None))
		yield ('id', Pointer, (0, generated.formats.base.basic.ZString))

	def get_info_str(self, indent=0):
		return f'MRFMember2 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* transition = {self.fmt_member(self.transition, indent+1)}'
		s += f'\n	* count_0 = {self.fmt_member(self.count_0, indent+1)}'
		s += f'\n	* count_1 = {self.fmt_member(self.count_1, indent+1)}'
		s += f'\n	* count_2 = {self.fmt_member(self.count_2, indent+1)}'
		s += f'\n	* count_3 = {self.fmt_member(self.count_3, indent+1)}'
		s += f'\n	* count_4 = {self.fmt_member(self.count_4, indent+1)}'
		s += f'\n	* count_5 = {self.fmt_member(self.count_5, indent+1)}'
		s += f'\n	* count_6 = {self.fmt_member(self.count_6, indent+1)}'
		s += f'\n	* id = {self.fmt_member(self.id, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
