
from generated.formats.ovl.versions import *
from hashes import constants_jwe, constants_pz, constants_jwe2, constants_pc


from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.struct import StructBase


class FileEntry(StructBase):

	"""
	Description of one file in the archive
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# offset in the ovl's names block; start offset of zero terminated string
		self.offset = 0

		# this hash is used to retrieve the file name from inside the archive
		self.file_hash = 0

		# pool type of this file's sizedstr pointer, if part of a set, it's usually the same as set pool type
		self.pool_type = 0

		# if this file is part of a set, the set's root entry's pool type, else 0
		self.set_pool_type = 0

		# index into 'Extensions' array
		self.extension = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.offset = 0
		self.file_hash = 0
		self.pool_type = 0
		self.set_pool_type = 0
		self.extension = 0

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
		instance.offset = stream.read_uint()
		instance.file_hash = stream.read_uint()
		instance.pool_type = stream.read_byte()
		instance.set_pool_type = stream.read_byte()
		instance.extension = stream.read_ushort()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.offset)
		stream.write_uint(instance.file_hash)
		stream.write_byte(instance.pool_type)
		stream.write_byte(instance.set_pool_type)
		stream.write_ushort(instance.extension)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('offset', Uint, (0, None))
		yield ('file_hash', Uint, (0, None))
		yield ('pool_type', Byte, (0, None))
		yield ('set_pool_type', Byte, (0, None))
		yield ('extension', Ushort, (0, None))

	def get_info_str(self, indent=0):
		return f'FileEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* file_hash = {fmt_member(self.file_hash, indent+1)}'
		s += f'\n	* pool_type = {fmt_member(self.pool_type, indent+1)}'
		s += f'\n	* set_pool_type = {fmt_member(self.set_pool_type, indent+1)}'
		s += f'\n	* extension = {fmt_member(self.extension, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

	def update_constants(self, ovl):
		"""Update the constants"""

		# update offset using the name buffer
		if is_jwe(ovl):
			constants = constants_jwe
		elif is_pz(ovl) or is_pz16(ovl):
			constants = constants_pz
		elif is_jwe2(ovl):
			constants = constants_jwe2
		elif is_pc(ovl):
			constants = constants_pc
		else:
			raise ValueError(f"Unsupported game {get_game(ovl)}")
		self.pool_type = constants.files_pool_type[self.ext]
		self.set_pool_type = constants.files_set_pool_type[self.ext]

