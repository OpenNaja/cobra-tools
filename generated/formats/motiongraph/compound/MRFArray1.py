from source.formats.base.basic import fmt_member
from generated.array import Array
from generated.formats.motiongraph.compound.MRFEntry1 import MRFEntry1
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class MRFArray1(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.states = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.states = Array((self.arg,), MRFEntry1, self.context, 0, None)

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
		instance.states = Array.from_stream(stream, (instance.arg,), MRFEntry1, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.states, (instance.arg,), MRFEntry1, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('states', Array, ((instance.arg,), MRFEntry1, 0, None))

	def get_info_str(self, indent=0):
		return f'MRFArray1 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* states = {fmt_member(self.states, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
