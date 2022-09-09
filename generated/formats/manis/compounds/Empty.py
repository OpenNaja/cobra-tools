from generated.base_struct import BaseStruct


class Empty(BaseStruct):

	"""
	Grabs 00 bytes only
	"""

	__name__ = 'Empty'

	_import_key = 'manis.compounds.Empty'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
