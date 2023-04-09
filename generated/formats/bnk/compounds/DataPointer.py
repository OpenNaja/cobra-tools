from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint


class DataPointer(BaseStruct):

	"""
	second Section of a soundbank aux
	"""

	__name__ = 'DataPointer'

	_import_key = 'bnk.compounds.DataPointer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.wem_id = 0

		# offset into data section
		self.data_section_offset = 0

		# length of the wem file
		self.wem_filesize = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('wem_id', Uint, (0, None), (False, None), (None, None))
		yield ('data_section_offset', Uint, (0, None), (False, None), (None, None))
		yield ('wem_filesize', Uint, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'wem_id', Uint, (0, None), (False, None)
		yield 'data_section_offset', Uint, (0, None), (False, None)
		yield 'wem_filesize', Uint, (0, None), (False, None)
