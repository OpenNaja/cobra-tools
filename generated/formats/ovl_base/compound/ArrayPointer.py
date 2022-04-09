
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ovl_base.compound.Pointer import Pointer
from source.formats.base.basic import fmt_member
from generated.formats.ovl_base.compound.Pointer import Pointer


class ArrayPointer(Pointer):

	"""
	a pointer to an array in an ovl memory layout
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		pass

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
		pass

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		pass

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

	def get_info_str(self):
		return f'Pointer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* data = {self.data.__repr__()}'
		return s

	def read_ptr(self, ovs, ref_ptr, io_start, sized_str_entry):
		"""Looks up the address of the pointer, checks if a frag points to pointer and reads the data at its address as
		the specified template."""
		# calculate offset specified to relative io_start
		rel_offset = self.io_start - io_start
		# print(f"handle_ptr dtype: {ptr.template.__name__} io_ref: {io_start} relative: {rel_offset} count: {ptr.arg}")
		# get a fragment whose ptr[0] lands on ref_ptr + rel_offset
		self.frag = ovs.frag_at_pointer(ref_ptr, offset=rel_offset)
		# ptr may be a nullptr, so ignore
		if not self.frag:
			# print("is a nullptr")
			return
		# store valid frag to be able to delete it later
		sized_str_entry.fragments.append(self.frag)
		# now read an instance of template class at the offset
		if self.template:
			# self.data = self.template.from_stream(self.frag.pointers[1].stream, self.context, self.arg)
			self.data = Array.from_stream(self.frag.pointers[1].stream, (self.arg,), self.template, self.context, 0, None)

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s

