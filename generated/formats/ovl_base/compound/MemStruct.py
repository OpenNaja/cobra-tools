
from generated.array import Array
from generated.formats.ovl_base.compound.Pointer import Pointer

ZERO = b"\x00"


from generated.context import ContextReference


class MemStruct:

	"""
	this is a struct that is capable of having pointers
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
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
		pass

	@classmethod
	def write_fields(cls, stream, instance):
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
		return f'MemStruct [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s

	def get_ptrs(self):
		return [val for prop, val in vars(self).items() if isinstance(val, Pointer)]

	def get_arrays(self):
		return [val for prop, val in vars(self).items() if isinstance(val, Array)]

	def read_ptrs(self, ovs, ref_ptr, ):
		# get all pointers in this struct
		ptrs = self.get_ptrs()
		for ptr in ptrs:
			self.handle_ptr(ptr, ovs, ref_ptr)
		arrays = self.get_arrays()
		# print(arrays)
		for array in arrays:
			for member in array:
				if isinstance(member, MemStruct):
					print("is a memstruct")
					member.read_ptrs(ovs, ref_ptr)

	def handle_ptr(self, ptr, ovs, ref_ptr):
		print(ptr, ptr.template, ptr.arg)
		f = ovs.frag_at_pointer(ref_ptr, offset=ptr.io_start)
		# ptr may be a nullptr, so ignore
		if not f:
			print("is a nullptr")
			return
		print(f)
		f_ptr = f.pointers[1]
		stream = f_ptr.pool.data
		stream.seek(f_ptr.data_offset)
		# ptr.data = f.pointers[1].load_as(ptr.template)[0]
		ptr.data = ptr.template.from_stream(stream, ptr.context, ptr.arg)
		if isinstance(ptr.data, MemStruct):
			print("is a memstruct")
			ptr.data.read_ptrs(ovs, f_ptr)
		print(ptr.data)

