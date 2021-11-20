
from generated.formats.ovl.versions import *
from hashes import constants_jwe, constants_pz, constants_jwe2


from generated.context import ContextReference


class FileEntry:

	"""
	Description of one file in the archive
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
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

		# if this file is part of a set, the set's sizedstr entry's pool type, else 0
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
		self.offset = stream.read_uint()
		self.file_hash = stream.read_uint()
		self.pool_type = stream.read_byte()
		self.set_pool_type = stream.read_byte()
		self.extension = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.offset)
		stream.write_uint(self.file_hash)
		stream.write_byte(self.pool_type)
		stream.write_byte(self.set_pool_type)
		stream.write_ushort(self.extension)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'FileEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* file_hash = {self.file_hash.__repr__()}'
		s += f'\n	* pool_type = {self.pool_type.__repr__()}'
		s += f'\n	* set_pool_type = {self.set_pool_type.__repr__()}'
		s += f'\n	* extension = {self.extension.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
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
		else:
			raise ValueError(f"Unsupported game {get_game(ovl)}")
		self.pool_type = constants.files_unkn_0[self.ext]
		self.set_pool_type = constants.files_unkn_1[self.ext]

