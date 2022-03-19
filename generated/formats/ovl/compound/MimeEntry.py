
from generated.formats.ovl.compound.Triplet import Triplet
from generated.formats.ovl.versions import *
from hashes import constants_jwe, constants_pz, constants_jwe2


from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class MimeEntry:

	"""
	Description of one mime type or file class.
	Inside the archive not the stored mime hash is used but the extension hash, has to be generated, eg. djb("bani") == 2090104799
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# offset in the header's Names block
		self.offset = 0

		# usually zero
		self.unknown = 0

		# changes with game version; hash of this file extension; same across all files, but not used anywhere else in the archive
		self.mime_hash = 0

		# usually increments with game
		self.mime_version = 0

		# Id of this class type. Later in the file there is a reference to this Id; offset into FileEntry list in number of files
		self.file_index_offset = 0

		# Number of entries of this class in the file.; from 'file index offset', this many files belong to this file extension
		self.file_count = 0

		# constant per mime, grab this many triplets
		self.triplet_count = 0

		# index into triplets list
		self.triplet_offset = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.offset = 0
		self.unknown = 0
		self.mime_hash = 0
		self.mime_version = 0
		self.file_index_offset = 0
		self.file_count = 0
		if self.context.version >= 20:
			self.triplet_count = 0
		if self.context.version >= 20:
			self.triplet_offset = 0

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
		instance.unknown = stream.read_uint()
		instance.mime_hash = stream.read_uint()
		instance.mime_version = stream.read_uint()
		instance.context.mime_version = instance.mime_version
		instance.file_index_offset = stream.read_uint()
		instance.file_count = stream.read_uint()
		if instance.context.version >= 20:
			instance.triplet_count = stream.read_uint()
			instance.triplet_offset = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.offset)
		stream.write_uint(instance.unknown)
		stream.write_uint(instance.mime_hash)
		stream.write_uint(instance.mime_version)
		stream.write_uint(instance.file_index_offset)
		stream.write_uint(instance.file_count)
		if instance.context.version >= 20:
			stream.write_uint(instance.triplet_count)
			stream.write_uint(instance.triplet_offset)

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
		return f'MimeEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* unknown = {fmt_member(self.unknown, indent+1)}'
		s += f'\n	* mime_hash = {fmt_member(self.mime_hash, indent+1)}'
		s += f'\n	* mime_version = {fmt_member(self.mime_version, indent+1)}'
		s += f'\n	* file_index_offset = {fmt_member(self.file_index_offset, indent+1)}'
		s += f'\n	* file_count = {fmt_member(self.file_count, indent+1)}'
		s += f'\n	* triplet_count = {fmt_member(self.triplet_count, indent+1)}'
		s += f'\n	* triplet_offset = {fmt_member(self.triplet_offset, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

	def update_constants(self, ovl):
		"""Update the constants"""

		# update offset using the name buffer
		if is_jwe(ovl):
			constants = constants_jwe
		elif is_pz(ovl) or is_pz16(ovl):
			constants = constants_pz
		elif is_jwe2(ovl):
			constants = constants_jwe2
		else:
			raise ValueError(f"Unsupported game {get_game(ovl)}")
		self.name = constants.mimes_name[self.ext]
		self.mime_hash = constants.mimes_mime_hash[self.ext]
		self.mime_version = constants.mimes_mime_version[self.ext]

		# update triplets
		if is_pz16(ovl) or is_jwe2(ovl):
			triplet_grab = constants.mimes_triplets[self.ext]
			self.triplet_offset = len(ovl.triplets)
			self.triplet_count = len(triplet_grab)
			for triplet in triplet_grab:
				trip = Triplet(self.context)
				trip.a, trip.b, trip.c = triplet
				ovl.triplets.append(trip)

