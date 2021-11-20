import numpy
from generated.array import Array
from generated.formats.ovl.compound.ArchiveEntry import ArchiveEntry
from generated.formats.ovl.compound.AuxEntry import AuxEntry
from generated.formats.ovl.compound.DependencyEntry import DependencyEntry
from generated.formats.ovl.compound.DirEntry import DirEntry
from generated.formats.ovl.compound.FileEntry import FileEntry
from generated.formats.ovl.compound.MimeEntry import MimeEntry
from generated.formats.ovl.compound.Triplet import Triplet
from generated.formats.ovl.compound.UnknownEntry import UnknownEntry
from generated.formats.ovl.compound.ZlibInfo import ZlibInfo
from generated.formats.ovl_base.compound.GenericHeader import GenericHeader
from generated.formats.ovl_base.compound.PadAlign import PadAlign
from generated.formats.ovl_base.compound.ZStringBuffer import ZStringBuffer


class Header(GenericHeader):

	"""
	Found at the beginning of every OVL file
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Seems to match the number of LOD models for the file (has more than 1 file)
		self.lod_depth = 0

		# length of the Names block below, including 00 bytes
		self.len_names = 0

		# always = 0
		self.zero_2 = 0

		# count of external aux files, ie audio banks
		self.num_aux_entries = 0

		# count of directories
		self.num_dirs = 0

		# count of file mime types, aka. extensions with metadata
		self.num_mimes = 0

		# count of files
		self.num_files = 0

		# repeat count of files ??
		self.num_files_2 = 0

		# count of parts
		self.num_dependencies = 0

		# number of archives
		self.num_archives = 0

		# number of pool_groups across all archives
		self.num_pool_groups = 0

		# number of headers of all types across all archives
		self.num_pools = 0

		# number of DataEntries across all archives
		self.num_datas = 0

		# number of BufferEntries across all archives
		self.num_buffers = 0

		# number of files in external OVS archive
		self.num_files_ovs = 0

		# used in ZTUAC elephants
		self.ztuac_unk_0 = 0

		# used in ZTUAC elephants
		self.ztuac_unk_1 = 0

		# used in ZTUAC elephants
		self.ztuac_unk_2 = 0

		# length of archive names
		self.len_archive_names = 0

		# another Num Files
		self.num_files_3 = 0

		# length of the type names portion insideNames block (usually at the start), not counting 00 bytes
		self.len_type_names = 0

		# used in PZ1.6 for the first time
		self.num_triplets = 0

		# zeros
		self.reserved = numpy.zeros((12), dtype=numpy.dtype('uint32'))

		# Name buffer for assets and file mime types.
		self.names = ZStringBuffer(self.context, self.len_names, None)

		# Array of MimeEntry objects that represent a mime type (file extension) each.
		self.mimes = Array((self.num_mimes), MimeEntry, self.context, 0, None)

		# ?
		self.triplets = Array((self.num_triplets), Triplet, self.context, 0, None)

		# ?
		self.triplets_pad = PadAlign(self.context, self.triplets, 4)

		# Array of FileEntry objects.
		self.files = Array((self.num_files), FileEntry, self.context, 0, None)

		# Name buffer for archives, usually will be STATIC followed by any OVS names
		self.archive_names = ZStringBuffer(self.context, self.len_archive_names, None)

		# Array of ArchiveEntry objects.
		self.archives = Array((self.num_archives), ArchiveEntry, self.context, 0, None)

		# Array of DirEntry objects.
		self.dirs = Array((self.num_dirs), DirEntry, self.context, 0, None)

		# aka InstancesArray of DependencyEntry objects.
		self.dependencies = Array((self.num_dependencies), DependencyEntry, self.context, 0, None)

		# Array of AuxEntry objects.
		self.aux_entries = Array((self.num_aux_entries), AuxEntry, self.context, 0, None)

		# after aux in ZTUAC
		self.dependencies = Array((self.num_dependencies), DependencyEntry, self.context, 0, None)

		# Array of UnknownEntry objects.
		self.unknowns = Array((self.num_files_ovs), UnknownEntry, self.context, 0, None)

		# repeats by archive count
		self.zlibs = Array((self.num_archives), ZlibInfo, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.lod_depth = 0
		self.len_names = 0
		self.zero_2 = 0
		self.num_aux_entries = 0
		self.num_dirs = 0
		self.num_mimes = 0
		self.num_files = 0
		self.num_files_2 = 0
		self.num_dependencies = 0
		self.num_archives = 0
		self.num_pool_groups = 0
		self.num_pools = 0
		self.num_datas = 0
		self.num_buffers = 0
		self.num_files_ovs = 0
		self.ztuac_unk_0 = 0
		self.ztuac_unk_1 = 0
		self.ztuac_unk_2 = 0
		self.len_archive_names = 0
		self.num_files_3 = 0
		self.len_type_names = 0
		self.num_triplets = 0
		self.reserved = numpy.zeros((12), dtype=numpy.dtype('uint32'))
		self.names = ZStringBuffer(self.context, self.len_names, None)
		self.mimes = Array((self.num_mimes), MimeEntry, self.context, 0, None)
		if self.context.version >= 20:
			self.triplets = Array((self.num_triplets), Triplet, self.context, 0, None)
		if self.context.version >= 20:
			self.triplets_pad = PadAlign(self.context, self.triplets, 4)
		self.files = Array((self.num_files), FileEntry, self.context, 0, None)
		self.archive_names = ZStringBuffer(self.context, self.len_archive_names, None)
		self.archives = Array((self.num_archives), ArchiveEntry, self.context, 0, None)
		self.dirs = Array((self.num_dirs), DirEntry, self.context, 0, None)
		if not (self.context.version == 17):
			self.dependencies = Array((self.num_dependencies), DependencyEntry, self.context, 0, None)
		self.aux_entries = Array((self.num_aux_entries), AuxEntry, self.context, 0, None)
		if self.context.version == 17:
			self.dependencies = Array((self.num_dependencies), DependencyEntry, self.context, 0, None)
		self.unknowns = Array((self.num_files_ovs), UnknownEntry, self.context, 0, None)
		self.zlibs = Array((self.num_archives), ZlibInfo, self.context, 0, None)

	def read(self, stream):
		super().read(stream)
		self.lod_depth = stream.read_uint()
		self.len_names = stream.read_uint()
		self.zero_2 = stream.read_uint()
		self.num_aux_entries = stream.read_uint()
		self.num_dirs = stream.read_ushort()
		self.num_mimes = stream.read_ushort()
		self.num_files = stream.read_uint()
		self.num_files_2 = stream.read_uint()
		self.num_dependencies = stream.read_uint()
		self.num_archives = stream.read_uint()
		self.num_pool_groups = stream.read_uint()
		self.num_pools = stream.read_uint()
		self.num_datas = stream.read_uint()
		self.num_buffers = stream.read_uint()
		self.num_files_ovs = stream.read_uint()
		self.ztuac_unk_0 = stream.read_uint()
		self.ztuac_unk_1 = stream.read_uint()
		self.ztuac_unk_2 = stream.read_uint()
		self.len_archive_names = stream.read_uint()
		self.num_files_3 = stream.read_uint()
		self.len_type_names = stream.read_uint()
		self.num_triplets = stream.read_uint()
		self.reserved = stream.read_uints((12))
		self.names = stream.read_type(ZStringBuffer, (self.context, self.len_names, None))
		self.mimes.read(stream, MimeEntry, self.num_mimes, None)
		if self.context.version >= 20:
			self.triplets.read(stream, Triplet, self.num_triplets, None)
			self.triplets_pad = stream.read_type(PadAlign, (self.context, self.triplets, 4))
		self.files.read(stream, FileEntry, self.num_files, None)
		self.archive_names = stream.read_type(ZStringBuffer, (self.context, self.len_archive_names, None))
		self.archives.read(stream, ArchiveEntry, self.num_archives, None)
		self.dirs.read(stream, DirEntry, self.num_dirs, None)
		if not (self.context.version == 17):
			self.dependencies.read(stream, DependencyEntry, self.num_dependencies, None)
		self.aux_entries.read(stream, AuxEntry, self.num_aux_entries, None)
		if self.context.version == 17:
			self.dependencies.read(stream, DependencyEntry, self.num_dependencies, None)
		self.unknowns.read(stream, UnknownEntry, self.num_files_ovs, None)
		self.zlibs.read(stream, ZlibInfo, self.num_archives, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		super().write(stream)
		stream.write_uint(self.lod_depth)
		stream.write_uint(self.len_names)
		stream.write_uint(self.zero_2)
		stream.write_uint(self.num_aux_entries)
		stream.write_ushort(self.num_dirs)
		stream.write_ushort(self.num_mimes)
		stream.write_uint(self.num_files)
		stream.write_uint(self.num_files_2)
		stream.write_uint(self.num_dependencies)
		stream.write_uint(self.num_archives)
		stream.write_uint(self.num_pool_groups)
		stream.write_uint(self.num_pools)
		stream.write_uint(self.num_datas)
		stream.write_uint(self.num_buffers)
		stream.write_uint(self.num_files_ovs)
		stream.write_uint(self.ztuac_unk_0)
		stream.write_uint(self.ztuac_unk_1)
		stream.write_uint(self.ztuac_unk_2)
		stream.write_uint(self.len_archive_names)
		stream.write_uint(self.num_files_3)
		stream.write_uint(self.len_type_names)
		stream.write_uint(self.num_triplets)
		stream.write_uints(self.reserved)
		stream.write_type(self.names)
		self.mimes.write(stream, MimeEntry, self.num_mimes, None)
		if self.context.version >= 20:
			self.triplets.write(stream, Triplet, self.num_triplets, None)
			stream.write_type(self.triplets_pad)
		self.files.write(stream, FileEntry, self.num_files, None)
		stream.write_type(self.archive_names)
		self.archives.write(stream, ArchiveEntry, self.num_archives, None)
		self.dirs.write(stream, DirEntry, self.num_dirs, None)
		if not (self.context.version == 17):
			self.dependencies.write(stream, DependencyEntry, self.num_dependencies, None)
		self.aux_entries.write(stream, AuxEntry, self.num_aux_entries, None)
		if self.context.version == 17:
			self.dependencies.write(stream, DependencyEntry, self.num_dependencies, None)
		self.unknowns.write(stream, UnknownEntry, self.num_files_ovs, None)
		self.zlibs.write(stream, ZlibInfo, self.num_archives, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Header [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* lod_depth = {self.lod_depth.__repr__()}'
		s += f'\n	* len_names = {self.len_names.__repr__()}'
		s += f'\n	* zero_2 = {self.zero_2.__repr__()}'
		s += f'\n	* num_aux_entries = {self.num_aux_entries.__repr__()}'
		s += f'\n	* num_dirs = {self.num_dirs.__repr__()}'
		s += f'\n	* num_mimes = {self.num_mimes.__repr__()}'
		s += f'\n	* num_files = {self.num_files.__repr__()}'
		s += f'\n	* num_files_2 = {self.num_files_2.__repr__()}'
		s += f'\n	* num_dependencies = {self.num_dependencies.__repr__()}'
		s += f'\n	* num_archives = {self.num_archives.__repr__()}'
		s += f'\n	* num_pool_groups = {self.num_pool_groups.__repr__()}'
		s += f'\n	* num_pools = {self.num_pools.__repr__()}'
		s += f'\n	* num_datas = {self.num_datas.__repr__()}'
		s += f'\n	* num_buffers = {self.num_buffers.__repr__()}'
		s += f'\n	* num_files_ovs = {self.num_files_ovs.__repr__()}'
		s += f'\n	* ztuac_unk_0 = {self.ztuac_unk_0.__repr__()}'
		s += f'\n	* ztuac_unk_1 = {self.ztuac_unk_1.__repr__()}'
		s += f'\n	* ztuac_unk_2 = {self.ztuac_unk_2.__repr__()}'
		s += f'\n	* len_archive_names = {self.len_archive_names.__repr__()}'
		s += f'\n	* num_files_3 = {self.num_files_3.__repr__()}'
		s += f'\n	* len_type_names = {self.len_type_names.__repr__()}'
		s += f'\n	* num_triplets = {self.num_triplets.__repr__()}'
		s += f'\n	* reserved = {self.reserved.__repr__()}'
		s += f'\n	* names = {self.names.__repr__()}'
		s += f'\n	* mimes = {self.mimes.__repr__()}'
		s += f'\n	* triplets = {self.triplets.__repr__()}'
		s += f'\n	* triplets_pad = {self.triplets_pad.__repr__()}'
		s += f'\n	* files = {self.files.__repr__()}'
		s += f'\n	* archive_names = {self.archive_names.__repr__()}'
		s += f'\n	* archives = {self.archives.__repr__()}'
		s += f'\n	* dirs = {self.dirs.__repr__()}'
		s += f'\n	* dependencies = {self.dependencies.__repr__()}'
		s += f'\n	* aux_entries = {self.aux_entries.__repr__()}'
		s += f'\n	* dependencies = {self.dependencies.__repr__()}'
		s += f'\n	* unknowns = {self.unknowns.__repr__()}'
		s += f'\n	* zlibs = {self.zlibs.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
