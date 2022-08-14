from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.ovl.compounds.HeaderPointer import HeaderPointer


class RootEntry(BaseStruct):

	"""
	Main file entry in the ovs, one per FileEntry
	"""

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

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.file_hash = stream.read_uint()
		if instance.context.version >= 19:
			instance.ext_hash = stream.read_uint()
		instance.struct_ptr = HeaderPointer.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.file_hash)
		if instance.context.version >= 19:
			stream.write_uint(instance.ext_hash)
		HeaderPointer.to_stream(stream, instance.struct_ptr)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield 'file_hash', Uint, (0, None)
		if instance.context.version >= 19:
			yield 'ext_hash', Uint, (0, None)
		yield 'struct_ptr', HeaderPointer, (0, None)

	def get_info_str(self, indent=0):
		return f'RootEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* file_hash = {self.fmt_member(self.file_hash, indent+1)}'
		s += f'\n	* ext_hash = {self.fmt_member(self.ext_hash, indent+1)}'
		s += f'\n	* struct_ptr = {self.fmt_member(self.struct_ptr, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
