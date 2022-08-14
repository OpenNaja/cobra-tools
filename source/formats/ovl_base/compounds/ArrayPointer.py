# START_GLOBALS
from generated.array import Array
from generated.formats.ovl_base.compounds.Pointer import Pointer
# END_GLOBALS


class ArrayPointer(Pointer):

	"""
	a pointer to an array in an ovl memory layout
	"""

# START_CLASS

	def read_template(self):
		if self.template:
			self.data = Array.from_stream(self.frag.struct_ptr.stream, (self.arg,), self.template, self.context, 0, None)

	@classmethod
	def _to_xml(cls, instance, elem, debug):
		"""Assigns data self to xml elem"""
		# elem, prop, instance, arguments, debug
		# instance.template.to_xml(elem, instance._handle_xml_str(prop), instance.data, arguments, debug)
		# Array.to_xml(elem, "data", instance.data, (len(instance.data), instance.template, 0, None), debug)
		# Array._to_xml(elem, "data", instance.data, (len(instance.data), instance.template, 0, None), debug)
		Array._to_xml(instance.data, elem, debug)

	# def write_template(self):
	# 	assert self.template is not None
	# 	# Array.to_stream(self.frag.struct_ptr.stream, self.data, (len(self.data),), self.template, self.context, 0, None)
	# 	self.frag.struct_ptr.write_instance(self.template, self.data)
