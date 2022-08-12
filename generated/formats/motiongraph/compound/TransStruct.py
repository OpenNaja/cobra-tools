from generated.formats.base.basic import fmt_member
from generated.formats.motiongraph.compound.StateArray import StateArray
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class TransStruct(MemStruct):

	"""
	24 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.states = 0
		self.another_mrfentry_2 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.states = StateArray(self.context, 0, None)
		self.another_mrfentry_2 = Pointer(self.context, 0, None)

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
		instance.another_mrfentry_2 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.states = StateArray.from_stream(stream, instance.context, 0, None)
		instance.another_mrfentry_2.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.another_mrfentry_2)
		StateArray.to_stream(stream, instance.states)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('another_mrfentry_2', Pointer, (0, None))
		yield ('states', StateArray, (0, None))

	def get_info_str(self, indent=0):
		return f'TransStruct [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* another_mrfentry_2 = {fmt_member(self.another_mrfentry_2, indent+1)}'
		s += f'\n	* states = {fmt_member(self.states, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
