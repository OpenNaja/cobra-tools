from generated.base_struct import BaseStruct
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint


class HeaderPointer(BaseStruct):

	"""
	Not standalone, used by RootEntry, Fragment and DependencyEntry
	"""

	__name__ = 'HeaderPointer'

	_import_key = 'ovl.compounds.HeaderPointer'
	allow_np = True

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# The index of the MemPool this one relates to; OR, for entries referred to from AssetEntries: -1
		self.pool_index = -1

		# the byte offset relative to the start of the MemPool's data
		self.data_offset = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('pool_index', Int, (0, None), (False, -1), None)
		yield ('data_offset', Uint, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'pool_index', Int, (0, None), (False, -1)
		yield 'data_offset', Uint, (0, None), (False, None)


HeaderPointer.init_attributes()
