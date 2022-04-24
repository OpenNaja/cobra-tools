from source.formats.base.basic import fmt_member
import numpy
from generated.array import Array
from generated.formats.base.compound.PadAlign import PadAlign
from generated.formats.base.compound.ZStringBuffer import ZStringBuffer
from generated.formats.ovl.compound.ArchiveEntry import ArchiveEntry
from generated.formats.ovl.compound.AuxEntry import AuxEntry
from generated.formats.ovl.compound.DependencyEntry import DependencyEntry
from generated.formats.ovl.compound.FileEntry import FileEntry
from generated.formats.ovl.compound.IncludedOvl import IncludedOvl
from generated.formats.ovl.compound.MimeEntry import MimeEntry
from generated.formats.ovl.compound.StreamEntry import StreamEntry
from generated.formats.ovl.compound.Triplet import Triplet
from generated.formats.ovl.compound.ZlibInfo import ZlibInfo
from generated.formats.ovl_base.compound.GenericHeader import GenericHeader


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
		self.reserved = numpy.zeros((12,), dtype=numpy.dtype('uint32'))

		# Name buffer for assets and file mime types.
		self.names = ZStringBuffer(self.context, self.len_names, None)

		# Array of MimeEntry objects that represent a mime type (file extension) each.
		self.mimes = Array((self.num_mimes,), MimeEntry, self.context, 0, None)

		# ?
		self.triplets = Array((self.num_triplets,), Triplet, self.context, 0, None)

		# ?
		self.triplets_pad = PadAlign(self.context, 4, self.triplets)

		# Array of FileEntry objects.
		self.files = Array((self.num_files,), FileEntry, self.context, 0, None)

		# Name buffer for archives, usually will be STATIC followed by any OVS names
		self.archive_names = ZStringBuffer(self.context, self.len_archive_names, None)

		# Array of ArchiveEntry objects.
		self.archives = Array((self.num_archives,), ArchiveEntry, self.context, 0, None)

		# Array of IncludedOvl objects.
		self.included_ovls = Array((self.num_included_ovls,), IncludedOvl, self.context, 0, None)

		# aka InstancesArray of DependencyEntry objects.
		self.dependencies = Array((self.num_dependencies,), DependencyEntry, self.context, 0, None)

		# Array of AuxEntry objects.
		self.aux_entries = Array((self.num_aux_entries,), AuxEntry, self.context, 0, None)

		# after aux in ZTUAC and PC
		self.dependencies = Array((self.num_dependencies,), DependencyEntry, self.context, 0, None)

		# Array of StreamEntry objects.
		self.stream_files = Array((self.num_files_ovs,), StreamEntry, self.context, 0, None)

		# repeats by archive count
		self.zlibs = Array((self.num_archives,), ZlibInfo, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
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
		self.num_files_ovs = 0
		self.ztuac_unk_0 = 0
		self.ztuac_unk_1 = 0
		self.ztuac_unk_2 = 0
		self.len_archive_names = 0
		self.num_files_3 = 0
		self.len_type_names = 0
		self.num_triplets = 0
		self.reserved = numpy.zeros((12,), dtype=numpy.dtype('uint32'))
		self.names = ZStringBuffer(self.context, self.len_names, None)
		self.mimes = Array((self.num_mimes,), MimeEntry, self.context, 0, None)
		if self.context.version >= 20:
			self.triplets = Array((self.num_triplets,), Triplet, self.context, 0, None)
		if self.context.version >= 20:
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
		self.stream_files = Array((self.num_files_ovs,), StreamEntry, self.context, 0, None)
		self.zlibs = Array((self.num_archives,), ZlibInfo, self.context, 0, None)

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
		instance.lod_depth = stream.read_uint()
		instance.len_names = stream.read_uint()
		instance.zero_2 = stream.read_uint()
		instance.num_aux_entries = stream.read_uint()
		instance.num_included_ovls = stream.read_ushort()
		instance.num_mimes = stream.read_ushort()
		instance.num_files = stream.read_uint()
		instance.num_files_2 = stream.read_uint()
		instance.num_dependencies = stream.read_uint()
		instance.num_archives = stream.read_uint()
		instance.num_pool_groups = stream.read_uint()
		instance.num_pools = stream.read_uint()
		instance.num_datas = stream.read_uint()
		instance.num_buffers = stream.read_uint()
		instance.num_files_ovs = stream.read_uint()
		instance.ztuac_unk_0 = stream.read_uint()
		instance.ztuac_unk_1 = stream.read_uint()
		instance.ztuac_unk_2 = stream.read_uint()
		instance.len_archive_names = stream.read_uint()
		instance.num_files_3 = stream.read_uint()
		instance.len_type_names = stream.read_uint()
		instance.num_triplets = stream.read_uint()
		instance.reserved = stream.read_uints((12,))
		instance.names = ZStringBuffer.from_stream(stream, instance.context, instance.len_names, None)
		instance.mimes = Array.from_stream(stream, (instance.num_mimes,), MimeEntry, instance.context, 0, None)
		if instance.context.version >= 20:
			instance.triplets = Array.from_stream(stream, (instance.num_triplets,), Triplet, instance.context, 0, None)
			instance.triplets_pad = PadAlign.from_stream(stream, instance.context, 4, instance.triplets)
		instance.files = Array.from_stream(stream, (instance.num_files,), FileEntry, instance.context, 0, None)
		instance.archive_names = ZStringBuffer.from_stream(stream, instance.context, instance.len_archive_names, None)
		instance.archives = Array.from_stream(stream, (instance.num_archives,), ArchiveEntry, instance.context, 0, None)
		instance.included_ovls = Array.from_stream(stream, (instance.num_included_ovls,), IncludedOvl, instance.context, 0, None)
		if instance.context.version >= 19:
			instance.dependencies = Array.from_stream(stream, (instance.num_dependencies,), DependencyEntry, instance.context, 0, None)
		instance.aux_entries = Array.from_stream(stream, (instance.num_aux_entries,), AuxEntry, instance.context, 0, None)
		if instance.context.version <= 18:
			instance.dependencies = Array.from_stream(stream, (instance.num_dependencies,), DependencyEntry, instance.context, 0, None)
		instance.stream_files = Array.from_stream(stream, (instance.num_files_ovs,), StreamEntry, instance.context, 0, None)
		instance.zlibs = Array.from_stream(stream, (instance.num_archives,), ZlibInfo, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.lod_depth)
		stream.write_uint(instance.len_names)
		stream.write_uint(instance.zero_2)
		stream.write_uint(instance.num_aux_entries)
		stream.write_ushort(instance.num_included_ovls)
		stream.write_ushort(instance.num_mimes)
		stream.write_uint(instance.num_files)
		stream.write_uint(instance.num_files_2)
		stream.write_uint(instance.num_dependencies)
		stream.write_uint(instance.num_archives)
		stream.write_uint(instance.num_pool_groups)
		stream.write_uint(instance.num_pools)
		stream.write_uint(instance.num_datas)
		stream.write_uint(instance.num_buffers)
		stream.write_uint(instance.num_files_ovs)
		stream.write_uint(instance.ztuac_unk_0)
		stream.write_uint(instance.ztuac_unk_1)
		stream.write_uint(instance.ztuac_unk_2)
		stream.write_uint(instance.len_archive_names)
		stream.write_uint(instance.num_files_3)
		stream.write_uint(instance.len_type_names)
		stream.write_uint(instance.num_triplets)
		stream.write_uints(instance.reserved)
		ZStringBuffer.to_stream(stream, instance.names)
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
		Array.to_stream(stream, instance.stream_files, (instance.num_files_ovs,), StreamEntry, instance.context, 0, None)
		Array.to_stream(stream, instance.zlibs, (instance.num_archives,), ZlibInfo, instance.context, 0, None)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'Header [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* lod_depth = {fmt_member(self.lod_depth, indent+1)}'
		s += f'\n	* len_names = {fmt_member(self.len_names, indent+1)}'
		s += f'\n	* zero_2 = {fmt_member(self.zero_2, indent+1)}'
		s += f'\n	* num_aux_entries = {fmt_member(self.num_aux_entries, indent+1)}'
		s += f'\n	* num_included_ovls = {fmt_member(self.num_included_ovls, indent+1)}'
		s += f'\n	* num_mimes = {fmt_member(self.num_mimes, indent+1)}'
		s += f'\n	* num_files = {fmt_member(self.num_files, indent+1)}'
		s += f'\n	* num_files_2 = {fmt_member(self.num_files_2, indent+1)}'
		s += f'\n	* num_dependencies = {fmt_member(self.num_dependencies, indent+1)}'
		s += f'\n	* num_archives = {fmt_member(self.num_archives, indent+1)}'
		s += f'\n	* num_pool_groups = {fmt_member(self.num_pool_groups, indent+1)}'
		s += f'\n	* num_pools = {fmt_member(self.num_pools, indent+1)}'
		s += f'\n	* num_datas = {fmt_member(self.num_datas, indent+1)}'
		s += f'\n	* num_buffers = {fmt_member(self.num_buffers, indent+1)}'
		s += f'\n	* num_files_ovs = {fmt_member(self.num_files_ovs, indent+1)}'
		s += f'\n	* ztuac_unk_0 = {fmt_member(self.ztuac_unk_0, indent+1)}'
		s += f'\n	* ztuac_unk_1 = {fmt_member(self.ztuac_unk_1, indent+1)}'
		s += f'\n	* ztuac_unk_2 = {fmt_member(self.ztuac_unk_2, indent+1)}'
		s += f'\n	* len_archive_names = {fmt_member(self.len_archive_names, indent+1)}'
		s += f'\n	* num_files_3 = {fmt_member(self.num_files_3, indent+1)}'
		s += f'\n	* len_type_names = {fmt_member(self.len_type_names, indent+1)}'
		s += f'\n	* num_triplets = {fmt_member(self.num_triplets, indent+1)}'
		s += f'\n	* reserved = {fmt_member(self.reserved, indent+1)}'
		s += f'\n	* names = {fmt_member(self.names, indent+1)}'
		s += f'\n	* mimes = {fmt_member(self.mimes, indent+1)}'
		s += f'\n	* triplets = {fmt_member(self.triplets, indent+1)}'
		s += f'\n	* triplets_pad = {fmt_member(self.triplets_pad, indent+1)}'
		s += f'\n	* files = {fmt_member(self.files, indent+1)}'
		s += f'\n	* archive_names = {fmt_member(self.archive_names, indent+1)}'
		s += f'\n	* archives = {fmt_member(self.archives, indent+1)}'
		s += f'\n	* included_ovls = {fmt_member(self.included_ovls, indent+1)}'
		s += f'\n	* dependencies = {fmt_member(self.dependencies, indent+1)}'
		s += f'\n	* aux_entries = {fmt_member(self.aux_entries, indent+1)}'
		s += f'\n	* dependencies = {fmt_member(self.dependencies, indent+1)}'
		s += f'\n	* stream_files = {fmt_member(self.stream_files, indent+1)}'
		s += f'\n	* zlibs = {fmt_member(self.zlibs, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
