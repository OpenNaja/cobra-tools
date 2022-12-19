from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.basic import OffsetString


class ArchiveEntry(BaseStruct):

	"""
	Description of one archive
	"""

	__name__ = 'ArchiveEntry'

	_import_key = 'ovl.compounds.ArchiveEntry'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.name = 0

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

	_attribute_list = BaseStruct._attribute_list + [
		('name', OffsetString, (None, None), (False, None), None),
		('pools_offset', Uint, (0, None), (False, None), None),
		('stream_files_offset', Uint, (0, None), (False, None), None),
		('num_pools', Uint, (0, None), (False, None), None),
		('num_datas', Ushort, (0, None), (False, None), None),
		('num_pool_groups', Ushort, (0, None), (False, None), None),
		('num_buffer_groups', Uint, (0, None), (False, None), None),
		('num_buffers', Uint, (0, None), (False, None), None),
		('num_fragments', Uint, (0, None), (False, None), None),
		('num_root_entries', Uint, (0, None), (False, None), None),
		('read_start', Uint, (0, None), (False, None), None),
		('set_data_size', Uint, (0, None), (False, None), None),
		('compressed_size', Uint, (0, None), (False, None), None),
		('uncompressed_size', Uint64, (0, None), (False, None), None),
		('pools_start', Uint, (0, None), (False, None), None),
		('pools_end', Uint, (0, None), (False, None), None),
		('ovs_offset', Uint, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'name', OffsetString, (instance.context.archive_names, None), (False, None)
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
