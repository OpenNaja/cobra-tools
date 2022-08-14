from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort


class ArchiveEntry(BaseStruct):

	"""
	Description of one archive
	"""

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
		instance.offset = stream.read_uint()
		instance.pools_offset = stream.read_uint()
		instance.stream_files_offset = stream.read_uint()
		instance.num_pools = stream.read_uint()
		instance.num_datas = stream.read_ushort()
		instance.num_pool_groups = stream.read_ushort()
		instance.num_buffer_groups = stream.read_uint()
		instance.num_buffers = stream.read_uint()
		instance.num_fragments = stream.read_uint()
		instance.num_root_entries = stream.read_uint()
		instance.read_start = stream.read_uint()
		instance.set_data_size = stream.read_uint()
		instance.compressed_size = stream.read_uint()
		instance.uncompressed_size = stream.read_uint64()
		instance.pools_start = stream.read_uint()
		instance.pools_end = stream.read_uint()
		instance.ovs_offset = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.offset)
		stream.write_uint(instance.pools_offset)
		stream.write_uint(instance.stream_files_offset)
		stream.write_uint(instance.num_pools)
		stream.write_ushort(instance.num_datas)
		stream.write_ushort(instance.num_pool_groups)
		stream.write_uint(instance.num_buffer_groups)
		stream.write_uint(instance.num_buffers)
		stream.write_uint(instance.num_fragments)
		stream.write_uint(instance.num_root_entries)
		stream.write_uint(instance.read_start)
		stream.write_uint(instance.set_data_size)
		stream.write_uint(instance.compressed_size)
		stream.write_uint64(instance.uncompressed_size)
		stream.write_uint(instance.pools_start)
		stream.write_uint(instance.pools_end)
		stream.write_uint(instance.ovs_offset)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'offset', Uint, (0, None)
		yield 'pools_offset', Uint, (0, None)
		yield 'stream_files_offset', Uint, (0, None)
		yield 'num_pools', Uint, (0, None)
		yield 'num_datas', Ushort, (0, None)
		yield 'num_pool_groups', Ushort, (0, None)
		yield 'num_buffer_groups', Uint, (0, None)
		yield 'num_buffers', Uint, (0, None)
		yield 'num_fragments', Uint, (0, None)
		yield 'num_root_entries', Uint, (0, None)
		yield 'read_start', Uint, (0, None)
		yield 'set_data_size', Uint, (0, None)
		yield 'compressed_size', Uint, (0, None)
		yield 'uncompressed_size', Uint64, (0, None)
		yield 'pools_start', Uint, (0, None)
		yield 'pools_end', Uint, (0, None)
		yield 'ovs_offset', Uint, (0, None)

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
