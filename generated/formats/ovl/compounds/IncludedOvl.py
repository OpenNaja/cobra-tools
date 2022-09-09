from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint


class IncludedOvl(BaseStruct):

	"""
	Description of one included ovl file that is force-loaded by this ovl
	"""

	__name__ = 'IncludedOvl'

	_import_path = 'generated.formats.ovl.compounds.IncludedOvl'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# offset in the header's names block. path is relative to this ovl's directory, without the .ovl suffix
		self.offset = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'offset', Uint, (0, None), (False, None)
