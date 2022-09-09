from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64


class BufferInfo(BaseStruct):

	"""
	Fragment data describing a MS2 buffer giving the size of the whole vertex and tri buffer.
	ZTUAC, DLA: 64 bytes verts, tris, uvs (incl. verts sometimes)
	PC: 32 bytes, lumps all data (pos, uv, weights, tris) into verts_size
	JWE1: 48 bytes
	PZ old: 32 bytes?
	PZ1.6+ and JWE2: 56 bytes
	JWE2 Biosyn: 88 bytes, with 4 values, order of arrays in buffer is verts, tris, tri_chunks, vert_chunks
	
	JWE and PC, 16 bytes of 00 padding
	"""

	__name__ = 'BufferInfo'

	_import_key = 'ms2.compounds.BufferInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
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

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if 32 <= instance.context.version <= 47:
			yield 'u_0', Uint64, (0, None), (False, None)
			yield 'u_1', Uint64, (0, None), (False, None)
		if (instance.context.version == 51) and instance.context.biosyn:
			yield 'tri_chunks_size', Uint64, (0, None), (False, None)
			yield 'tri_chunks_ptr', Uint64, (0, None), (False, None)
			yield 'vert_chunks_size', Uint64, (0, None), (False, None)
			yield 'vert_chunks_ptr', Uint64, (0, None), (False, None)
		yield 'verts_size', Uint64, (0, None), (False, None)
		yield 'verts_ptr', Uint64, (0, None), (False, None)
		if instance.context.version >= 48:
			yield 'u_3', Uint64, (0, None), (False, None)
		if not (instance.context.version == 32):
			yield 'tris_size', Uint64, (0, None), (False, None)
			yield 'tris_ptr', Uint64, (0, None), (False, None)
		if instance.context.version >= 48:
			yield 'u_5', Uint64, (0, None), (False, None)
			yield 'u_6', Uint64, (0, None), (False, None)
		if instance.context.version <= 13:
			yield 'u_5', Uint64, (0, None), (False, None)
			yield 'uvs_size', Uint64, (0, None), (False, None)
			yield 'u_6', Uint64, (0, None), (False, None)
			yield 'u_7', Uint64, (0, None), (False, None)
