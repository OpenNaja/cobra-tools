import enum


class D3D10ResourceDimension(enum.IntEnum):

	"""
	An unsigned 32-bit integer. Identifies the type of resource being used.
	"""
	D3D10_RESOURCE_DIMENSION_UNKNOWN = 0
	D3D10_RESOURCE_DIMENSION_BUFFER = 1
	D3D10_RESOURCE_DIMENSION_TEXTURE1D = 2
	D3D10_RESOURCE_DIMENSION_TEXTURE2D = 3
	D3D10_RESOURCE_DIMENSION_TEXTURE3D = 4

	def read(self, stream):
		self._value_ = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self._value_)
