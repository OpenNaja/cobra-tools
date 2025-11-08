# START_GLOBALS
import logging

from generated.array import Array
from generated.formats.ovl_base.structs.Pointer import Pointer
# END_GLOBALS


class ArrayPointer(Pointer):

	"""
	a pointer to an array in an ovl memory layout
	"""

# START_CLASS

	def set_defaults(self):
		super(ArrayPointer, self).set_defaults()
		self.data = Array(self.context, 0, None, (self.arg,), self.template, True)

	def read_template(self, stream):
		if self.template:
			try:
				self.data = Array.from_stream(stream, self.context, 0, None, (self.arg,), self.template)
			except:
				logging.exception(f"Could not read array of '{self.template.__name__}'")
				self.data = None

	@classmethod
	def from_xml(cls, target, elem, prop, arg, template):
		"""Creates object for parent object 'target', from parent element elem."""
		# create Pointer instance
		instance = cls(target.context, arg, template, set_default=False)
		# check if the pointer holds data
		sub = elem.find(f'./{prop}')
		if sub is None:
			if arg:
				logging.warning(f"Missing array '{prop}' on XML element '{elem.tag}' for count {arg}")
			cls._from_xml(instance, ())
		else:
			cls._from_xml(instance, sub)
			cls.pool_type_from_xml(sub, instance)
		return instance

	@classmethod
	def _to_xml(cls, instance, elem, debug):
		"""Assigns data self to xml elem"""
		if callable(getattr(instance.template, "_to_xml_array", None)):
			instance.template._to_xml_array(instance.data, elem, debug)
			return
		# assert isinstance(instance.data, Array)
		try:
			Array._to_xml(instance.data, elem, debug)
		except:
			logging.warning(f"Could not convert array '{instance.data}' to XML")

	@classmethod
	def _from_xml(cls, instance, elem):
		if callable(getattr(instance.template, "_from_xml_array", None)):
			instance.data = instance.template._from_xml_array(None, elem)
			return
		arr = Array(instance.context, 0, None, (len(elem)), instance.template, set_default=False)
		instance.data = Array._from_xml(arr, elem)
		return instance
