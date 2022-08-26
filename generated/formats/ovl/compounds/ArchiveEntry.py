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

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* offset = {self.fmt_member(self.offset, indent+1)}'
		s += f'\n	* pools_offset = {self.fmt_member(self.pools_offset, indent+1)}'
		s += f'\n	* stream_files_offset = {self.fmt_member(self.stream_files_offset, indent+1)}'
		s += f'\n	* num_pools = {self.fmt_member(self.num_pools, indent+1)}'
		s += f'\n	* num_datas = {self.fmt_member(self.num_datas, indent+1)}'
		s += f'\n	* num_pool_groups = {self.fmt_member(self.num_pool_groups, indent+1)}'
		s += f'\n	* num_buffer_groups = {self.fmt_member(self.num_buffer_groups, indent+1)}'
		s += f'\n	* num_buffers = {self.fmt_member(self.num_buffers, indent+1)}'
		s += f'\n	* num_fragments = {self.fmt_member(self.num_fragments, indent+1)}'
		s += f'\n	* num_root_entries = {self.fmt_member(self.num_root_entries, indent+1)}'
		s += f'\n	* read_start = {self.fmt_member(self.read_start, indent+1)}'
		s += f'\n	* set_data_size = {self.fmt_member(self.set_data_size, indent+1)}'
		s += f'\n	* compressed_size = {self.fmt_member(self.compressed_size, indent+1)}'
		s += f'\n	* uncompressed_size = {self.fmt_member(self.uncompressed_size, indent+1)}'
		s += f'\n	* pools_start = {self.fmt_member(self.pools_start, indent+1)}'
		s += f'\n	* pools_end = {self.fmt_member(self.pools_end, indent+1)}'
		s += f'\n	* ovs_offset = {self.fmt_member(self.ovs_offset, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
