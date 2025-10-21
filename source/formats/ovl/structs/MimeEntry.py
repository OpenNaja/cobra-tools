# START_GLOBALS
from generated.formats.ovl.structs.Triplet import Triplet


# END_GLOBALS


class MimeEntry:

	# START_CLASS

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
