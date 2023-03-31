from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.basic import OffsetString


class AuxEntry(BaseStruct):

	"""
	describes an external AUX resource
	"""

	__name__ = 'AuxEntry'

	_import_key = 'ovl.compounds.AuxEntry'
	allow_np = True

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into files list
		self.file_index = 0
		self.basename = 0

		# byte count of the complete external resource file
		self.size = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('file_index', Uint, (0, None), (False, None), (None, None))
		yield ('basename', OffsetString, (None, None), (False, None), (None, None))
		yield ('size', Uint, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'file_index', Uint, (0, None), (False, None)
		yield 'basename', OffsetString, (instance.context.names, None), (False, None)
		yield 'size', Uint, (0, None), (False, None)


AuxEntry.init_attributes()
