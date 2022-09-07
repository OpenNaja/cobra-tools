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
		self.reserved = Array(self.context, 0, None, (0,), Uint)

		# Name buffer for assets and file mime types.
		self.names = ZStringBuffer(self.context, self.len_names, None)

		# used in DLA
		self.names_pad = Array(self.context, 0, None, (0,), Ubyte)

		# Array of MimeEntry objects that represent a mime type (file extension) each.
		self.mimes = Array(self.context, 0, None, (0,), MimeEntry)

		# ?
		self.triplets = Array(self.context, 0, None, (0,), Triplet)

		# ?
		self.triplets_pad = PadAlign(self.context, 4, self.triplets)

		# Array of FileEntry objects.
		self.files = Array(self.context, 0, None, (0,), FileEntry)

		# Name buffer for archives, usually will be STATIC followed by any OVS names
		self.archive_names = ZStringBuffer(self.context, self.len_archive_names, None)

		# Array of ArchiveEntry objects.
		self.archives = Array(self.context, 0, None, (0,), ArchiveEntry)

		# Array of IncludedOvl objects.
		self.included_ovls = Array(self.context, 0, None, (0,), IncludedOvl)

		# aka InstancesArray of DependencyEntry objects.
		self.dependencies = Array(self.context, 0, None, (0,), DependencyEntry)

		# Array of AuxEntry objects.
		self.aux_entries = Array(self.context, 0, None, (0,), AuxEntry)

		# after aux in ZTUAC and PC
		self.dependencies = Array(self.context, 0, None, (0,), DependencyEntry)

		# Array of StreamEntry objects.
		self.stream_files = Array(self.context, 0, None, (0,), StreamEntry)

		# repeats by archive count
		self.zlibs = Array(self.context, 0, None, (0,), ZlibInfo)
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
		self.mimes = Array(self.context, 0, None, (self.num_mimes,), MimeEntry)
		if self.context.version >= 20:
			self.triplets = Array(self.context, 0, None, (self.num_triplets,), Triplet)
			self.triplets_pad = PadAlign(self.context, 4, self.triplets)
		self.files = Array(self.context, 0, None, (self.num_files,), FileEntry)
		self.archive_names = ZStringBuffer(self.context, self.len_archive_names, None)
		self.archives = Array(self.context, 0, None, (self.num_archives,), ArchiveEntry)
		self.included_ovls = Array(self.context, 0, None, (self.num_included_ovls,), IncludedOvl)
		if self.context.version >= 19:
			self.dependencies = Array(self.context, 0, None, (self.num_dependencies,), DependencyEntry)
		self.aux_entries = Array(self.context, 0, None, (self.num_aux_entries,), AuxEntry)
		if self.context.version <= 18:
			self.dependencies = Array(self.context, 0, None, (self.num_dependencies,), DependencyEntry)
		self.stream_files = Array(self.context, 0, None, (self.num_stream_files,), StreamEntry)
		self.zlibs = Array(self.context, 0, None, (self.num_archives,), ZlibInfo)

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
		Array.to_stream(stream, instance.reserved, Uint)
		ZStringBuffer.to_stream(stream, instance.names)
		if instance.context.version <= 15:
			Array.to_stream(stream, instance.names_pad, Ubyte)
		Array.to_stream(stream, instance.mimes, MimeEntry)
		if instance.context.version >= 20:
			Array.to_stream(stream, instance.triplets, Triplet)
			PadAlign.to_stream(stream, instance.triplets_pad)
		Array.to_stream(stream, instance.files, FileEntry)
		ZStringBuffer.to_stream(stream, instance.archive_names)
		Array.to_stream(stream, instance.archives, ArchiveEntry)
		Array.to_stream(stream, instance.included_ovls, IncludedOvl)
		if instance.context.version >= 19:
			Array.to_stream(stream, instance.dependencies, DependencyEntry)
		Array.to_stream(stream, instance.aux_entries, AuxEntry)
		if instance.context.version <= 18:
			Array.to_stream(stream, instance.dependencies, DependencyEntry)
		Array.to_stream(stream, instance.stream_files, StreamEntry)
		Array.to_stream(stream, instance.zlibs, ZlibInfo)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
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
		yield 'reserved', Array, (0, None, (12,), Uint), (False, None)
		yield 'names', ZStringBuffer, (instance.len_names, None), (False, None)
		if instance.context.version <= 15:
			yield 'names_pad', Array, (0, None, ((16 - (instance.len_names % 16)) % 16,), Ubyte), (False, None)
		yield 'mimes', Array, (0, None, (instance.num_mimes,), MimeEntry), (False, None)
		if instance.context.version >= 20:
			yield 'triplets', Array, (0, None, (instance.num_triplets,), Triplet), (False, None)
			yield 'triplets_pad', PadAlign, (4, instance.triplets), (False, None)
		yield 'files', Array, (0, None, (instance.num_files,), FileEntry), (False, None)
		yield 'archive_names', ZStringBuffer, (instance.len_archive_names, None), (False, None)
		yield 'archives', Array, (0, None, (instance.num_archives,), ArchiveEntry), (False, None)
		yield 'included_ovls', Array, (0, None, (instance.num_included_ovls,), IncludedOvl), (False, None)
		if instance.context.version >= 19:
			yield 'dependencies', Array, (0, None, (instance.num_dependencies,), DependencyEntry), (False, None)
		yield 'aux_entries', Array, (0, None, (instance.num_aux_entries,), AuxEntry), (False, None)
		if instance.context.version <= 18:
			yield 'dependencies', Array, (0, None, (instance.num_dependencies,), DependencyEntry), (False, None)
		yield 'stream_files', Array, (0, None, (instance.num_stream_files,), StreamEntry), (False, None)
		yield 'zlibs', Array, (0, None, (instance.num_archives,), ZlibInfo), (False, None)

	def get_info_str(self, indent=0):
		return f'Header [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
