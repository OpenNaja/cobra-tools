
import logging
import math
import numpy as np
import struct
from generated.formats.ms2.compound.packing_utils import *

FUR_OVERHEAD = 2


import numpy
import typing
from generated.array import Array
from generated.formats.ms2.bitfield.ModelFlag import ModelFlag
from generated.formats.ms2.compound.MeshData import MeshData


class NewMeshData(MeshData):

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		super().__init__(context, arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# PZ and JWE have a ptr at the start instead of the stream index
		self.ptr = 0

		# unused
		self.zero_0 = 0

		# vertex count of model
		self.vertex_count = 0

		# number of index entries in the triangle index list; (not: number of triangles, byte count of tri buffer)
		self.tri_index_count = 0

		# always zero
		self.zero_1 = 0

		# power of 2 increasing with lod index
		self.poweroftwo = 0

		# byte offset from start of vert buffer (=start of buffer nr 2) in bytes
		self.vertex_offset = 0

		# usually 48
		self.size_of_vertex = 0

		# byte offset from start of tri buffer in bytes
		self.tri_offset = 0

		# always zero
		self.zero_2 = 0

		# some floats, purpose unknown
		self.unk_floats = numpy.zeros((2), dtype='float')

		# always zero
		self.zero_3 = 0

		# bitfield, determines vertex format
		self.flag = ModelFlag()
		self.set_defaults()

	def set_defaults(self):
		self.ptr = 0
		self.zero_0 = 0
		self.vertex_count = 0
		self.tri_index_count = 0
		self.zero_1 = 0
		self.poweroftwo = 0
		self.vertex_offset = 0
		self.size_of_vertex = 0
		self.tri_offset = 0
		self.zero_2 = 0
		self.unk_floats = numpy.zeros((2), dtype='float')
		self.zero_3 = 0
		self.flag = ModelFlag()

	def read(self, stream):
		self.io_start = stream.tell()
		super().read(stream)
		self.ptr = stream.read_uint64()
		self.zero_0 = stream.read_uint64()
		self.vertex_count = stream.read_uint()
		self.tri_index_count = stream.read_uint()
		self.zero_1 = stream.read_uint()
		self.poweroftwo = stream.read_uint()
		self.vertex_offset = stream.read_uint()
		self.size_of_vertex = stream.read_uint()
		self.tri_offset = stream.read_uint()
		self.zero_2 = stream.read_uint()
		self.unk_floats = stream.read_floats((2))
		self.zero_3 = stream.read_uint()
		self.flag = stream.read_type(ModelFlag)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		super().write(stream)
		stream.write_uint64(self.ptr)
		stream.write_uint64(self.zero_0)
		stream.write_uint(self.vertex_count)
		stream.write_uint(self.tri_index_count)
		stream.write_uint(self.zero_1)
		stream.write_uint(self.poweroftwo)
		stream.write_uint(self.vertex_offset)
		stream.write_uint(self.size_of_vertex)
		stream.write_uint(self.tri_offset)
		stream.write_uint(self.zero_2)
		stream.write_floats(self.unk_floats)
		stream.write_uint(self.zero_3)
		stream.write_type(self.flag)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'NewMeshData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* ptr = {self.ptr.__repr__()}'
		s += f'\n	* zero_0 = {self.zero_0.__repr__()}'
		s += f'\n	* vertex_count = {self.vertex_count.__repr__()}'
		s += f'\n	* tri_index_count = {self.tri_index_count.__repr__()}'
		s += f'\n	* zero_1 = {self.zero_1.__repr__()}'
		s += f'\n	* poweroftwo = {self.poweroftwo.__repr__()}'
		s += f'\n	* vertex_offset = {self.vertex_offset.__repr__()}'
		s += f'\n	* size_of_vertex = {self.size_of_vertex.__repr__()}'
		s += f'\n	* tri_offset = {self.tri_offset.__repr__()}'
		s += f'\n	* zero_2 = {self.zero_2.__repr__()}'
		s += f'\n	* unk_floats = {self.unk_floats.__repr__()}'
		s += f'\n	* zero_3 = {self.zero_3.__repr__()}'
		s += f'\n	* flag = {self.flag.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s

	def init_arrays(self):
		self.vertices = np.empty((self.vertex_count, 3), np.float32)
		self.normals = np.empty((self.vertex_count, 3), np.float32)
		self.tangents = np.empty((self.vertex_count, 3), np.float32)
		try:
			uv_shape = self.dt["uvs"].shape
			self.uvs = np.empty((self.vertex_count, *uv_shape), np.float32)
		except:
			self.uvs = None
		try:
			fur_shape = self.dt["fur_shell"].shape
			self.fur = np.empty((self.vertex_count, *fur_shape), np.float32)
		except:
			self.fur = None
		try:
			colors_shape = self.dt["colors"].shape
			self.colors = np.empty((self.vertex_count, *colors_shape), np.float32)
		except:
			self.colors = None
		try:
			shapekeys_shape = self.dt["shapekeys0"].shape
			self.shapekeys = np.empty((self.vertex_count, 3), np.float32)
		except:
			self.shapekeys = None
		self.weights = []

	def get_vcol_count(self, ):
		if "colors" in self.dt.fields:
			return self.dt["colors"].shape[0]
		return 0

	def get_uv_count(self, ):
		if "uvs" in self.dt.fields:
			return self.dt["uvs"].shape[0]
		return 0

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
		# uv variations
		if self.flag == 528:
			dt.extend([
				("uvs", np.ushort, (1, 2)),
				("zeros0", np.int32, (3,))
			])
		elif self.flag == 529:
			dt.extend([
				("uvs", np.ushort, (2, 2)),
				("zeros0", np.int32, (2,))
			])
		elif self.flag in (565,):
			dt.extend([
				("uvs", np.ushort, (2, 2)),
				("colors", np.ubyte, (1, 4)),  # these appear to be directional vectors
				("zeros0", np.int32, (1,))
			])
		elif self.flag in (821, 853, 885, 1013):
			dt.extend([
				("uvs", np.ushort, (1, 2)),
				("fur_shell", np.ushort, (2,)),
				("colors", np.ubyte, (1, 4)),  # these appear to be directional vectors
				("zeros0", np.int32, (1,))
			])
		elif self.flag == 533:
			dt.extend([
				# see walls_gate.mdl2, two uv layers
				("uvs", np.ushort, (2, 2)),
				("colors", np.ubyte, (1, 4)),
				("zeros2", np.int32, (1,))
			])
		elif self.flag == 513:
			dt.extend([
				("uvs", np.ushort, (2, 2)),
				# ("colors", np.ubyte, (1, 4)),
				("zeros2", np.uint64, (3,))
			])
		elif self.flag == 512:
			dt.extend([
				# tree_birch_white_03 - apparently 8 uvs
				("uvs", np.ushort, (8, 2)),
			])
		elif self.flag == 517:
			dt.extend([
				("uvs", np.ushort, (1, 2)),
				("shapekeys0", np.uint32, 1),
				("colors", np.ubyte, (1, 4)),  # this appears to be normals, or something similar
				("shapekeys1", np.uint32, 1),
				("colors1", np.ubyte, (4, 4)),
			])
		elif self.flag == 545:
			dt.extend([
				# cz_glasspanel_4m_02.mdl2
				("uvs", np.ushort, (1, 2)),
				("zeros2", np.uint32, (7,)),
			])

		# bone weights
		if self.flag in (528, 529, 533, 565, 821, 853, 885, 1013):
			dt.extend([
				("bone ids", np.ubyte, (4,)),
				("bone weights", np.ubyte, (4,)),
				("zeros1", np.uint64)
			])
		self.dt = np.dtype(dt)
		self.update_shell_count()
		if self.dt.itemsize != self.size_of_vertex:
			raise AttributeError(
				f"Vertex size for flag {self.flag} is wrong! Collected {self.dt.itemsize}, got {self.size_of_vertex}")

	def read_verts(self, stream):
		# read a vertices of this mesh
		stream.seek(self.buffer_2_offset + self.vertex_offset)
		logging.debug(f"Reading {self.vertex_count} verts at {stream.tell()}")
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# read the packed ms2_file
		self.verts_data = np.empty(dtype=self.dt, shape=self.vertex_count)
		stream.readinto(self.verts_data)
		# if len(self.verts_data) != self.vertex_count:
		# 	raise BufferError(f"{len(self.verts_data)} were read into vertex buffer, should have {self.vertex_count}")
		# create arrays for the unpacked ms2_file
		self.init_arrays()
		# first cast to the float uvs array so unpacking doesn't use int division
		if self.uvs is not None:
			self.uvs[:] = self.verts_data[:]["uvs"]
			self.uvs = unpack_ushort_vector(self.uvs)
		self.fur_length = 0.0
		if self.fur is not None:
			self.fur[:] = self.verts_data[:]["fur_shell"]
			self.fur = unpack_ushort_vector(self.fur)
			# normalize with some overhead
			self.fur_length = np.max(self.fur[:, 0]) * FUR_OVERHEAD
			# fur length can be set to 0 for the whole mesh, so make sure we don't divide in that case
			if self.fur_length:
				# print("self.fur_length", self.fur_length)
				self.fur[:, 0] /= self.fur_length
			# value range of fur width is +-16 - squash it into 0 - 1
			self.fur[:, 1] = remap(self.fur[:, 1], -16, 16, 0, 1)
			# print("self.fur[0]", self.fur[0])
		if self.colors is not None:
			# first cast to the float colors array so unpacking doesn't use int division
			self.colors[:] = self.verts_data[:]["colors"]
			self.colors /= 255
		self.normals[:] = self.verts_data[:]["normal"]
		self.tangents[:] = self.verts_data[:]["tangent"]
		self.normals = (self.normals - 128) / 128
		# normalize
		self.normals /= np.linalg.norm(self.normals, axis=1, keepdims=True)
		self.tangents = (self.tangents - 128) / 128
		# unpack the shapekeys
		if self.shapekeys is not None:
			for i in range(self.vertex_count):
				first = self.verts_data[i]["shapekeys0"]
				second = self.verts_data[i]["shapekeys1"]
				packed = struct.pack("LL", first, second)
				unpacked = struct.unpack("Q", packed)[0]
				vert, residue = unpack_longint_vec(unpacked, self.base)
				self.shapekeys[i] = unpack_swizzle(vert)
			# print(self.shapekeys)

		for i in range(self.vertex_count):
			in_pos_packed = self.verts_data[i]["pos"]
			vert, residue = unpack_longint_vec(in_pos_packed, self.base)
			self.vertices[i] = unpack_swizzle(vert)
			self.normals[i] = unpack_swizzle(self.normals[i])
			self.tangents[i] = unpack_swizzle(self.tangents[i])
			self.weights.append(unpack_weights(self, i, residue))

	def write_verts(self, stream):
		stream.write(self.verts_data.tobytes())

	@property
	def tris_address(self):
		return self.buffer_2_offset + self.ms2_file.buffer_info.vertexdatasize + self.tri_offset

	def set_verts(self, verts):
		"""Update self.verts_data from list of new verts"""
		self.verts_data = np.zeros(len(verts), dtype=self.dt)
		for i, (
				position, residue, normal, unk_0, tangent, bone_index, uvs, vcols, bone_ids, bone_weights,
				fur_length, fur_width, shapekey) in enumerate(
			verts):
			# print("shapekey", shapekey)
			self.verts_data[i]["pos"] = pack_longint_vec(pack_swizzle(position), residue, self.base)
			self.verts_data[i]["normal"] = pack_ubyte_vector(pack_swizzle(normal))
			self.verts_data[i]["tangent"] = pack_ubyte_vector(pack_swizzle(tangent))
			self.verts_data[i]["unk"] = unk_0 * 255
			self.verts_data[i]["bone index"] = bone_index
			if "bone ids" in self.dt.fields:
				self.verts_data[i]["bone ids"] = bone_ids
				# round is essential so the float is not truncated
				self.verts_data[i]["bone weights"] = list(round(w * 255) for w in bone_weights)
				# print(self.verts_data[i]["bone weights"], np.sum(self.verts_data[i]["bone weights"]))
				# additional double check
				d = np.sum(self.verts_data[i]["bone weights"]) - 255
				self.verts_data[i]["bone weights"][0] -= d
				assert np.sum(self.verts_data[i]["bone weights"]) == 255
			if "uvs" in self.dt.fields:
				self.verts_data[i]["uvs"] = list(pack_ushort_vector(uv) for uv in uvs)
			if "fur_shell" in self.dt.fields and fur_length is not None:
				self.verts_data[i]["fur_shell"] = pack_ushort_vector((fur_length, remap(fur_width, 0, 1, -16, 16)))
			if "colors" in self.dt.fields:
				self.verts_data[i]["colors"] = list(list(round(c * 255) for c in vcol) for vcol in vcols)
			if "shapekeys0" in self.dt.fields:
				# first pack it as uint64
				raw_packed = pack_longint_vec(pack_swizzle(shapekey), 0, self.base)
				if raw_packed < 0:
					logging.error(f"Shapekey {raw_packed} could not be packed into uint64")
					raw_packed = 0
				raw_bytes = struct.pack("Q", raw_packed)
				# unpack to 2 uints again and assign data
				first, second = struct.unpack("LL", raw_bytes)
				self.verts_data[i]["shapekeys0"] = first
				self.verts_data[i]["shapekeys1"] = second

	def populate(self, ms2_file, ms2_stream, buffer_2_offset, base=512):
		self.buffer_2_offset = buffer_2_offset
		self.ms2_file = ms2_file
		self.base = base
		self.read_verts(ms2_stream)
		self.read_tris(ms2_stream)
		self.validate_tris()


