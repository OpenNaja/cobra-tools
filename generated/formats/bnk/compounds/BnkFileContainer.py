from generated.formats.bnk.compounds.BnkBufferData import BnkBufferData
from generated.formats.ovl_base.compounds.GenericHeader import GenericHeader


class BnkFileContainer(GenericHeader):

	"""
	custom struct
	"""

	__name__ = 'BnkFileContainer'

	_import_path = 'generated.formats.bnk.compounds.BnkFileContainer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.bnk_header = BnkBufferData(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'bnk_header', BnkBufferData, (0, None), (False, None)
