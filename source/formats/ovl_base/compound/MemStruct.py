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

	def read_ptrs(self, ovs, ref_ptr, io_start=None):
		if not io_start:
			io_start = self.io_start
		# self.ref_ptr = ref_ptr
		# if isinstance(self, Array):
		# 	print("read_ptrs on array")
			# for member in self:
				# get all pointers in this struct
				# member.read_ptrs(ovs, ref_ptr)
				# member.handle_ptr(ptr, ovs, ref_ptr)
		# else:
		print("read_ptrs")
		# get all pointers in this struct
		ptrs = self.get_ptrs()
		for ptr in ptrs:
			self.handle_ptr(ptr, ovs, ref_ptr, io_start)
		arrays = self.get_arrays()
		# print(arrays)
		for array in arrays:
			print("array")
			# self.read_ptrs(ovs, ref_ptr)
			for member in array:
				if isinstance(member, MemStruct):
					print("member is a memstruct")
					member.read_ptrs(ovs, ref_ptr, array.io_start)

	def handle_ptr(self, ptr, ovs, ref_ptr, io_start):
		# this is wrong for arrays
		# rel_offset = ptr.io_start-self.io_start
		rel_offset = ptr.io_start-io_start
		print(f"handle_ptr dtype: {ptr.template.__name__} relative: {rel_offset} count: {ptr.arg}")
		# get a fragment that is relative to pointer + offset
		f = ovs.frag_at_pointer(ref_ptr, offset=rel_offset)
		# ptr may be a nullptr, so ignore
		if not f:
			print("is a nullptr")
			return
		# print(f)
		f_ptr = f.pointers[1]
		stream = f_ptr.pool.data
		stream.seek(f_ptr.data_offset)
		# ptr.data = f.pointers[1].load_as(ptr.template)[0]
		ptr.data = ptr.template.from_stream(stream, ptr.context, ptr.arg)
		if isinstance(ptr.data, Array):
			print("is an array")
			ptr.data.ref_ptr = f_ptr
			# for member in ptr.data:
			# 	if isinstance(member, MemStruct):
			# 		print("member is a memstruct")
			# 		member.read_ptrs(ovs, f_ptr)
		if isinstance(ptr.data, MemStruct):
			print("is a memstruct")
			ptr.data.read_ptrs(ovs, f_ptr)
		# print(ptr.data)

	def get_info_str(self):
		return f'\nMemStruct'

	def get_fields_str(self):
		return ""

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return ""