
import math
import logging
import numpy as np
from generated.formats.ms2.compound.packing_utils import *
from plugin.utils.tristrip import triangulate
from generated.formats.ms2.bitfield.ModelFlag import ModelFlag
from generated.formats.ms2.compound.MeshData import MeshData


class PcMeshData(MeshData):

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		super().__init__(context, arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# repeat
		self.tri_index_count_a = 0

		# vertex count of model
		self.vertex_count = 0

		# x*16 = offset in buffer 2
		self.tri_offset = 0

		# number of index entries in the triangle index list; (not: number of triangles, byte count of tri buffer)
		self.tri_index_count = 0

		# x*16 = offset in buffer 2
		self.vertex_offset = 0

		# x*16 = offset in buffer 2
		self.weights_offset = 0

		# x*16 = offset in buffer 2
		self.uv_offset = 0

		# always zero
		self.zero_b = 0

		# x*16 = offset in buffer 2
		self.vertex_color_offset = 0

		# ?
		self.vertex_offset_within_lod = 0

		# power of 2 increasing with lod index
		self.poweroftwo = 0

		# always zero
		self.zero = 0

		# some floats
		self.unknown_07 = 0

		# bitfield
		self.flag = ModelFlag()

		# always zero
		self.zero_uac = 0
		self.set_defaults()

	def set_defaults(self):
		self.tri_index_count_a = 0
		self.vertex_count = 0
		self.tri_offset = 0
		self.tri_index_count = 0
		self.vertex_offset = 0
		self.weights_offset = 0
		self.uv_offset = 0
		self.zero_b = 0
		self.vertex_color_offset = 0
		self.vertex_offset_within_lod = 0
		if self.context.version == 32:
			self.poweroftwo = 0
		if self.context.version == 32:
			self.zero = 0
		if self.context.version == 32:
			self.unknown_07 = 0
		self.flag = ModelFlag()
		if self.context.version == 13:
			self.zero_uac = 0

	def read(self, stream):
		self.io_start = stream.tell()
		super().read(stream)
		self.tri_index_count_a = stream.read_uint()
		self.vertex_count = stream.read_uint()
		self.tri_offset = stream.read_uint()
		self.tri_index_count = stream.read_uint()
		self.vertex_offset = stream.read_uint()
		self.weights_offset = stream.read_uint()
		self.uv_offset = stream.read_uint()
		self.zero_b = stream.read_uint()
		self.vertex_color_offset = stream.read_uint()
		self.vertex_offset_within_lod = stream.read_uint()
		if self.context.version == 32:
			self.poweroftwo = stream.read_uint()
			self.zero = stream.read_uint()
		if self.context.version == 32:
			self.unknown_07 = stream.read_float()
		self.flag = stream.read_type(ModelFlag)
		if self.context.version == 13:
			self.zero_uac = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		super().write(stream)
		stream.write_uint(self.tri_index_count_a)
		stream.write_uint(self.vertex_count)
		stream.write_uint(self.tri_offset)
		stream.write_uint(self.tri_index_count)
		stream.write_uint(self.vertex_offset)
		stream.write_uint(self.weights_offset)
		stream.write_uint(self.uv_offset)
		stream.write_uint(self.zero_b)
		stream.write_uint(self.vertex_color_offset)
		stream.write_uint(self.vertex_offset_within_lod)
		if self.context.version == 32:
			stream.write_uint(self.poweroftwo)
			stream.write_uint(self.zero)
		if self.context.version == 32:
			stream.write_float(self.unknown_07)
		stream.write_type(self.flag)
		if self.context.version == 13:
			stream.write_uint(self.zero_uac)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'PcMeshData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* tri_index_count_a = {self.tri_index_count_a.__repr__()}'
		s += f'\n	* vertex_count = {self.vertex_count.__repr__()}'
		s += f'\n	* tri_offset = {self.tri_offset.__repr__()}'
		s += f'\n	* tri_index_count = {self.tri_index_count.__repr__()}'
		s += f'\n	* vertex_offset = {self.vertex_offset.__repr__()}'
		s += f'\n	* weights_offset = {self.weights_offset.__repr__()}'
		s += f'\n	* uv_offset = {self.uv_offset.__repr__()}'
		s += f'\n	* zero_b = {self.zero_b.__repr__()}'
		s += f'\n	* vertex_color_offset = {self.vertex_color_offset.__repr__()}'
		s += f'\n	* vertex_offset_within_lod = {self.vertex_offset_within_lod.__repr__()}'
		s += f'\n	* poweroftwo = {self.poweroftwo.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* unknown_07 = {self.unknown_07.__repr__()}'
		s += f'\n	* flag = {self.flag.__repr__()}'
		s += f'\n	* zero_uac = {self.zero_uac.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s

	def populate(self, ms2_file, ms2_stream, buffer_2_offset, base=512, last_vertex_offset=0, sum_uv_dict={}):
		self.buffer_2_offset = buffer_2_offset
		self.ms2_file = ms2_file
		self.base = base
		self.shapekeys = None
		self.read_verts(ms2_stream)
		self.read_tris(ms2_stream)

	def init_arrays(self, count):
		self.vertex_count = count
		self.vertices = np.empty((self.vertex_count, 3), np.float32)
		self.normals = np.empty((self.vertex_count, 3), np.float32)
		self.tangents = np.empty((self.vertex_count, 3), np.float32)
		try:
			uv_shape = self.dt_uv["uvs"].shape
			self.uvs = np.empty((self.vertex_count, *uv_shape), np.float32)
		except:
			self.uvs = None
		try:
			colors_shape = self.dt["colors"].shape
			self.colors = np.empty((self.vertex_count, *colors_shape), np.float32)
		except:
			self.colors = None
		self.weights = []

	def update_dtype(self):
		"""Update MeshData.dt (numpy dtype) according to MeshData.flag"""
		# basic shared stuff
		dt = [
			("pos", np.uint64),
			("normal", np.ubyte, (3,)),
			("unk", np.ubyte),
			("tangent", np.ubyte, (3,)),
			("bone index", np.ubyte),
		]
		dt_uv = [
			("uvs", np.ushort, (1, 2)),
		]
		# bone weights
		# if self.flag in (529, 533, 885, 565, 1013, 528, 821):
		dt_w = [
			("bone ids", np.ubyte, (4,)),
			("bone weights", np.ubyte, (4,)),
		]
		self.dt = np.dtype(dt)
		self.dt_uv = np.dtype(dt_uv)
		self.dt_w = np.dtype(dt_w)
		self.update_shell_count()
		logging.debug(f"PC size of vertex: {self.dt.itemsize}")
		logging.debug(f"PC size of uv: {self.dt_uv.itemsize}")
		logging.debug(f"PC size of weights: {self.dt_w.itemsize}")

	@property
	def tris_address(self):
		logging.debug(f"self.buffer_2_offset {self.buffer_2_offset}, count {self.tri_offset}")
		return self.buffer_2_offset + (self.tri_offset * 16)

	def read_verts(self, stream):
		# read a vertices of this mesh
		stream.seek(self.buffer_2_offset + (self.vertex_offset * 16))
		logging.debug(f"VERTS at {stream.tell()}")
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# read the packed ms2_file
		self.verts_data = np.empty(dtype=self.dt, shape=self.vertex_count)
		stream.readinto(self.verts_data)
		stream.seek(self.buffer_2_offset + (self.uv_offset * 16))
		logging.debug(f"UV at {stream.tell()}")
		self.uv_data = np.empty(dtype=self.dt_uv, shape=self.vertex_count)
		stream.readinto(self.uv_data)
		stream.seek(self.buffer_2_offset + (self.weights_offset * 16))
		logging.debug(f"WEIGHTS at {stream.tell()}")
		# print(self)
		# PC ostrich download has self.weights_offset = 0 for eyes and lashes, which consequently get wrong weights
		self.weights_data = np.empty(dtype=self.dt_w, shape=self.vertex_count)
		stream.readinto(self.weights_data)
		# print(self.verts_data)
		# create arrays for the unpacked ms2_file
		self.init_arrays(self.vertex_count)
		# first cast to the float uvs array so unpacking doesn't use int division
		if self.uvs is not None:
			self.uvs[:] = self.uv_data[:]["uvs"]
			# unpack uvs
			self.uvs = unpack_ushort_vector(self.uvs)
		# if self.colors is not None:
		# 	# first cast to the float colors array so unpacking doesn't use int division
		# 	self.colors[:] = self.verts_data[:]["colors"]
		# 	self.colors /= 255
		self.normals[:] = self.verts_data[:]["normal"]
		self.tangents[:] = self.verts_data[:]["tangent"]
		self.normals = (self.normals - 128) / 128
		self.tangents = (self.tangents - 128) / 128
		for i in range(self.vertex_count):
			in_pos_packed = self.verts_data[i]["pos"]
			vert, residue = unpack_longint_vec(in_pos_packed, self.base)
			self.vertices[i] = unpack_swizzle(vert)
			self.normals[i] = unpack_swizzle(self.normals[i])
			self.tangents[i] = unpack_swizzle(self.tangents[i])
			self.weights.append(unpack_weights(self, i, residue, extra=False))
		# print(self.vertices)

