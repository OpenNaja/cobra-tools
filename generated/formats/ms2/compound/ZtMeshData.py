
import logging
import math
import numpy as np
from generated.formats.ms2.compound.packing_utils import *
from plugin.utils.tristrip import triangulate
from source.formats.base.basic import fmt_member
from generated.formats.ms2.bitfield.ModelFlagDLA import ModelFlagDLA
from generated.formats.ms2.bitfield.ModelFlagZT import ModelFlagZT
from generated.formats.ms2.compound.MeshData import MeshData


class ZtMeshData(MeshData):

	"""
	64 bytes total, same layout for DLA and ZTUAC
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# repeat
		self.tri_index_count = 0
		self.vertex_count = 0

		# stores count, -1 as ints
		self.tri_info_offset = 0

		# stores count, -1 as ints
		self.vert_info_offset = 0

		# x*16 = offset in buffer 2
		self.known_ff_0 = 0

		# relative to start of buffer[i]'s tris section start, blocks of 2 bytes (ushort), tri_index_count
		self.tri_offset = 0

		# relative to start of buffer[i], blocks of 8 bytes, count vertex_count
		self.uv_offset = 0

		# relative to start of buffer[i], blocks of 24 bytes, count vertex_count
		self.vertex_offset = 0

		# x*16 = offset in buffer 2
		self.known_ff_1 = 0

		# x*16 = offset in buffer 2
		self.one_0 = 0

		# ?
		self.one_1 = 0

		# ?
		self.poweroftwo = 0

		# bitfield
		self.flag = ModelFlagDLA(self.context, 0, None)

		# bitfield
		self.flag = ModelFlagZT(self.context, 0, None)

		# always zero
		self.zero_uac = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.tri_index_count = 0
		self.vertex_count = 0
		self.tri_info_offset = 0
		self.vert_info_offset = 0
		self.known_ff_0 = 0
		self.tri_offset = 0
		self.uv_offset = 0
		self.vertex_offset = 0
		self.known_ff_1 = 0
		self.one_0 = 0
		self.one_1 = 0
		self.poweroftwo = 0
		if self.context.version <= 7:
			self.flag = ModelFlagDLA(self.context, 0, None)
		if self.context.version >= 13:
			self.flag = ModelFlagZT(self.context, 0, None)
		self.zero_uac = 0

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
		instance.tri_index_count = stream.read_uint()
		instance.vertex_count = stream.read_uint()
		instance.tri_info_offset = stream.read_uint()
		instance.vert_info_offset = stream.read_uint()
		instance.known_ff_0 = stream.read_int()
		instance.tri_offset = stream.read_uint()
		instance.uv_offset = stream.read_uint()
		instance.vertex_offset = stream.read_uint()
		instance.known_ff_1 = stream.read_short()
		instance.one_0 = stream.read_ushort()
		instance.one_1 = stream.read_ushort()
		instance.poweroftwo = stream.read_ushort()
		if instance.context.version <= 7:
			instance.flag = ModelFlagDLA.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 13:
			instance.flag = ModelFlagZT.from_stream(stream, instance.context, 0, None)
		instance.zero_uac = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.tri_index_count)
		stream.write_uint(instance.vertex_count)
		stream.write_uint(instance.tri_info_offset)
		stream.write_uint(instance.vert_info_offset)
		stream.write_int(instance.known_ff_0)
		stream.write_uint(instance.tri_offset)
		stream.write_uint(instance.uv_offset)
		stream.write_uint(instance.vertex_offset)
		stream.write_short(instance.known_ff_1)
		stream.write_ushort(instance.one_0)
		stream.write_ushort(instance.one_1)
		stream.write_ushort(instance.poweroftwo)
		if instance.context.version <= 7:
			ModelFlagDLA.to_stream(stream, instance.flag)
		if instance.context.version >= 13:
			ModelFlagZT.to_stream(stream, instance.flag)
		stream.write_uint(instance.zero_uac)

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
		return f'ZtMeshData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* tri_index_count = {fmt_member(self.tri_index_count, indent+1)}'
		s += f'\n	* vertex_count = {fmt_member(self.vertex_count, indent+1)}'
		s += f'\n	* tri_info_offset = {fmt_member(self.tri_info_offset, indent+1)}'
		s += f'\n	* vert_info_offset = {fmt_member(self.vert_info_offset, indent+1)}'
		s += f'\n	* known_ff_0 = {fmt_member(self.known_ff_0, indent+1)}'
		s += f'\n	* tri_offset = {fmt_member(self.tri_offset, indent+1)}'
		s += f'\n	* uv_offset = {fmt_member(self.uv_offset, indent+1)}'
		s += f'\n	* vertex_offset = {fmt_member(self.vertex_offset, indent+1)}'
		s += f'\n	* known_ff_1 = {fmt_member(self.known_ff_1, indent+1)}'
		s += f'\n	* one_0 = {fmt_member(self.one_0, indent+1)}'
		s += f'\n	* one_1 = {fmt_member(self.one_1, indent+1)}'
		s += f'\n	* poweroftwo = {fmt_member(self.poweroftwo, indent+1)}'
		s += f'\n	* flag = {fmt_member(self.flag, indent+1)}'
		s += f'\n	* zero_uac = {fmt_member(self.zero_uac, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

	def init_arrays(self):
		self.vertices = np.empty((self.vertex_count, 3), np.float32)
		self.normals = np.empty((self.vertex_count, 3), np.float32)
		self.tangents = np.empty((self.vertex_count, 3), np.float32)
		try:
			uv_shape = self.dt_colors["uvs"].shape
			self.uvs = np.empty((self.vertex_count, *uv_shape), np.float32)
		except:
			self.uvs = None
		try:
			colors_shape = self.dt_colors["colors"].shape
			self.colors = np.empty((self.vertex_count, *colors_shape), np.float32)
		except:
			self.colors = None
		self.weights_info = {}

	def update_dtype(self):
		"""Update MeshData.dt (numpy dtype) according to MeshData.flag"""
		# basic shared stuff
		dt = [
			("bone ids", np.ubyte, (4,)),
			("bone weights", np.ubyte, (4,)),
			("pos", np.float16, (3,)),
			("one", np.float16),
			("normal", np.ubyte, (3,)),
			("winding", np.ubyte, ),  # not tested
			("tangent", np.ubyte, (3,)),
			("bone index", np.ubyte, ),  # not tested
		]
		vert_count_in_stream = self.sum_uv_dict[self.stream_index]
		if 4294967295 == self.vertex_offset:
			# 20 bytes per vert
			dt_colors = [
				("pos", np.float16, (3,)),
				("one", np.float16),
				("normal", np.ubyte, (3,)),
				("winding", np.ubyte, ),  # not tested
				("tangent", np.ubyte, (3,)),
				("bone index", np.ubyte, ),  # not tested
				# ("colors", np.ubyte, (1, 4)),
				("uvs", np.ushort, (1, 2)),
			]
		else:
			# hack for zt monitor
			if self.buffer_info.uvs_size // vert_count_in_stream == 4:
				dt_colors = [
					("uvs", np.ushort, (1, 2)),
				]
			else:
				dt_colors = [
					("colors", np.ubyte, (1, 4)),
					("uvs", np.ushort, (1 + self.some_index, 2)),
				]
		self.dt = np.dtype(dt)
		self.dt_colors = np.dtype(dt_colors)
		self.update_shell_count()

	def read_verts(self):
		logging.debug(f"Tri info address {self.tri_info_offset}")
		logging.debug(f"Vertex info address {self.vert_info_offset}")
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# create arrays for the unpacked ms2_file
		self.init_arrays()
		# read vertices of this mesh
		self.verts_data = np.empty(dtype=self.dt, shape=self.vertex_count)
		self.colors_data = np.empty(dtype=self.dt_colors, shape=self.vertex_count)
		self.buffer_info.uvs.seek(self.uv_offset)
		# logging.debug(f"UV at {self.buffer_info.uvs.tell()}")
		self.buffer_info.uvs.readinto(self.colors_data)
		if 4294967295 != self.vertex_offset:
			self.buffer_info.verts.seek(self.vertex_offset)
			# logging.debug(f"{self.vertex_count} VERTS at {self.buffer_info.verts.tell()}")
			self.buffer_info.verts.readinto(self.verts_data)
			self.normals[:] = self.verts_data["normal"]
			self.tangents[:] = self.verts_data["tangent"]
			self.vertices[:] = self.verts_data["pos"]

			# if "bone weights" in self.dt.fields:
			bone_weights = self.verts_data["bone weights"].astype(np.float32) / 255
			self.get_blended_weights(self.verts_data["bone ids"], bone_weights)
		else:
			self.normals[:] = self.colors_data["normal"]
			self.tangents[:] = self.colors_data["tangent"]
			self.vertices[:] = self.colors_data["pos"]

		# first cast to the float uvs array so unpacking doesn't use int division
		if self.colors is not None:
			# first cast to the float colors array so unpacking doesn't use int division
			self.colors[:] = self.colors_data["colors"]
			unpack_ubyte_color(self.colors)
		if self.uvs is not None:
			self.uvs[:] = self.colors_data["uvs"]
			self.uvs /= 2048
		unpack_ubyte_vector(self.normals)
		unpack_ubyte_vector(self.tangents)
		unpack_swizzle_vectorized(self.vertices)
		unpack_swizzle_vectorized_b(self.normals)
		unpack_swizzle_vectorized(self.tangents)

		# self.get_static_weights(self.verts_data["bone index"], self.use_blended_weights)


