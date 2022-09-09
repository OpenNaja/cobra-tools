from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.ovl.compounds.HeaderPointer import HeaderPointer


class DependencyEntry(BaseStruct):

	"""
	Description of dependency; links it to an entry from this archive
	"""

	__name__ = 'DependencyEntry'

	_import_key = 'ovl.compounds.DependencyEntry'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Hash of this dependency, for lookup in hash dict. Can be either external or internal.
		self.file_hash = 0

		# offset for extension into string name table
		self.offset = 0

		# index into ovl file table, points to the file entry where this dependency is used
		self.file_index = 0

		# pointer into flattened list of all archives' pools
		self.link_ptr = HeaderPointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'file_hash', Uint, (0, None), (False, None)
		yield 'offset', Uint, (0, None), (False, None)
		yield 'file_index', Uint, (0, None), (False, None)
		yield 'link_ptr', HeaderPointer, (0, None), (False, None)
