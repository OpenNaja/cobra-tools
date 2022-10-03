from generated.formats.path.compounds.SupportAttachExtra import SupportAttachExtra


class Pillar(SupportAttachExtra):

	__name__ = 'Pillar'

	_import_key = 'path.compounds.Pillar'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		if set_default:
			self.set_defaults()

	_attribute_list = SupportAttachExtra._attribute_list + [
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
