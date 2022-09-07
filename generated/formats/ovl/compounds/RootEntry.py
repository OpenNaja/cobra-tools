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

	def set_defaults(self):
		super().set_defaults()
		self.file_hash = 0
		if self.context.version >= 19:
			self.ext_hash = 0
		self.struct_ptr = HeaderPointer(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.file_hash = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 19:
			instance.ext_hash = Uint.from_stream(stream, instance.context, 0, None)
		instance.struct_ptr = HeaderPointer.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.file_hash)
		if instance.context.version >= 19:
			Uint.to_stream(stream, instance.ext_hash)
		HeaderPointer.to_stream(stream, instance.struct_ptr)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'file_hash', Uint, (0, None), (False, None)
		if instance.context.version >= 19:
			yield 'ext_hash', Uint, (0, None), (False, None)
		yield 'struct_ptr', HeaderPointer, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'RootEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
