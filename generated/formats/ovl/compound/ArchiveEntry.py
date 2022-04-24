from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class ArchiveEntry:

	"""
	Description of one archive
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

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
		self.num_files = 0

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
		self.offset = 0
		self.pools_offset = 0
		self.stream_files_offset = 0
		self.num_pools = 0
		self.num_datas = 0
		self.num_pool_groups = 0
		self.num_buffer_groups = 0
		self.num_buffers = 0
		self.num_fragments = 0
		self.num_files = 0
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
		instance.offset = stream.read_uint()
		instance.pools_offset = stream.read_uint()
		instance.stream_files_offset = stream.read_uint()
		instance.num_pools = stream.read_uint()
		instance.num_datas = stream.read_ushort()
		instance.num_pool_groups = stream.read_ushort()
		instance.num_buffer_groups = stream.read_uint()
		instance.num_buffers = stream.read_uint()
		instance.num_fragments = stream.read_uint()
		instance.num_files = stream.read_uint()
		instance.read_start = stream.read_uint()
		instance.set_data_size = stream.read_uint()
		instance.compressed_size = stream.read_uint()
		instance.uncompressed_size = stream.read_uint64()
		instance.pools_start = stream.read_uint()
		instance.pools_end = stream.read_uint()
		instance.ovs_offset = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.offset)
		stream.write_uint(instance.pools_offset)
		stream.write_uint(instance.stream_files_offset)
		stream.write_uint(instance.num_pools)
		stream.write_ushort(instance.num_datas)
		stream.write_ushort(instance.num_pool_groups)
		stream.write_uint(instance.num_buffer_groups)
		stream.write_uint(instance.num_buffers)
		stream.write_uint(instance.num_fragments)
		stream.write_uint(instance.num_files)
		stream.write_uint(instance.read_start)
		stream.write_uint(instance.set_data_size)
		stream.write_uint(instance.compressed_size)
		stream.write_uint64(instance.uncompressed_size)
		stream.write_uint(instance.pools_start)
		stream.write_uint(instance.pools_end)
		stream.write_uint(instance.ovs_offset)

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
		return f'ArchiveEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* pools_offset = {fmt_member(self.pools_offset, indent+1)}'
		s += f'\n	* stream_files_offset = {fmt_member(self.stream_files_offset, indent+1)}'
		s += f'\n	* num_pools = {fmt_member(self.num_pools, indent+1)}'
		s += f'\n	* num_datas = {fmt_member(self.num_datas, indent+1)}'
		s += f'\n	* num_pool_groups = {fmt_member(self.num_pool_groups, indent+1)}'
		s += f'\n	* num_buffer_groups = {fmt_member(self.num_buffer_groups, indent+1)}'
		s += f'\n	* num_buffers = {fmt_member(self.num_buffers, indent+1)}'
		s += f'\n	* num_fragments = {fmt_member(self.num_fragments, indent+1)}'
		s += f'\n	* num_files = {fmt_member(self.num_files, indent+1)}'
		s += f'\n	* read_start = {fmt_member(self.read_start, indent+1)}'
		s += f'\n	* set_data_size = {fmt_member(self.set_data_size, indent+1)}'
		s += f'\n	* compressed_size = {fmt_member(self.compressed_size, indent+1)}'
		s += f'\n	* uncompressed_size = {fmt_member(self.uncompressed_size, indent+1)}'
		s += f'\n	* pools_start = {fmt_member(self.pools_start, indent+1)}'
		s += f'\n	* pools_end = {fmt_member(self.pools_end, indent+1)}'
		s += f'\n	* ovs_offset = {fmt_member(self.ovs_offset, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
