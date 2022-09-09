from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint


class SetEntry(BaseStruct):

	"""
	the asset indices of two consecutive SetEntries define a set of AssetEntries
	"""

	__name__ = 'SetEntry'

	_import_path = 'generated.formats.ovl.compounds.SetEntry'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.file_hash = 0
		self.ext_hash = 0

		# add from last set's entry up to this index to this set
		self.start = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'file_hash', Uint, (0, None), (False, None)
		if instance.context.version >= 19:
			yield 'ext_hash', Uint, (0, None), (False, None)
		yield 'start', Uint, (0, None), (False, None)
