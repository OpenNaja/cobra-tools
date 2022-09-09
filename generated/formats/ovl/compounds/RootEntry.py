from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.ovl.compounds.HeaderPointer import HeaderPointer


class RootEntry(BaseStruct):

	"""
	Main file entry in the ovs, one per FileEntry
	"""

	__name__ = 'RootEntry'

	_import_path = 'generated.formats.ovl.compounds.RootEntry'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# id (index or djb2) of the file
		self.file_hash = 0

		# djb2 of extension
		self.ext_hash = 0

		# points to the main struct of this file OR -1 pointer for assets
		self.struct_ptr = HeaderPointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'file_hash', Uint, (0, None), (False, None)
		if instance.context.version >= 19:
			yield 'ext_hash', Uint, (0, None), (False, None)
		yield 'struct_ptr', HeaderPointer, (0, None), (False, None)
