import typing
from generated.formats.ovl.compound.ArchiveEntry import ArchiveEntry
from generated.formats.ovl.compound.AuxEntry import AuxEntry
from generated.formats.ovl.compound.DirEntry import DirEntry
from generated.formats.ovl.compound.FileEntry import FileEntry
from generated.formats.ovl.compound.FixedString import FixedString
from generated.formats.ovl.compound.MimeEntry import MimeEntry
from generated.formats.ovl.compound.TextureEntry import TextureEntry
from generated.formats.ovl.compound.UnknownEntry import UnknownEntry
from generated.formats.ovl.compound.ZStringBuffer import ZStringBuffer
from generated.formats.ovl.compound.ZlibInfo import ZlibInfo


class Header:

	"""
	Found at the beginning of every OVL file
	"""

	# 'FRES'
	fres: FixedString

	# if 0x08 then 64bit
	flag: int

	# 0x13 = JWE
	version: int

	# endianness?
	needs_bitswap: int

	# always = 1
	seventh_byte: int = 1

	# usually 94 60 00 00
	flag_2: int

	# always = 0
	zero: int

	# length of the Names block below, including 00 bytes
	len_names: int

	# always = 0
	zero_2: int

	# count of external aux files, ie audio banks
	num_aux_entries: int

	# count of directories
	num_dirs: int

	# count of file mime types, aka. extensions with metadata
	num_mimes: int

	# count of files
	num_files: int

	# repeat count of files ??
	num_files_2: int

	# count of parts
	num_textures: int

	# number of archives
	num_archives: int

	# number of header types across all archives
	num_header_types: int

	# number of headers of all types across all archives
	num_headers: int

	# number of DataEntries across all archives
	num_datas: int

	# number of BufferEntries across all archives
	num_buffers: int

	# number of files in external OVS archive
	num_files_ovs: int

	# used in ZTUAC elephants
	ztuac_unknowns: typing.List[int]

	# length of archive names
	len_archive_names: int

	# another Num Files
	num_files_3: int

	# length of the type names portion insideNames block (usually at the start), not counting 00 bytes
	len_type_names: int

	# 52 bytes zeros
	zeros_2: typing.List[int]

	# Name buffer for assets and file mime types.
	names: ZStringBuffer

	# Array of MimeEntry objects that represent a mime type (file extension) each.
	mimes: typing.List[MimeEntry]

	# Array of FileEntry objects.
	files: typing.List[FileEntry]

	# Name buffer for archives, usually will be STATIC followed by any OVS names
	archive_names: ZStringBuffer

	# Array of ArchiveEntry objects.
	archives: typing.List[ArchiveEntry]

	# Array of DirEntry objects.
	dirs: typing.List[DirEntry]

	# Array of TextureEntry objects.
	textures: typing.List[TextureEntry]

	# Array of AuxEntry objects.
	aux_entries: typing.List[AuxEntry]

	# Array of UnknownEntry objects.
	unknowns: typing.List[UnknownEntry]

	# repeats by archive count
	zlibs: typing.List[ZlibInfo]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.fres = FixedString()
		self.flag = 0
		self.version = 0
		self.needs_bitswap = 0
		self.seventh_byte = 1
		self.flag_2 = 0
		self.zero = 0
		self.len_names = 0
		self.zero_2 = 0
		self.num_aux_entries = 0
		self.num_dirs = 0
		self.num_mimes = 0
		self.num_files = 0
		self.num_files_2 = 0
		self.num_textures = 0
		self.num_archives = 0
		self.num_header_types = 0
		self.num_headers = 0
		self.num_datas = 0
		self.num_buffers = 0
		self.num_files_ovs = 0
		self.ztuac_unknowns = []
		self.len_archive_names = 0
		self.num_files_3 = 0
		self.len_type_names = 0
		self.zeros_2 = []
		self.names = ZStringBuffer()
		self.mimes = []
		self.files = []
		self.archive_names = ZStringBuffer()
		self.archives = []
		self.dirs = []
		self.textures = []
		self.aux_entries = []
		self.unknowns = []
		self.zlibs = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.fres = stream.read_type(FixedString, (4,))
		self.flag = stream.read_byte()
		self.version = stream.read_byte()
		stream.version = self.version
		self.needs_bitswap = stream.read_byte()
		self.seventh_byte = stream.read_byte()
		self.flag_2 = stream.read_uint()
		self.zero = stream.read_uint()
		self.len_names = stream.read_uint()
		self.zero_2 = stream.read_uint()
		self.num_aux_entries = stream.read_uint()
		self.num_dirs = stream.read_ushort()
		self.num_mimes = stream.read_ushort()
		self.num_files = stream.read_uint()
		self.num_files_2 = stream.read_uint()
		self.num_textures = stream.read_uint()
		self.num_archives = stream.read_uint()
		self.num_header_types = stream.read_uint()
		self.num_headers = stream.read_uint()
		self.num_datas = stream.read_uint()
		self.num_buffers = stream.read_uint()
		self.num_files_ovs = stream.read_uint()
		self.ztuac_unknowns = [stream.read_uint() for _ in range(3)]
		self.len_archive_names = stream.read_uint()
		self.num_files_3 = stream.read_uint()
		self.len_type_names = stream.read_uint()
		self.zeros_2 = [stream.read_byte() for _ in range(52)]
		self.names = stream.read_type(ZStringBuffer, (self.len_names,))
		self.mimes = [stream.read_type(MimeEntry) for _ in range(self.num_mimes)]
		self.files = [stream.read_type(FileEntry) for _ in range(self.num_files)]
		self.archive_names = stream.read_type(ZStringBuffer, (self.len_archive_names,))
		self.archives = [stream.read_type(ArchiveEntry) for _ in range(self.num_archives)]
		self.dirs = [stream.read_type(DirEntry) for _ in range(self.num_dirs)]
		self.textures = [stream.read_type(TextureEntry) for _ in range(self.num_textures)]
		self.aux_entries = [stream.read_type(AuxEntry) for _ in range(self.num_aux_entries)]
		self.unknowns = [stream.read_type(UnknownEntry) for _ in range(self.num_files_ovs)]
		self.zlibs = [stream.read_type(ZlibInfo) for _ in range(self.num_archives)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.fres)
		stream.write_byte(self.flag)
		stream.write_byte(self.version)
		stream.version = self.version
		stream.write_byte(self.needs_bitswap)
		stream.write_byte(self.seventh_byte)
		stream.write_uint(self.flag_2)
		stream.write_uint(self.zero)
		stream.write_uint(self.len_names)
		stream.write_uint(self.zero_2)
		stream.write_uint(self.num_aux_entries)
		stream.write_ushort(self.num_dirs)
		stream.write_ushort(self.num_mimes)
		stream.write_uint(self.num_files)
		stream.write_uint(self.num_files_2)
		stream.write_uint(self.num_textures)
		stream.write_uint(self.num_archives)
		stream.write_uint(self.num_header_types)
		stream.write_uint(self.num_headers)
		stream.write_uint(self.num_datas)
		stream.write_uint(self.num_buffers)
		stream.write_uint(self.num_files_ovs)
		for item in self.ztuac_unknowns: stream.write_uint(item)
		stream.write_uint(self.len_archive_names)
		stream.write_uint(self.num_files_3)
		stream.write_uint(self.len_type_names)
		for item in self.zeros_2: stream.write_byte(item)
		stream.write_type(self.names)
		for item in self.mimes: stream.write_type(item)
		for item in self.files: stream.write_type(item)
		stream.write_type(self.archive_names)
		for item in self.archives: stream.write_type(item)
		for item in self.dirs: stream.write_type(item)
		for item in self.textures: stream.write_type(item)
		for item in self.aux_entries: stream.write_type(item)
		for item in self.unknowns: stream.write_type(item)
		for item in self.zlibs: stream.write_type(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Header [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* fres = ' + self.fres.__repr__()
		s += '\n	* flag = ' + self.flag.__repr__()
		s += '\n	* version = ' + self.version.__repr__()
		s += '\n	* needs_bitswap = ' + self.needs_bitswap.__repr__()
		s += '\n	* seventh_byte = ' + self.seventh_byte.__repr__()
		s += '\n	* flag_2 = ' + self.flag_2.__repr__()
		s += '\n	* zero = ' + self.zero.__repr__()
		s += '\n	* len_names = ' + self.len_names.__repr__()
		s += '\n	* zero_2 = ' + self.zero_2.__repr__()
		s += '\n	* num_aux_entries = ' + self.num_aux_entries.__repr__()
		s += '\n	* num_dirs = ' + self.num_dirs.__repr__()
		s += '\n	* num_mimes = ' + self.num_mimes.__repr__()
		s += '\n	* num_files = ' + self.num_files.__repr__()
		s += '\n	* num_files_2 = ' + self.num_files_2.__repr__()
		s += '\n	* num_textures = ' + self.num_textures.__repr__()
		s += '\n	* num_archives = ' + self.num_archives.__repr__()
		s += '\n	* num_header_types = ' + self.num_header_types.__repr__()
		s += '\n	* num_headers = ' + self.num_headers.__repr__()
		s += '\n	* num_datas = ' + self.num_datas.__repr__()
		s += '\n	* num_buffers = ' + self.num_buffers.__repr__()
		s += '\n	* num_files_ovs = ' + self.num_files_ovs.__repr__()
		s += '\n	* ztuac_unknowns = ' + self.ztuac_unknowns.__repr__()
		s += '\n	* len_archive_names = ' + self.len_archive_names.__repr__()
		s += '\n	* num_files_3 = ' + self.num_files_3.__repr__()
		s += '\n	* len_type_names = ' + self.len_type_names.__repr__()
		s += '\n	* zeros_2 = ' + self.zeros_2.__repr__()
		s += '\n	* names = ' + self.names.__repr__()
		s += '\n	* mimes = ' + self.mimes.__repr__()
		s += '\n	* files = ' + self.files.__repr__()
		s += '\n	* archive_names = ' + self.archive_names.__repr__()
		s += '\n	* archives = ' + self.archives.__repr__()
		s += '\n	* dirs = ' + self.dirs.__repr__()
		s += '\n	* textures = ' + self.textures.__repr__()
		s += '\n	* aux_entries = ' + self.aux_entries.__repr__()
		s += '\n	* unknowns = ' + self.unknowns.__repr__()
		s += '\n	* zlibs = ' + self.zlibs.__repr__()
		s += '\n'
		return s
