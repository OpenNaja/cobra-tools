from generated.context import ContextReference


class Vector3:

	"""
	A vector in 3D space (x,y,z).
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# First coordinate.
		self.x = 0

		# Second coordinate.
		self.y = 0

		# Third coordinate.
		self.z = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.x = 0
		self.y = 0
		self.z = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.x = stream.read_float()
		self.y = stream.read_float()
		self.z = stream.read_float()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_float(self.x)
		stream.write_float(self.y)
		stream.write_float(self.z)

		self.io_size = stream.tell() - self.io_start

	def set(self, vec):
		if hasattr(vec, "x"):
			self.x = vec.x
			self.y = vec.y
			self.z = vec.z
		else:
			self.x, self.y, self.z = vec

	def __repr__(self):
		return "[ %6.3f %6.3f %6.3f ]" % (self.x, self.y, self.z)

