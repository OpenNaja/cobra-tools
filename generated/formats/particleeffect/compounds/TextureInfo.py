from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class TextureInfo(MemStruct):

	__name__ = 'TextureInfo'

	_import_key = 'particleeffect.compounds.TextureInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
