# START_GLOBALS
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ovl_base.compound.Pointer import Pointer
# END_GLOBALS


class ArrayPointer(Pointer):

	"""
	a pointer to an array in an ovl memory layout
	"""

	context = ContextReference()

# START_CLASS

	def handle_template(self):
		if self.template:
			# self.data = self.template.from_stream(self.frag.pointers[1].stream, self.context, self.arg)
			self.data = Array.from_stream(self.frag.pointers[1].stream, (self.arg,), self.template, self.context, 0, None)

