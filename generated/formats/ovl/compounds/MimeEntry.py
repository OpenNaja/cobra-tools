from generated.formats.ovl.compounds.Triplet import Triplet


from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.basic import OffsetString


class MimeEntry(BaseStruct):

	"""
	Description of one mime type or file class.
	Inside the archive not the stored mime hash is used but the extension hash, has to be generated, eg. djb2("bani") == 2090104799
	"""

	__name__ = 'MimeEntry'

	_import_key = 'ovl.compounds.MimeEntry'
	allow_np = True

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.name = 0
		self.zero_0 = 0

		# hash of this mime, changes with mime version; not used anywhere else in the ovl
		self.mime_hash = 0

		# usually increments with game
		self.mime_version = 0

		# Id of this class type. Later in the file there is a reference to this Id; offset into FileEntry list in number of files
		self.file_index_offset = 0

		# Number of entries of this class in the file.; from 'file index offset', this many files belong to this file extension
		self.file_count = 0
		self.zero_1 = 0

		# constant per mime, grab this many triplets
		self.triplet_count = 0

		# index into triplets list
		self.triplet_offset = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('name', OffsetString, (None, None), (False, None), None),
		('zero_0', Uint, (0, None), (False, 0), None),
		('mime_hash', Uint, (0, None), (False, None), True),
		('mime_version', Uint, (0, None), (False, None), None),
		('file_index_offset', Uint, (0, None), (False, None), None),
		('file_count', Uint, (0, None), (False, None), None),
		('zero_1', Uint, (0, None), (False, None), True),
		('triplet_count', Uint, (0, None), (False, None), True),
		('triplet_offset', Uint, (0, None), (False, None), True),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'name', OffsetString, (instance.context.names, None), (False, None)
		yield 'zero_0', Uint, (0, None), (False, 0)
		if instance.context.version >= 17:
			yield 'mime_hash', Uint, (0, None), (False, None)
		yield 'mime_version', Uint, (0, None), (False, None)
		yield 'file_index_offset', Uint, (0, None), (False, None)
		yield 'file_count', Uint, (0, None), (False, None)
		if instance.context.version <= 15:
			yield 'zero_1', Uint, (0, None), (False, None)
		if instance.context.version >= 20:
			yield 'triplet_count', Uint, (0, None), (False, None)
			yield 'triplet_offset', Uint, (0, None), (False, None)

	def update_constants(self, ovl):
		"""Update the constants"""
		self.name = ovl.get_mime(self.ext, "name")
		self.mime_hash = ovl.get_mime(self.ext, "hash")
		self.mime_version = ovl.get_mime(self.ext, "version")
		triplet_grab = ovl.get_mime(self.ext, "triplets")
		self.triplet_offset = len(ovl.triplets)
		self.triplet_count = len(triplet_grab)
		for triplet in triplet_grab:
			trip = Triplet(self.context)
			trip.a, trip.b, trip.c = triplet
			ovl.triplets.append(trip)

