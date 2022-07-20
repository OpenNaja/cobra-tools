from source.formats.base.basic import fmt_member
from generated.formats.base.enum import UbyteEnum


class DdsTypeCoaster(UbyteEnum):

	"""
	maps the OVL's dds type to name of compression format
	"""
	# ZTUAC ele heights textures
	D_24_UNORM_S_8_UINT = 74
	# ?
	D_24_UNORM_S_8_UINT_B = 76
	BC_1_UNORM = 97
	BC_1_UNORM_SRGB = 98
	BC_2_UNORM = 99
	BC_2_UNORM_SRGB = 100
	BC_3_UNORM = 101
	BC_3_UNORM_SRGB = 102
	BC_4_UNORM = 103
	BC_4_SNORM = 104
	BC_5_UNORM = 105
	BC_5_SNORM = 106
	BC_4_UNORM_B = 121
	BC_7_UNORM = 126
	BC_7_UNORM_SRGB = 127
	ALL = 250
