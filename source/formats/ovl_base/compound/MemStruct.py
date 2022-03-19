# START_GLOBALS
from generated.array import Array
from generated.formats.ovl_base.compound.Pointer import Pointer

ZERO = b"\x00"


# END_GLOBALS

class MemStruct:
	"""this is a struct that is capable of having pointers"""
# START_CLASS

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
