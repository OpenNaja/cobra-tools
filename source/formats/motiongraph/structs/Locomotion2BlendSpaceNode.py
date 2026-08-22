# START_GLOBALS
from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct

# JWE3 widened this record from 16 to 24 bytes by inserting 8 unused bytes
# between anim_name and speed:
#
#     +0   anim_name    Pointer
#     +8   jwe3_gap     8 bytes, observed always zero, no relocation
#     +16  speed        float
#     +20  orientation  float
#
# JWE2 and JWE3 are indistinguishable by version: both are version 20,
# user_version 25108, version_flag 1, is_dev 0.  No vercond can separate them, so
# the game name carried on the context is the only available discriminator.
#
# Measured evidence:
#   JWE2 Pteranodon  24 nodes -> 384-byte allocation -> stride 16
#   JWE3 Acrocanthosaurus  10 nodes -> 240-byte allocation -> stride 24
#
# Reading JWE3 at the declared 16-byte stride mis-aligns the array and silently
# drops the anim_name of every record that does not land on a 24-byte boundary.
JWE3_GAME = "Jurassic World Evolution 3"

# END_GLOBALS


class Locomotion2BlendSpaceNode(MemStruct):

# START_CLASS

	# Class-level default so get_size() and set_defaults() work on an instance
	# that has not been read from a stream yet.
	jwe3_gap = 0

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from MemStruct._get_filtered_attribute_list(instance, include_abstract)
		yield 'anim_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		if getattr(instance.context, "game", None) == JWE3_GAME:
			yield 'jwe3_gap', name_type_map['Uint64'], (0, None), (False, None)
		yield 'speed', name_type_map['Float'], (0, None), (False, None)
		yield 'orientation', name_type_map['Float'], (0, None), (False, None)
