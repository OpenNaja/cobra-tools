from generated.context import ContextReference


class PoolGroup:

	"""
	Located at start of deflated archive stream
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Type of the pools that follow
		self.type = 0

		# Amount of pools of that type that follow the pool types block
		self.num_pools = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.type = 0
		self.num_pools = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.type = stream.read_ushort()
		self.num_pools = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_ushort(self.type)
		stream.write_ushort(self.num_pools)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'PoolGroup [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* type = {self.type.__repr__()}'
		s += f'\n	* num_pools = {self.num_pools.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
