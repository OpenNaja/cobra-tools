from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64


class AssetEntry(BaseStruct):

	"""
	refers to root entries so they can be grouped into set entries.
	points to RootEntry with pool_index -1
	"""

	__name__ = 'AssetEntry'

	_import_key = 'ovl.compounds.AssetEntry'
	allow_np = True

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.file_hash = 0
		self.ext_hash = 0

		# index into root entries array
		self.root_index = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('file_hash', Uint64, (0, None), (False, None), None)
		yield ('ext_hash', Uint64, (0, None), (False, None), True)
		yield ('root_index', Uint64, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'file_hash', Uint64, (0, None), (False, None)
		if instance.context.version >= 19:
			yield 'ext_hash', Uint64, (0, None), (False, None)
		yield 'root_index', Uint64, (0, None), (False, None)


AssetEntry.init_attributes()
