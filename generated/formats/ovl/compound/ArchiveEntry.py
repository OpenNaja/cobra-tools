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

		# starting index of file entries
		self.ovs_file_offset = 0

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

		# ?
		self.zeros_3 = 0

		# byte offset, cumulative size of all pools preceding this archive
		self.pools_start = 0

		# byte offset, sum of the archives header entry data blocks + the pools_start
		self.pools_end = 0

		# Seemingly unused, can be zeroed without effect ingame in JWE
		self.ovs_offset = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.offset = 0
		self.pools_offset = 0
		self.ovs_file_offset = 0
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
		self.zeros_3 = 0
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
		instance.ovs_file_offset = stream.read_uint()
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
		instance.uncompressed_size = stream.read_uint()
		instance.zeros_3 = stream.read_uint()
		instance.pools_start = stream.read_uint()
		instance.pools_end = stream.read_uint()
		instance.ovs_offset = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.offset)
		stream.write_uint(instance.pools_offset)
		stream.write_uint(instance.ovs_file_offset)
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
		stream.write_uint(instance.uncompressed_size)
		stream.write_uint(instance.zeros_3)
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

	def get_info_str(self):
		return f'ArchiveEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* pools_offset = {self.pools_offset.__repr__()}'
		s += f'\n	* ovs_file_offset = {self.ovs_file_offset.__repr__()}'
		s += f'\n	* num_pools = {self.num_pools.__repr__()}'
		s += f'\n	* num_datas = {self.num_datas.__repr__()}'
		s += f'\n	* num_pool_groups = {self.num_pool_groups.__repr__()}'
		s += f'\n	* num_buffer_groups = {self.num_buffer_groups.__repr__()}'
		s += f'\n	* num_buffers = {self.num_buffers.__repr__()}'
		s += f'\n	* num_fragments = {self.num_fragments.__repr__()}'
		s += f'\n	* num_files = {self.num_files.__repr__()}'
		s += f'\n	* read_start = {self.read_start.__repr__()}'
		s += f'\n	* set_data_size = {self.set_data_size.__repr__()}'
		s += f'\n	* compressed_size = {self.compressed_size.__repr__()}'
		s += f'\n	* uncompressed_size = {self.uncompressed_size.__repr__()}'
		s += f'\n	* zeros_3 = {self.zeros_3.__repr__()}'
		s += f'\n	* pools_start = {self.pools_start.__repr__()}'
		s += f'\n	* pools_end = {self.pools_end.__repr__()}'
		s += f'\n	* ovs_offset = {self.ovs_offset.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
