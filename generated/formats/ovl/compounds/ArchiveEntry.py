from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort


class ArchiveEntry(BaseStruct):

	"""
	Description of one archive
	"""

	__name__ = 'ArchiveEntry'

	_import_path = 'generated.formats.ovl.compounds.ArchiveEntry'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# offset in the ovl's Archive Names block
		self.offset = 0

		# starting index in ovl list of pools, this archive's pools continue for num_pools
		self.pools_offset = 0

		# starting index into ovl.stream_files
		self.stream_files_offset = 0

		# Total amount of pools in this archive; sum of all PoolGroup.num_pools
		self.num_pools = 0

		# Amount of Data Entries
		self.num_datas = 0

		# Amount of PoolGroup objects at start of this deflated archive.
		self.num_pool_groups = 0

		# used in pz 1.6
		self.num_buffer_groups = 0

		# Amount of buffers in the archive
		self.num_buffers = 0

		# Amount of Fragments in the archive
		self.num_fragments = 0

		# Number of files in the archive
		self.num_root_entries = 0

		# Seek to pos to get zlib header for this archive
		self.read_start = 0

		# size of the set and asset entry data
		self.set_data_size = 0

		# size of the compressed data for this archive
		self.compressed_size = 0

		# size of the uncompressed data for this archive
		self.uncompressed_size = 0

		# byte offset, cumulative size of all pools preceding this archive
		self.pools_start = 0

		# byte offset, pools_start + sum of this archive's pools' sizes
		self.pools_end = 0

		# Seemingly unused, can be zeroed without effect ingame in JWE
		self.ovs_offset = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.offset = 0
		self.pools_offset = 0
		self.stream_files_offset = 0
		self.num_pools = 0
		self.num_datas = 0
		self.num_pool_groups = 0
		self.num_buffer_groups = 0
		self.num_buffers = 0
		self.num_fragments = 0
		self.num_root_entries = 0
		self.read_start = 0
		self.set_data_size = 0
		self.compressed_size = 0
		self.uncompressed_size = 0
		self.pools_start = 0
		self.pools_end = 0
		self.ovs_offset = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.offset = Uint.from_stream(stream, instance.context, 0, None)
		instance.pools_offset = Uint.from_stream(stream, instance.context, 0, None)
		instance.stream_files_offset = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_pools = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_datas = Ushort.from_stream(stream, instance.context, 0, None)
		instance.num_pool_groups = Ushort.from_stream(stream, instance.context, 0, None)
		instance.num_buffer_groups = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_buffers = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_fragments = Uint.from_stream(stream, instance.context, 0, None)
		instance.num_root_entries = Uint.from_stream(stream, instance.context, 0, None)
		instance.read_start = Uint.from_stream(stream, instance.context, 0, None)
		instance.set_data_size = Uint.from_stream(stream, instance.context, 0, None)
		instance.compressed_size = Uint.from_stream(stream, instance.context, 0, None)
		instance.uncompressed_size = Uint64.from_stream(stream, instance.context, 0, None)
		instance.pools_start = Uint.from_stream(stream, instance.context, 0, None)
		instance.pools_end = Uint.from_stream(stream, instance.context, 0, None)
		instance.ovs_offset = Uint.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.offset)
		Uint.to_stream(stream, instance.pools_offset)
		Uint.to_stream(stream, instance.stream_files_offset)
		Uint.to_stream(stream, instance.num_pools)
		Ushort.to_stream(stream, instance.num_datas)
		Ushort.to_stream(stream, instance.num_pool_groups)
		Uint.to_stream(stream, instance.num_buffer_groups)
		Uint.to_stream(stream, instance.num_buffers)
		Uint.to_stream(stream, instance.num_fragments)
		Uint.to_stream(stream, instance.num_root_entries)
		Uint.to_stream(stream, instance.read_start)
		Uint.to_stream(stream, instance.set_data_size)
		Uint.to_stream(stream, instance.compressed_size)
		Uint64.to_stream(stream, instance.uncompressed_size)
		Uint.to_stream(stream, instance.pools_start)
		Uint.to_stream(stream, instance.pools_end)
		Uint.to_stream(stream, instance.ovs_offset)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'offset', Uint, (0, None), (False, None)
		yield 'pools_offset', Uint, (0, None), (False, None)
		yield 'stream_files_offset', Uint, (0, None), (False, None)
		yield 'num_pools', Uint, (0, None), (False, None)
		yield 'num_datas', Ushort, (0, None), (False, None)
		yield 'num_pool_groups', Ushort, (0, None), (False, None)
		yield 'num_buffer_groups', Uint, (0, None), (False, None)
		yield 'num_buffers', Uint, (0, None), (False, None)
		yield 'num_fragments', Uint, (0, None), (False, None)
		yield 'num_root_entries', Uint, (0, None), (False, None)
		yield 'read_start', Uint, (0, None), (False, None)
		yield 'set_data_size', Uint, (0, None), (False, None)
		yield 'compressed_size', Uint, (0, None), (False, None)
		yield 'uncompressed_size', Uint64, (0, None), (False, None)
		yield 'pools_start', Uint, (0, None), (False, None)
		yield 'pools_end', Uint, (0, None), (False, None)
		yield 'ovs_offset', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'ArchiveEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
