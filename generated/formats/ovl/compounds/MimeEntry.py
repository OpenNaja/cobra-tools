
from generated.formats.ovl.compounds.Triplet import Triplet
from generated.formats.ovl.versions import *
from hashes import constants_jwe, constants_pz, constants_jwe2, constants_pc, constants_dla


from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint


class MimeEntry(BaseStruct):

	"""
	Description of one mime type or file class.
	Inside the archive not the stored mime hash is used but the extension hash, has to be generated, eg. djb2("bani") == 2090104799
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

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
		super().set_defaults()
		self.offset = 0
		self.unknown = 0
		self.mime_hash = 0
		self.mime_version = 0
		self.file_index_offset = 0
		self.file_count = 0
		if self.context.version >= 20:
			self.triplet_count = 0
			self.triplet_offset = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.offset = Uint.from_stream(stream, instance.context, 0, None)
		instance.unknown = Uint.from_stream(stream, instance.context, 0, None)
		instance.mime_hash = Uint.from_stream(stream, instance.context, 0, None)
		instance.mime_version = Uint.from_stream(stream, instance.context, 0, None)
		instance.context.mime_version = instance.mime_version
		instance.file_index_offset = Uint.from_stream(stream, instance.context, 0, None)
		instance.file_count = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 20:
			instance.triplet_count = Uint.from_stream(stream, instance.context, 0, None)
			instance.triplet_offset = Uint.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.offset)
		Uint.to_stream(stream, instance.unknown)
		Uint.to_stream(stream, instance.mime_hash)
		Uint.to_stream(stream, instance.mime_version)
		Uint.to_stream(stream, instance.file_index_offset)
		Uint.to_stream(stream, instance.file_count)
		if instance.context.version >= 20:
			Uint.to_stream(stream, instance.triplet_count)
			Uint.to_stream(stream, instance.triplet_offset)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'offset', Uint, (0, None), (False, None)
		yield 'unknown', Uint, (0, None), (False, None)
		yield 'mime_hash', Uint, (0, None), (False, None)
		yield 'mime_version', Uint, (0, None), (False, None)
		yield 'file_index_offset', Uint, (0, None), (False, None)
		yield 'file_count', Uint, (0, None), (False, None)
		if instance.context.version >= 20:
			yield 'triplet_count', Uint, (0, None), (False, None)
			yield 'triplet_offset', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'MimeEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* offset = {self.fmt_member(self.offset, indent+1)}'
		s += f'\n	* unknown = {self.fmt_member(self.unknown, indent+1)}'
		s += f'\n	* mime_hash = {self.fmt_member(self.mime_hash, indent+1)}'
		s += f'\n	* mime_version = {self.fmt_member(self.mime_version, indent+1)}'
		s += f'\n	* file_index_offset = {self.fmt_member(self.file_index_offset, indent+1)}'
		s += f'\n	* file_count = {self.fmt_member(self.file_count, indent+1)}'
		s += f'\n	* triplet_count = {self.fmt_member(self.triplet_count, indent+1)}'
		s += f'\n	* triplet_offset = {self.fmt_member(self.triplet_offset, indent+1)}'
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
		elif is_pc(ovl):
			constants = constants_pc
		elif is_dla(ovl):
			constants = constants_dla
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

