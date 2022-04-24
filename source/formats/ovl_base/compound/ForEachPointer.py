# START_GLOBALS
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ovl_base.compound.Pointer import Pointer
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
# END_GLOBALS


class ForEachPointer(Pointer):

	"""
	a pointer to an array in an ovl memory layout
	"""

	context = ContextReference()

# START_CLASS

	def read_template(self):
		if self.template:
			if isinstance(self.arg, ArrayPointer):
				args = self.arg.data
			else:
				raise AttributeError(f"Unsupported arg {type(self.arg)} for ForEachPointer")
			self.data = Array((len(args)), self.template, self.context, set_default=False)
			stream = self.frag.pointers[1].stream
			self.data[:] = [self.template.from_stream(stream, self.context, arg) for arg in args]

	# def write_template(self):
	# 	assert self.template is not None
	# 	# Array.to_stream(self.frag.pointers[1].stream, self.data, (len(self.data),), self.template, self.context, 0, None)
	# 	self.frag.pointers[1].write_instance(self.template, self.data)
