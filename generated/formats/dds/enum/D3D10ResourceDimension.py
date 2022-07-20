from source.formats.base.basic import fmt_member
from generated.formats.dds.enum import UintEnum


class D3D10ResourceDimension(UintEnum):

	"""
	An unsigned 32-bit integer. Identifies the type of resource being used.
	"""
	D_3_D_10_RESOURCE_DIMENSION_UNKNOWN = 0
	D_3_D_10_RESOURCE_DIMENSION_BUFFER = 1
	D_3_D_10_RESOURCE_DIMENSION_TEXTURE_1_D = 2
	D_3_D_10_RESOURCE_DIMENSION_TEXTURE_2_D = 3
	D_3_D_10_RESOURCE_DIMENSION_TEXTURE_3_D = 4
