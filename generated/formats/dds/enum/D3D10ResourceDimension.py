from generated.base_enum import UintEnum


class D3D10ResourceDimension(UintEnum):

	"""
	An unsigned 32-bit integer. Identifies the type of resource being used.
	"""
	D3D10_RESOURCE_DIMENSION_UNKNOWN = 0
	D3D10_RESOURCE_DIMENSION_BUFFER = 1
	D3D10_RESOURCE_DIMENSION_TEXTURE1D = 2
	D3D10_RESOURCE_DIMENSION_TEXTURE2D = 3
	D3D10_RESOURCE_DIMENSION_TEXTURE3D = 4
