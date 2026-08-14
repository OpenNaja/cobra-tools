# START_GLOBALS
import struct

from generated.base_struct import BaseStruct

# END_GLOBALS


class AclPaddingReader(BaseStruct):

	# START_CLASS

	ACL_TAG = b"\x11\xac\x11\xac"

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		mani_info = instance.arg.arg
		origin = stream.tell()
		data = stream.read()
		search_from = 8
		while True:
			tag_offset = data.find(cls.ACL_TAG, search_from)
			if tag_offset < 0:
				raise BufferError(f"Could not find ACL transform stream after {origin}")
			blob_offset = tag_offset - 8
			if blob_offset >= 0 and tag_offset + 20 <= len(data):
				size = struct.unpack_from("<I", data, blob_offset)[0]
				version, _algorithm, track_type = struct.unpack_from("<HBB", data, tag_offset + 4)
				num_tracks, num_samples = struct.unpack_from("<II", data, tag_offset + 8)
				if (
					size >= 32
					and blob_offset + size <= len(data)
					and version == 10
					and track_type == 12
					and num_tracks == mani_info.target_bone_count
					and num_samples in (mani_info.frame_count, mani_info.frame_count - 1)
				):
					instance.data = data[:blob_offset]
					stream.seek(origin + blob_offset)
					instance.io_size = blob_offset
					return
			search_from = tag_offset + 1

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		stream.write(instance.data)
		instance.io_size = len(instance.data)

	@classmethod
	def get_fields_str(cls, instance, indent=0):
		return f"ACL prefix bytes: {len(instance.data)}"
