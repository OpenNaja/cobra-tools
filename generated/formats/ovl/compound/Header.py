import typing
from generated.formats.ovl.compound.DirEntry import DirEntry
from generated.formats.ovl.compound.MimeEntry import MimeEntry
from generated.formats.ovl.compound.OtherEntry import OtherEntry
from generated.formats.ovl.compound.ZlibInfo import ZlibInfo
from generated.formats.ovl.compound.FileEntry import FileEntry
from generated.formats.ovl.compound.ArchiveEntry import ArchiveEntry
from generated.formats.ovl.compound.TextureEntry import TextureEntry
from generated.formats.ovl.compound.UnknownEntry import UnknownEntry


class Header:

# Found at the beginning of every OVL file

	# 'FRES'
	fres: typing.List[int]

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

	# count of something
	num_others: int

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

	# 12 bytes zeros
	zeros: typing.List[int]

	# length of archive names
	len_archive_names: int

	# another Num Files
	num_files_3: int

	# length of the type names portion insideNames block (usually at the start), not counting 00 bytes
	len_type_names: int

	# 52 bytes zeros
	zeros_2: typing.List[int]

	# Name buffer for assets and file mime types.
	names: typing.List[Char]

	# Array of MimeEntry objects that represent a mime type (file extension) each.
	mimes: typing.List[MimeEntry]

	# Array of FileEntry objects.
	files: typing.List[FileEntry]

	# Name buffer for archives, usually will be STATIC followed by any OVS names
	archive_names: typing.List[Char]

	# Array of ArchiveEntry objects.
	archives: typing.List[ArchiveEntry]

	# Array of DirEntry objects.
	dirs: typing.List[DirEntry]

	# Array of TextureEntry objects.
	textures: typing.List[TextureEntry]

	# Array of OtherEntry objects.
	others: typing.List[OtherEntry]

	# Array of UnknownEntry objects.
	unknowns: typing.List[UnknownEntry]

	# repeats by archive count
	zlibs: typing.List[ZlibInfo]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.fres = [stream.read_byte() for _ in range(4)]
		self.flag = stream.read_byte()
		self.version = stream.read_byte()
		self.needs_bitswap = stream.read_byte()
		self.seventh_byte = stream.read_byte()
		self.flag_2 = stream.read_uint()
		self.zero = stream.read_uint()
		self.len_names = stream.read_uint()
		self.zero_2 = stream.read_uint()
		self.num_others = stream.read_uint()
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
		self.zeros = [stream.read_byte() for _ in range(12)]
		self.len_archive_names = stream.read_uint()
		self.num_files_3 = stream.read_uint()
		self.len_type_names = stream.read_uint()
		self.zeros_2 = [stream.read_byte() for _ in range(52)]
		self.names = [stream.read_char() for _ in range(self.len_names)]
		self.mimes = [stream.read_type(MimeEntry) for _ in range(self.num_mimes)]
		self.files = [stream.read_type(FileEntry) for _ in range(self.num_files)]
		self.archive_names = [stream.read_char() for _ in range(self.len_archive_names)]
		self.archives = [stream.read_type(ArchiveEntry) for _ in range(self.num_archives)]
		self.dirs = [stream.read_type(DirEntry) for _ in range(self.num_dirs)]
		self.textures = [stream.read_type(TextureEntry) for _ in range(self.num_textures)]
		self.others = [stream.read_type(OtherEntry) for _ in range(self.num_others)]
		self.unknowns = [stream.read_type(UnknownEntry) for _ in range(self.num_files_ovs)]
		self.zlibs = [stream.read_type(ZlibInfo) for _ in range(self.num_archives)]

	def write(self, stream):
		for item in self.fres: stream.write_byte(item)
		stream.write_byte(self.flag)
		stream.write_byte(self.version)
		stream.write_byte(self.needs_bitswap)
		stream.write_byte(self.seventh_byte)
		stream.write_uint(self.flag_2)
		stream.write_uint(self.zero)
		stream.write_uint(self.len_names)
		stream.write_uint(self.zero_2)
		stream.write_uint(self.num_others)
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
		for item in self.zeros: stream.write_byte(item)
		stream.write_uint(self.len_archive_names)
		stream.write_uint(self.num_files_3)
		stream.write_uint(self.len_type_names)
		for item in self.zeros_2: stream.write_byte(item)
		for item in self.names: stream.write_char(item)
		for item in self.mimes: stream.write_type(item)
		for item in self.files: stream.write_type(item)
		for item in self.archive_names: stream.write_char(item)
		for item in self.archives: stream.write_type(item)
		for item in self.dirs: stream.write_type(item)
		for item in self.textures: stream.write_type(item)
		for item in self.others: stream.write_type(item)
		for item in self.unknowns: stream.write_type(item)
		for item in self.zlibs: stream.write_type(item)

	def __repr__(self):
		s = 'Header'
		s += '\nfres ' + self.fres.__repr__()
		s += '\nflag ' + self.flag.__repr__()
		s += '\nversion ' + self.version.__repr__()
		s += '\nneeds_bitswap ' + self.needs_bitswap.__repr__()
		s += '\nseventh_byte ' + self.seventh_byte.__repr__()
		s += '\nflag_2 ' + self.flag_2.__repr__()
		s += '\nzero ' + self.zero.__repr__()
		s += '\nlen_names ' + self.len_names.__repr__()
		s += '\nzero_2 ' + self.zero_2.__repr__()
		s += '\nnum_others ' + self.num_others.__repr__()
		s += '\nnum_dirs ' + self.num_dirs.__repr__()
		s += '\nnum_mimes ' + self.num_mimes.__repr__()
		s += '\nnum_files ' + self.num_files.__repr__()
		s += '\nnum_files_2 ' + self.num_files_2.__repr__()
		s += '\nnum_textures ' + self.num_textures.__repr__()
		s += '\nnum_archives ' + self.num_archives.__repr__()
		s += '\nnum_header_types ' + self.num_header_types.__repr__()
		s += '\nnum_headers ' + self.num_headers.__repr__()
		s += '\nnum_datas ' + self.num_datas.__repr__()
		s += '\nnum_buffers ' + self.num_buffers.__repr__()
		s += '\nnum_files_ovs ' + self.num_files_ovs.__repr__()
		s += '\nzeros ' + self.zeros.__repr__()
		s += '\nlen_archive_names ' + self.len_archive_names.__repr__()
		s += '\nnum_files_3 ' + self.num_files_3.__repr__()
		s += '\nlen_type_names ' + self.len_type_names.__repr__()
		s += '\nzeros_2 ' + self.zeros_2.__repr__()
		s += '\nnames ' + self.names.__repr__()
		s += '\nmimes ' + self.mimes.__repr__()
		s += '\nfiles ' + self.files.__repr__()
		s += '\narchive_names ' + self.archive_names.__repr__()
		s += '\narchives ' + self.archives.__repr__()
		s += '\ndirs ' + self.dirs.__repr__()
		s += '\ntextures ' + self.textures.__repr__()
		s += '\nothers ' + self.others.__repr__()
		s += '\nunknowns ' + self.unknowns.__repr__()
		s += '\nzlibs ' + self.zlibs.__repr__()
		s += '\n'
		return s