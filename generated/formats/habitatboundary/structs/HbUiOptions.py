from generated.formats.ovl_base.basic import Bool
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class HbUiOptions(MemStruct):

	__name__ = 'HB_UI_Options'

	_import_path = 'generated.formats.habitatboundary.structs.HbUiOptions'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Controls the Straight-Curved option for barriers
		self.straight_curve = False

		# Controls the Windows option for barriers
		self.windows = False
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'straight_curve', Bool, (0, None), (False, None)
		yield 'windows', Bool, (0, None), (False, None)
