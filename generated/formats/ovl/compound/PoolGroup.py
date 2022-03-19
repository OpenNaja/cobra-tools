from source.formats.base.basic import fmt_member
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
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		instance.type = stream.read_ushort()
		instance.num_pools = stream.read_ushort()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_ushort(instance.type)
		stream.write_ushort(instance.num_pools)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'PoolGroup [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* type = {fmt_member(self.type, indent+1)}'
		s += f'\n	* num_pools = {fmt_member(self.num_pools, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
