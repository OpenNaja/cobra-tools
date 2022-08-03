from generated.formats.base.basic import fmt_member
from generated.formats.base.basic import Uint64
from generated.struct import StructBase


class BufferInfo(StructBase):

	"""
	Fragment data describing a MS2 buffer giving the size of the whole vertex and tri buffer.
	ZTUAC: 64 bytes
	PC: 32 bytes, lumps all data (pos, uv, weights, tris) into verts_size
	JWE1: 48 bytes
	PZ old: 32 bytes?
	PZ1.6+ and JWE2: 56 bytes
	JWE2 Biosyn: 88 bytes, with 4 values, order of arrays in buffer is verts, tris, tri_chunks, vert_chunks
	
	JWE and PC, 16 bytes of 00 padding
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.u_0 = 0
		self.u_1 = 0
		self.tri_chunks_size = 0
		self.tri_chunks_ptr = 0
		self.vert_chunks_size = 0
		self.vert_chunks_ptr = 0
		self.verts_size = 0
		self.verts_ptr = 0
		self.u_3 = 0
		self.tris_size = 0
		self.tris_ptr = 0
		self.u_5 = 0
		self.u_6 = 0
		self.u_5 = 0

		# from start of tris buffer
		self.uvs_size = 0
		self.u_6 = 0
		self.u_7 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if 32 <= self.context.version <= 47:
			self.u_0 = 0
			self.u_1 = 0
		if (self.context.version == 51) and self.context.biosyn:
			self.tri_chunks_size = 0
			self.tri_chunks_ptr = 0
			self.vert_chunks_size = 0
			self.vert_chunks_ptr = 0
		self.verts_size = 0
		self.verts_ptr = 0
		if self.context.version >= 48:
			self.u_3 = 0
		if not (self.context.version == 32):
			self.tris_size = 0
			self.tris_ptr = 0
		if self.context.version >= 48:
			self.u_5 = 0
			self.u_6 = 0
		if self.context.version <= 13:
			self.u_5 = 0
			self.uvs_size = 0
			self.u_6 = 0
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
		super().read_fields(stream, instance)
		if 32 <= instance.context.version <= 47:
			instance.u_0 = stream.read_uint64()
			instance.u_1 = stream.read_uint64()
		if (instance.context.version == 51) and instance.context.biosyn:
			instance.tri_chunks_size = stream.read_uint64()
			instance.tri_chunks_ptr = stream.read_uint64()
			instance.vert_chunks_size = stream.read_uint64()
			instance.vert_chunks_ptr = stream.read_uint64()
		instance.verts_size = stream.read_uint64()
		instance.verts_ptr = stream.read_uint64()
		if instance.context.version >= 48:
			instance.u_3 = stream.read_uint64()
		if not (instance.context.version == 32):
			instance.tris_size = stream.read_uint64()
			instance.tris_ptr = stream.read_uint64()
		if instance.context.version >= 48:
			instance.u_5 = stream.read_uint64()
			instance.u_6 = stream.read_uint64()
		if instance.context.version <= 13:
			instance.u_5 = stream.read_uint64()
			instance.uvs_size = stream.read_uint64()
			instance.u_6 = stream.read_uint64()
			instance.u_7 = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if 32 <= instance.context.version <= 47:
			stream.write_uint64(instance.u_0)
			stream.write_uint64(instance.u_1)
		if (instance.context.version == 51) and instance.context.biosyn:
			stream.write_uint64(instance.tri_chunks_size)
			stream.write_uint64(instance.tri_chunks_ptr)
			stream.write_uint64(instance.vert_chunks_size)
			stream.write_uint64(instance.vert_chunks_ptr)
		stream.write_uint64(instance.verts_size)
		stream.write_uint64(instance.verts_ptr)
		if instance.context.version >= 48:
			stream.write_uint64(instance.u_3)
		if not (instance.context.version == 32):
			stream.write_uint64(instance.tris_size)
			stream.write_uint64(instance.tris_ptr)
		if instance.context.version >= 48:
			stream.write_uint64(instance.u_5)
			stream.write_uint64(instance.u_6)
		if instance.context.version <= 13:
			stream.write_uint64(instance.u_5)
			stream.write_uint64(instance.uvs_size)
			stream.write_uint64(instance.u_6)
			stream.write_uint64(instance.u_7)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		if 32 <= instance.context.version <= 47:
			yield ('u_0', Uint64, (0, None))
			yield ('u_1', Uint64, (0, None))
		if (instance.context.version == 51) and instance.context.biosyn:
			yield ('tri_chunks_size', Uint64, (0, None))
			yield ('tri_chunks_ptr', Uint64, (0, None))
			yield ('vert_chunks_size', Uint64, (0, None))
			yield ('vert_chunks_ptr', Uint64, (0, None))
		yield ('verts_size', Uint64, (0, None))
		yield ('verts_ptr', Uint64, (0, None))
		if instance.context.version >= 48:
			yield ('u_3', Uint64, (0, None))
		if not (instance.context.version == 32):
			yield ('tris_size', Uint64, (0, None))
			yield ('tris_ptr', Uint64, (0, None))
		if instance.context.version >= 48:
			yield ('u_5', Uint64, (0, None))
			yield ('u_6', Uint64, (0, None))
		if instance.context.version <= 13:
			yield ('u_5', Uint64, (0, None))
			yield ('uvs_size', Uint64, (0, None))
			yield ('u_6', Uint64, (0, None))
			yield ('u_7', Uint64, (0, None))

	def get_info_str(self, indent=0):
		return f'BufferInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* u_0 = {fmt_member(self.u_0, indent+1)}'
		s += f'\n	* u_1 = {fmt_member(self.u_1, indent+1)}'
		s += f'\n	* tri_chunks_size = {fmt_member(self.tri_chunks_size, indent+1)}'
		s += f'\n	* tri_chunks_ptr = {fmt_member(self.tri_chunks_ptr, indent+1)}'
		s += f'\n	* vert_chunks_size = {fmt_member(self.vert_chunks_size, indent+1)}'
		s += f'\n	* vert_chunks_ptr = {fmt_member(self.vert_chunks_ptr, indent+1)}'
		s += f'\n	* verts_size = {fmt_member(self.verts_size, indent+1)}'
		s += f'\n	* verts_ptr = {fmt_member(self.verts_ptr, indent+1)}'
		s += f'\n	* u_3 = {fmt_member(self.u_3, indent+1)}'
		s += f'\n	* tris_size = {fmt_member(self.tris_size, indent+1)}'
		s += f'\n	* tris_ptr = {fmt_member(self.tris_ptr, indent+1)}'
		s += f'\n	* u_5 = {fmt_member(self.u_5, indent+1)}'
		s += f'\n	* u_6 = {fmt_member(self.u_6, indent+1)}'
		s += f'\n	* u_5 = {fmt_member(self.u_5, indent+1)}'
		s += f'\n	* uvs_size = {fmt_member(self.uvs_size, indent+1)}'
		s += f'\n	* u_6 = {fmt_member(self.u_6, indent+1)}'
		s += f'\n	* u_7 = {fmt_member(self.u_7, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
