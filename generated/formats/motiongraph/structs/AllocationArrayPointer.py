import logging

from generated.array import Array
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer


class AllocationArrayPointer(ArrayPointer):

	"""
	Motiongraph pointer whose target allocation is a contiguous array.
	"""

	__name__ = 'AllocationArrayPointer'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	def read_template(self, stream):
		if not self.template or self.target_pool is None or self.target_offset is None:
			self.data = None
			return
		size = self.target_pool.size_map.get(self.target_offset)
		sample = self.template(self.context, 0, None)
		element_size = self.template.get_size(sample, self.context, 0, None)
		if size is None or element_size <= 0 or size % element_size:
			logging.warning(
				"AllocationArrayPointer target %s | %s has size %s, not a multiple of %s for %s",
				self.target_pool.i,
				self.target_offset,
				size,
				element_size,
				self.template.__name__,
			)
			self.data = None
			return
		count = size // element_size
		self.data = Array.from_stream(
			stream, self.context, 0, None, (count,), self.template
		)

	@classmethod
	def _from_xml(cls, instance, elem):
		instance.data = Array(
			instance.context, 0, None, (len(elem),), instance.template, set_default=False
		)
		instance.data = Array._from_xml(instance.data, elem)
		return instance

