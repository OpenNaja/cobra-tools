import numpy
from generated.array import Array
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.base.compounds.PadAlign import PadAlign
from generated.formats.base.compounds.ZStringBuffer import ZStringBuffer
from generated.formats.ovl.compounds.ArchiveEntry import ArchiveEntry
from generated.formats.ovl.compounds.AuxEntry import AuxEntry
from generated.formats.ovl.compounds.DependencyEntry import DependencyEntry
from generated.formats.ovl.compounds.FileEntry import FileEntry
from generated.formats.ovl.compounds.IncludedOvl import IncludedOvl
from generated.formats.ovl.compounds.MimeEntry import MimeEntry
from generated.formats.ovl.compounds.StreamEntry import StreamEntry
from generated.formats.ovl.compounds.Triplet import Triplet
from generated.formats.ovl.compounds.ZlibInfo import ZlibInfo
from generated.formats.ovl_base.compounds.GenericHeader import GenericHeader


class Header(GenericHeader):

	"""
	Found at the beginning of every OVL file
	"""

	__name__ = 'Header'

	_import_path = 'generated.formats.ovl.compounds.Header'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Seems to match the number of LOD models for the file (has more than 1 file)
		self.lod_depth = 0

		# length of the Names block below, including 00 bytes
		self.len_names = 0

		# always = 0
		self.zero_2 = 0

		# count of external aux files, ie audio banks
		self.num_aux_entries = 0

		# count of included ovl files that are available to this ovl
		self.num_included_ovls = 0

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

		# number of files in external OVS archives
		self.num_stream_files = 0

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
		self.reserved = Array((0,), Uint, self.context, 0, None)

		# Name buffer for assets and file mime types.
		self.names = ZStringBuffer(self.context, self.len_names, None)

		# used in DLA
		self.names_pad = Array((0,), Ubyte, self.context, 0, None)

		# Array of MimeEntry objects that represent a mime type (file extension) each.
		self.mimes = Array((0,), MimeEntry, self.context, 0, None)

		# ?
		self.triplets = Array((0,), Triplet, self.context, 0, None)

		# ?
		self.triplets_pad = PadAlign(self.context, 4, self.triplets)

		# Array of FileEntry objects.
		self.files = Array((0,), FileEntry, self.context, 0, None)

		# Name buffer for archives, usually will be STATIC followed by any OVS names
		self.archive_names = ZStringBuffer(self.context, self.len_archive_names, None)

		# Array of ArchiveEntry objects.
		self.archives = Array((0,), ArchiveEntry, self.context, 0, None)

		# Array of IncludedOvl objects.
		self.included_ovls = Array((0,), IncludedOvl, self.context, 0, None)

		# aka InstancesArray of DependencyEntry objects.
		self.dependencies = Array((0,), DependencyEntry, self.context, 0, None)

		# Array of AuxEntry objects.
		self.aux_entries = Array((0,), AuxEntry, self.context, 0, None)

		# after aux in ZTUAC and PC
		self.dependencies = Array((0,), DependencyEntry, self.context, 0, None)

		# Array of StreamEntry objects.
		self.stream_files = Array((0,), StreamEntry, self.context, 0, None)

		# repeats by archive count
		self.zlibs = Array((0,), ZlibInfo, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.lod_depth = 0
		self.len_names = 0
		self.zero_2 = 0
		self.num_aux_entries = 0
		self.num_included_ovls = 0
		self.num_mimes = 0
		self.num_files = 0
		self.num_files_2 = 0
		self.num_dependencies = 0
		self.num_archives = 0
		self.num_pool_groups = 0
		self.num_pools = 0
		self.num_datas = 0
		self.num_buffers = 0
		self.num_stream_files = 0
		self.ztuac_unk_0 = 0
		self.ztuac_unk_1 = 0
		self.ztuac_unk_2 = 0
		self.len_archive_names = 0
		self.num_files_3 = 0
		self.len_type_names = 0
		self.num_triplets = 0
		self.reserved = numpy.zeros((12,), dtype=numpy.dtype('uint32'))
		self.names = ZStringBuffer(self.context, self.len_names, None)
		if self.context.version <= 15:
			self.names_pad = numpy.zeros(((16 - (self.len_names % 16)) % 16,), dtype=numpy.dtype('uint8'))
		self.mimes = Array((self.num_mimes,), MimeEntry, self.context, 0, None)
		if self.context.version >= 20:
			self.triplets = Array((self.num_triplets,), Triplet, self.context, 0, None)
			self.triplets_pad = PadAlign(self.context, 4, self.triplets)
		self.files = Array((self.num_files,), FileEntry, self.context, 0, None)
		self.archive_names = ZStringBuffer(self.context, self.len_archive_names, None)
		self.archives = Array((self.num_archives,), ArchiveEntry, self.context, 0, None)
		self.included_ovls = Array((self.num_included_ovls,), IncludedOvl, self.context, 0, None)
		if self.context.version >= 19:
			self.dependencies = Array((self.num_dependencies,), DependencyEntry, self.context, 0, None)
		self.aux_entries = Array((self.num_aux_entries,), AuxEntry, self.context, 0, None)
		if self.context.version <= 18:
			self.dependencies = Array((self.num_dependencies,), DependencyEntry, self.context, 0, None)
		self.stream_files = Array((self.num_stream_files,), StreamEntry, self.context, 0, None)
		self.zlibs = Array((self.num_archives,), ZlibInfo, self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.lod_depth = Uint.from_stream(stream, instance.context, 0, None)
		instance.len_names = Uint.from_stream(stream, instance.context, 0, None)
		instance.zero_2 = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_aux_entries = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_included_ovls = Ushort.from_stream(stream, instance.context, 0, None)
		instance.num_mimes = Ushort.from_stream(stream, instance.context, 0, None)
		instance.num_files = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_files_2 = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_dependencies = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_archives = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_pool_groups = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_pools = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_datas = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_buffers = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_stream_files = Uint.from_stream(stream, instance.context, 0, None)
		instance.ztuac_unk_0 = Uint.from_stream(stream, instance.context, 0, None)
		instance.ztuac_unk_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.ztuac_unk_2 = Uint.from_stream(stream, instance.context, 0, None)
		instance.len_archive_names = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_files_3 = Uint.from_stream(stream, instance.context, 0, None)
		instance.len_type_names = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_triplets = Uint.from_stream(stream, instance.context, 0, None)
		instance.reserved = Array.from_stream(stream, instance.context, 0, None, (12,), Uint)
		instance.names = ZStringBuffer.from_stream(stream, instance.context, instance.len_names, None)
		if instance.context.version <= 15:
			instance.names_pad = Array.from_stream(stream, instance.context, 0, None, ((16 - (instance.len_names % 16)) % 16,), Ubyte)
		instance.mimes = Array.from_stream(stream, instance.context, 0, None, (instance.num_mimes,), MimeEntry)
		if instance.context.version >= 20:
			instance.triplets = Array.from_stream(stream, instance.context, 0, None, (instance.num_triplets,), Triplet)
			instance.triplets_pad = PadAlign.from_stream(stream, instance.context, 4, instance.triplets)
		instance.files = Array.from_stream(stream, instance.context, 0, None, (instance.num_files,), FileEntry)
		instance.archive_names = ZStringBuffer.from_stream(stream, instance.context, instance.len_archive_names, None)
		instance.archives = Array.from_stream(stream, instance.context, 0, None, (instance.num_archives,), ArchiveEntry)
		instance.included_ovls = Array.from_stream(stream, instance.context, 0, None, (instance.num_included_ovls,), IncludedOvl)
		if instance.context.version >= 19:
			instance.dependencies = Array.from_stream(stream, instance.context, 0, None, (instance.num_dependencies,), DependencyEntry)
		instance.aux_entries = Array.from_stream(stream, instance.context, 0, None, (instance.num_aux_entries,), AuxEntry)
		if instance.context.version <= 18:
			instance.dependencies = Array.from_stream(stream, instance.context, 0, None, (instance.num_dependencies,), DependencyEntry)
		instance.stream_files = Array.from_stream(stream, instance.context, 0, None, (instance.num_stream_files,), StreamEntry)
		instance.zlibs = Array.from_stream(stream, instance.context, 0, None, (instance.num_archives,), ZlibInfo)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.lod_depth)
		Uint.to_stream(stream, instance.len_names)
		Uint.to_stream(stream, instance.zero_2)
		Uint.to_stream(stream, instance.num_aux_entries)
		Ushort.to_stream(stream, instance.num_included_ovls)
		Ushort.to_stream(stream, instance.num_mimes)
		Uint.to_stream(stream, instance.num_files)
		Uint.to_stream(stream, instance.num_files_2)
		Uint.to_stream(stream, instance.num_dependencies)
		Uint.to_stream(stream, instance.num_archives)
		Uint.to_stream(stream, instance.num_pool_groups)
		Uint.to_stream(stream, instance.num_pools)
		Uint.to_stream(stream, instance.num_datas)
		Uint.to_stream(stream, instance.num_buffers)
		Uint.to_stream(stream, instance.num_stream_files)
		Uint.to_stream(stream, instance.ztuac_unk_0)
		Uint.to_stream(stream, instance.ztuac_unk_1)
		Uint.to_stream(stream, instance.ztuac_unk_2)
		Uint.to_stream(stream, instance.len_archive_names)
		Uint.to_stream(stream, instance.num_files_3)
		Uint.to_stream(stream, instance.len_type_names)
		Uint.to_stream(stream, instance.num_triplets)
		Array.to_stream(stream, instance.reserved, (12,), Uint, instance.context, 0, None)
		ZStringBuffer.to_stream(stream, instance.names)
		if instance.context.version <= 15:
			Array.to_stream(stream, instance.names_pad, ((16 - (instance.len_names % 16)) % 16,), Ubyte, instance.context, 0, None)
		Array.to_stream(stream, instance.mimes, (instance.num_mimes,), MimeEntry, instance.context, 0, None)
		if instance.context.version >= 20:
			Array.to_stream(stream, instance.triplets, (instance.num_triplets,), Triplet, instance.context, 0, None)
			PadAlign.to_stream(stream, instance.triplets_pad)
		Array.to_stream(stream, instance.files, (instance.num_files,), FileEntry, instance.context, 0, None)
		ZStringBuffer.to_stream(stream, instance.archive_names)
		Array.to_stream(stream, instance.archives, (instance.num_archives,), ArchiveEntry, instance.context, 0, None)
		Array.to_stream(stream, instance.included_ovls, (instance.num_included_ovls,), IncludedOvl, instance.context, 0, None)
		if instance.context.version >= 19:
			Array.to_stream(stream, instance.dependencies, (instance.num_dependencies,), DependencyEntry, instance.context, 0, None)
		Array.to_stream(stream, instance.aux_entries, (instance.num_aux_entries,), AuxEntry, instance.context, 0, None)
		if instance.context.version <= 18:
			Array.to_stream(stream, instance.dependencies, (instance.num_dependencies,), DependencyEntry, instance.context, 0, None)
		Array.to_stream(stream, instance.stream_files, (instance.num_stream_files,), StreamEntry, instance.context, 0, None)
		Array.to_stream(stream, instance.zlibs, (instance.num_archives,), ZlibInfo, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'lod_depth', Uint, (0, None), (False, None)
		yield 'len_names', Uint, (0, None), (False, None)
		yield 'zero_2', Uint, (0, None), (False, None)
		yield 'num_aux_entries', Uint, (0, None), (False, None)
		yield 'num_included_ovls', Ushort, (0, None), (False, None)
		yield 'num_mimes', Ushort, (0, None), (False, None)
		yield 'num_files', Uint, (0, None), (False, None)
		yield 'num_files_2', Uint, (0, None), (False, None)
		yield 'num_dependencies', Uint, (0, None), (False, None)
		yield 'num_archives', Uint, (0, None), (False, None)
		yield 'num_pool_groups', Uint, (0, None), (False, None)
		yield 'num_pools', Uint, (0, None), (False, None)
		yield 'num_datas', Uint, (0, None), (False, None)
		yield 'num_buffers', Uint, (0, None), (False, None)
		yield 'num_stream_files', Uint, (0, None), (False, None)
		yield 'ztuac_unk_0', Uint, (0, None), (False, None)
		yield 'ztuac_unk_1', Uint, (0, None), (False, None)
		yield 'ztuac_unk_2', Uint, (0, None), (False, None)
		yield 'len_archive_names', Uint, (0, None), (False, None)
		yield 'num_files_3', Uint, (0, None), (False, None)
		yield 'len_type_names', Uint, (0, None), (False, None)
		yield 'num_triplets', Uint, (0, None), (False, None)
		yield 'reserved', Array, ((12,), Uint, 0, None), (False, None)
		yield 'names', ZStringBuffer, (instance.len_names, None), (False, None)
		if instance.context.version <= 15:
			yield 'names_pad', Array, (((16 - (instance.len_names % 16)) % 16,), Ubyte, 0, None), (False, None)
		yield 'mimes', Array, ((instance.num_mimes,), MimeEntry, 0, None), (False, None)
		if instance.context.version >= 20:
			yield 'triplets', Array, ((instance.num_triplets,), Triplet, 0, None), (False, None)
			yield 'triplets_pad', PadAlign, (4, instance.triplets), (False, None)
		yield 'files', Array, ((instance.num_files,), FileEntry, 0, None), (False, None)
		yield 'archive_names', ZStringBuffer, (instance.len_archive_names, None), (False, None)
		yield 'archives', Array, ((instance.num_archives,), ArchiveEntry, 0, None), (False, None)
		yield 'included_ovls', Array, ((instance.num_included_ovls,), IncludedOvl, 0, None), (False, None)
		if instance.context.version >= 19:
			yield 'dependencies', Array, ((instance.num_dependencies,), DependencyEntry, 0, None), (False, None)
		yield 'aux_entries', Array, ((instance.num_aux_entries,), AuxEntry, 0, None), (False, None)
		if instance.context.version <= 18:
			yield 'dependencies', Array, ((instance.num_dependencies,), DependencyEntry, 0, None), (False, None)
		yield 'stream_files', Array, ((instance.num_stream_files,), StreamEntry, 0, None), (False, None)
		yield 'zlibs', Array, ((instance.num_archives,), ZlibInfo, 0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Header [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* lod_depth = {self.fmt_member(self.lod_depth, indent+1)}'
		s += f'\n	* len_names = {self.fmt_member(self.len_names, indent+1)}'
		s += f'\n	* zero_2 = {self.fmt_member(self.zero_2, indent+1)}'
		s += f'\n	* num_aux_entries = {self.fmt_member(self.num_aux_entries, indent+1)}'
		s += f'\n	* num_included_ovls = {self.fmt_member(self.num_included_ovls, indent+1)}'
		s += f'\n	* num_mimes = {self.fmt_member(self.num_mimes, indent+1)}'
		s += f'\n	* num_files = {self.fmt_member(self.num_files, indent+1)}'
		s += f'\n	* num_files_2 = {self.fmt_member(self.num_files_2, indent+1)}'
		s += f'\n	* num_dependencies = {self.fmt_member(self.num_dependencies, indent+1)}'
		s += f'\n	* num_archives = {self.fmt_member(self.num_archives, indent+1)}'
		s += f'\n	* num_pool_groups = {self.fmt_member(self.num_pool_groups, indent+1)}'
		s += f'\n	* num_pools = {self.fmt_member(self.num_pools, indent+1)}'
		s += f'\n	* num_datas = {self.fmt_member(self.num_datas, indent+1)}'
		s += f'\n	* num_buffers = {self.fmt_member(self.num_buffers, indent+1)}'
		s += f'\n	* num_stream_files = {self.fmt_member(self.num_stream_files, indent+1)}'
		s += f'\n	* ztuac_unk_0 = {self.fmt_member(self.ztuac_unk_0, indent+1)}'
		s += f'\n	* ztuac_unk_1 = {self.fmt_member(self.ztuac_unk_1, indent+1)}'
		s += f'\n	* ztuac_unk_2 = {self.fmt_member(self.ztuac_unk_2, indent+1)}'
		s += f'\n	* len_archive_names = {self.fmt_member(self.len_archive_names, indent+1)}'
		s += f'\n	* num_files_3 = {self.fmt_member(self.num_files_3, indent+1)}'
		s += f'\n	* len_type_names = {self.fmt_member(self.len_type_names, indent+1)}'
		s += f'\n	* num_triplets = {self.fmt_member(self.num_triplets, indent+1)}'
		s += f'\n	* reserved = {self.fmt_member(self.reserved, indent+1)}'
		s += f'\n	* names = {self.fmt_member(self.names, indent+1)}'
		s += f'\n	* names_pad = {self.fmt_member(self.names_pad, indent+1)}'
		s += f'\n	* mimes = {self.fmt_member(self.mimes, indent+1)}'
		s += f'\n	* triplets = {self.fmt_member(self.triplets, indent+1)}'
		s += f'\n	* triplets_pad = {self.fmt_member(self.triplets_pad, indent+1)}'
		s += f'\n	* files = {self.fmt_member(self.files, indent+1)}'
		s += f'\n	* archive_names = {self.fmt_member(self.archive_names, indent+1)}'
		s += f'\n	* archives = {self.fmt_member(self.archives, indent+1)}'
		s += f'\n	* included_ovls = {self.fmt_member(self.included_ovls, indent+1)}'
		s += f'\n	* dependencies = {self.fmt_member(self.dependencies, indent+1)}'
		s += f'\n	* aux_entries = {self.fmt_member(self.aux_entries, indent+1)}'
		s += f'\n	* dependencies = {self.fmt_member(self.dependencies, indent+1)}'
		s += f'\n	* stream_files = {self.fmt_member(self.stream_files, indent+1)}'
		s += f'\n	* zlibs = {self.fmt_member(self.zlibs, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
