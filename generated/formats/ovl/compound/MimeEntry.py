
from generated.formats.ovl import *

lut_mime_version_jwe = {
	".fdb": 1,
	".banis": 5,
	".assetpkg": 2,
	".userinterfaceicondata": 1,
	".lua": 7,
	".txt": 2,
	".tex": 8,
	".ms2": 47,
	".mdl2": 47,
	".fgm": 6,
}

lut_mime_version_pz = {
	".fdb": 1,
	".bani": 5,
	".banis": 5,
	".assetpkg": 2,
	# ".userinterfaceicondata": 1,
	".lua": 7,
	".txt": 3,
	".tex": 9,
	".texturestream": 9,
	".ms2": 50,
	".mdl2": 50,
	".fgm": 6,
}


lut_mime_hash_jwe = {
	".assetpkg": 1145776474,
	".banis": 1177957172,
	".fdb": 2545474337,
	".fgm": 861771362,
	".mdl2": 4285397356,
	".ms2": 2893339803,
	".lua": 1779074288,
	".txt": 640591494,
	".tex": 3242366505,
	".userinterfaceicondata": 2127665351,
}

lut_mime_hash_pz = {
	".bani": 1380752341,
	".banis": 1177957172,
	".fgm": 861771362,
	".mdl2": 4285397382,
	".ms2": 2893339829,
	".tex": 3242366506,
	".texturestream": 4096653506,
	".assetpkg": 1145776474,
	".fdb": 2545474337,
	".lua": 1779074288,
	".txt": 640591495,
	# ".userinterfaceicondata": 2127665351,
}

class MimeEntry:

	"""
	Description of one mime type, which is sort of a container for
	Note that for JWE at least, inside the archive not the stored mime hash is used but the extension hash, has to be generated, eg. djb("bani") == 2090104799
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# offset in the header's Names block
		self.offset = 0

		# usually zero
		self.unknown = 0

		# changes with game version; hash of this file extension; same across all files, but seemingly not used anywhere else in the archive
		self.mime_hash = 0

		# usually increments with game
		self.mime_version = 0

		# Id of this class type. Later in the file there is a reference to this Id; offset into FileEntry list in number of files
		self.file_index_offset = 0

		# Number of entries of this class in the file.; from 'file index offset', this many files belong to this file extension
		self.file_count = 0

		# constant per mime, grab this many triplets
		self.triplet_count = 0

		# index into triplets list
		self.triplet_offset = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.offset = stream.read_uint()
		self.unknown = stream.read_uint()
		self.mime_hash = stream.read_uint()
		self.mime_version = stream.read_uint()
		stream.mime_version = self.mime_version
		self.file_index_offset = stream.read_uint()
		self.file_count = stream.read_uint()
		if stream.version >= 20:
			self.triplet_count = stream.read_uint()
			self.triplet_offset = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.offset)
		stream.write_uint(self.unknown)
		stream.write_uint(self.mime_hash)
		stream.write_uint(self.mime_version)
		stream.mime_version = self.mime_version
		stream.write_uint(self.file_index_offset)
		stream.write_uint(self.file_count)
		if stream.version >= 20:
			stream.write_uint(self.triplet_count)
			stream.write_uint(self.triplet_offset)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'MimeEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* unknown = {self.unknown.__repr__()}'
		s += f'\n	* mime_hash = {self.mime_hash.__repr__()}'
		s += f'\n	* mime_version = {self.mime_version.__repr__()}'
		s += f'\n	* file_index_offset = {self.file_index_offset.__repr__()}'
		s += f'\n	* file_count = {self.file_count.__repr__()}'
		s += f'\n	* triplet_count = {self.triplet_count.__repr__()}'
		s += f'\n	* triplet_offset = {self.triplet_offset.__repr__()}'
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
			self.mime_hash = lut_mime_hash_jwe.get(self.ext)
			self.mime_version = lut_mime_version_jwe.get(self.ext)
		elif is_pz(ovl) or is_pz16(ovl):
			self.mime_hash = lut_mime_hash_pz.get(self.ext)
			self.mime_version = lut_mime_version_pz.get(self.ext)
		else:
			raise ValueError(f"Unsupported game {get_game(ovl)}")

