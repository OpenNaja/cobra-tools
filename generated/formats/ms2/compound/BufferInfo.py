from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class BufferInfo:

	"""
	Fragment data describing a MS2 buffer giving the size of the whole vertex and tri buffer.
	ZTUAC: 64 bytes
	PC: 32 bytes
	JWE1: 48 bytes
	PZ old: 32 bytes?
	PZ1.6+ and JWE2: 56 bytes
	JWE2 Biosyn: 88 bytes, with 4 values, order of arrays in buffer is verts, tris, chunks_pos, chunks_size
	
	JWE and PC, 16 bytes of 00 padding
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.u_0 = 0
		self.u_1 = 0
		self.chunk_pos_size = 0
		self.chunk_pos_ptr = 0
		self.chunks_size = 0
		self.chunks_ptr = 0
		self.vertex_buffer_size = 0
		self.u_2 = 0
		self.u_3 = 0
		self.tris_buffer_size = 0
		self.u_4 = 0
		self.u_5 = 0
		self.u_6 = 0
		self.u_5 = 0

		# from start of tris buffer
		self.uv_buffer_size = 0
		self.u_6 = 0
		self.u_7 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if 32 <= self.context.version <= 47:
			self.u_0 = 0
		if 32 <= self.context.version <= 47:
			self.u_1 = 0
		if (self.context.version == 51) and self.context.biosyn:
			self.chunk_pos_size = 0
		if (self.context.version == 51) and self.context.biosyn:
			self.chunk_pos_ptr = 0
		if (self.context.version == 51) and self.context.biosyn:
			self.chunks_size = 0
		if (self.context.version == 51) and self.context.biosyn:
			self.chunks_ptr = 0
		self.vertex_buffer_size = 0
		self.u_2 = 0
		if self.context.version >= 48:
			self.u_3 = 0
		if not (self.context.version == 32):
			self.tris_buffer_size = 0
		if not (self.context.version == 32):
			self.u_4 = 0
		if self.context.version >= 48:
			self.u_5 = 0
		if self.context.version >= 48:
			self.u_6 = 0
		if self.context.version <= 13:
			self.u_5 = 0
		if self.context.version <= 13:
			self.uv_buffer_size = 0
		if self.context.version <= 13:
			self.u_6 = 0
		if self.context.version <= 13:
			self.u_7 = 0

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
		if 32 <= instance.context.version <= 47:
			instance.u_0 = stream.read_uint64()
			instance.u_1 = stream.read_uint64()
		if (instance.context.version == 51) and instance.context.biosyn:
			instance.chunk_pos_size = stream.read_uint64()
			instance.chunk_pos_ptr = stream.read_uint64()
		if (instance.context.version == 51) and instance.context.biosyn:
			instance.chunks_size = stream.read_uint64()
			instance.chunks_ptr = stream.read_uint64()
		instance.vertex_buffer_size = stream.read_uint64()
		instance.u_2 = stream.read_uint64()
		if instance.context.version >= 48:
			instance.u_3 = stream.read_uint64()
		if not (instance.context.version == 32):
			instance.tris_buffer_size = stream.read_uint64()
			instance.u_4 = stream.read_uint64()
		if instance.context.version >= 48:
			instance.u_5 = stream.read_uint64()
			instance.u_6 = stream.read_uint64()
		if instance.context.version <= 13:
			instance.u_5 = stream.read_uint64()
			instance.uv_buffer_size = stream.read_uint64()
		if instance.context.version <= 13:
			instance.u_6 = stream.read_uint64()
			instance.u_7 = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		if 32 <= instance.context.version <= 47:
			stream.write_uint64(instance.u_0)
			stream.write_uint64(instance.u_1)
		if (instance.context.version == 51) and instance.context.biosyn:
			stream.write_uint64(instance.chunk_pos_size)
			stream.write_uint64(instance.chunk_pos_ptr)
		if (instance.context.version == 51) and instance.context.biosyn:
			stream.write_uint64(instance.chunks_size)
			stream.write_uint64(instance.chunks_ptr)
		stream.write_uint64(instance.vertex_buffer_size)
		stream.write_uint64(instance.u_2)
		if instance.context.version >= 48:
			stream.write_uint64(instance.u_3)
		if not (instance.context.version == 32):
			stream.write_uint64(instance.tris_buffer_size)
			stream.write_uint64(instance.u_4)
		if instance.context.version >= 48:
			stream.write_uint64(instance.u_5)
			stream.write_uint64(instance.u_6)
		if instance.context.version <= 13:
			stream.write_uint64(instance.u_5)
			stream.write_uint64(instance.uv_buffer_size)
		if instance.context.version <= 13:
			stream.write_uint64(instance.u_6)
			stream.write_uint64(instance.u_7)

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
		return f'BufferInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* u_0 = {fmt_member(self.u_0, indent+1)}'
		s += f'\n	* u_1 = {fmt_member(self.u_1, indent+1)}'
		s += f'\n	* chunk_pos_size = {fmt_member(self.chunk_pos_size, indent+1)}'
		s += f'\n	* chunk_pos_ptr = {fmt_member(self.chunk_pos_ptr, indent+1)}'
		s += f'\n	* chunks_size = {fmt_member(self.chunks_size, indent+1)}'
		s += f'\n	* chunks_ptr = {fmt_member(self.chunks_ptr, indent+1)}'
		s += f'\n	* vertex_buffer_size = {fmt_member(self.vertex_buffer_size, indent+1)}'
		s += f'\n	* u_2 = {fmt_member(self.u_2, indent+1)}'
		s += f'\n	* u_3 = {fmt_member(self.u_3, indent+1)}'
		s += f'\n	* tris_buffer_size = {fmt_member(self.tris_buffer_size, indent+1)}'
		s += f'\n	* u_4 = {fmt_member(self.u_4, indent+1)}'
		s += f'\n	* u_5 = {fmt_member(self.u_5, indent+1)}'
		s += f'\n	* u_6 = {fmt_member(self.u_6, indent+1)}'
		s += f'\n	* u_5 = {fmt_member(self.u_5, indent+1)}'
		s += f'\n	* uv_buffer_size = {fmt_member(self.uv_buffer_size, indent+1)}'
		s += f'\n	* u_6 = {fmt_member(self.u_6, indent+1)}'
		s += f'\n	* u_7 = {fmt_member(self.u_7, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
