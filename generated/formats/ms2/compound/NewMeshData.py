
import logging
import time

import numpy as np
import struct
from generated.formats.ms2.compound.packing_utils import *


from source.formats.base.basic import fmt_member
import numpy
from generated.formats.ms2.bitfield.ModelFlag import ModelFlag
from generated.formats.ms2.compound.MeshData import MeshData


class NewMeshData(MeshData):

	"""
	PZ, JWE2 - 64 bytes incl. inheritance
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default=False)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
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
		self.unk_floats = numpy.zeros((2,), dtype=numpy.dtype('float32'))

		# always zero
		self.zero_3 = 0

		# bitfield, determines vertex format
		self.flag = ModelFlag(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.vertex_count = 0
		self.tri_index_count = 0
		self.zero_1 = 0
		self.poweroftwo = 0
		self.vertex_offset = 0
		self.size_of_vertex = 0
		self.tri_offset = 0
		self.zero_2 = 0
		self.unk_floats = numpy.zeros((2,), dtype=numpy.dtype('float32'))
		self.zero_3 = 0
		self.flag = ModelFlag(self.context, 0, None)

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
		instance.vertex_count = stream.read_uint()
		instance.tri_index_count = stream.read_uint()
		instance.zero_1 = stream.read_uint()
		instance.poweroftwo = stream.read_uint()
		instance.vertex_offset = stream.read_uint()
		instance.size_of_vertex = stream.read_uint()
		instance.tri_offset = stream.read_uint()
		instance.zero_2 = stream.read_uint()
		instance.unk_floats = stream.read_floats((2,))
		instance.zero_3 = stream.read_uint()
		instance.flag = ModelFlag.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.vertex_count)
		stream.write_uint(instance.tri_index_count)
		stream.write_uint(instance.zero_1)
		stream.write_uint(instance.poweroftwo)
		stream.write_uint(instance.vertex_offset)
		stream.write_uint(instance.size_of_vertex)
		stream.write_uint(instance.tri_offset)
		stream.write_uint(instance.zero_2)
		stream.write_floats(instance.unk_floats)
		stream.write_uint(instance.zero_3)
		ModelFlag.to_stream(stream, instance.flag)

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
		return f'NewMeshData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* vertex_count = {fmt_member(self.vertex_count, indent+1)}'
		s += f'\n	* tri_index_count = {fmt_member(self.tri_index_count, indent+1)}'
		s += f'\n	* zero_1 = {fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* poweroftwo = {fmt_member(self.poweroftwo, indent+1)}'
		s += f'\n	* vertex_offset = {fmt_member(self.vertex_offset, indent+1)}'
		s += f'\n	* size_of_vertex = {fmt_member(self.size_of_vertex, indent+1)}'
		s += f'\n	* tri_offset = {fmt_member(self.tri_offset, indent+1)}'
		s += f'\n	* zero_2 = {fmt_member(self.zero_2, indent+1)}'
		s += f'\n	* unk_floats = {fmt_member(self.unk_floats, indent+1)}'
		s += f'\n	* zero_3 = {fmt_member(self.zero_3, indent+1)}'
		s += f'\n	* flag = {fmt_member(self.flag, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

	# @property
	def get_stream_index(self):
		# logging.debug(f"Using stream {self.buffer_info.offset}")
		return self.buffer_info.offset

	def init_arrays(self):
		self.vertices = np.empty((self.vertex_count, 3), np.float32)
		self.normals = np.empty((self.vertex_count, 3), np.float32)
		self.tangents = np.empty((self.vertex_count, 3), np.float32)
		self.residues = np.empty(self.vertex_count, np.bool)
		self.shape_residues = np.empty(self.vertex_count, np.bool)
		try:
			uv_shape = self.dt["uvs"].shape
			self.uvs = np.empty((self.vertex_count, *uv_shape), np.float32)
		except:
			self.uvs = None
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
		self.weights_info = {}

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
			("pos", np.int64),
			("normal", np.ubyte, (3,)),
			("winding", np.ubyte),
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
		elif self.flag in (533, 565, 821, 853, 885, 1013):
			dt.extend([
				("uvs", np.ushort, (2, 2)),  # second UV is either fins texcoords or fur length and shell tile scale
				("colors", np.ubyte, (1, 4)),  # these appear to be directional vectors
				("zeros0", np.int32)
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
				("shapekeys0", np.uint32),
				("colors", np.ubyte, (1, 4)),  # this appears to be normals, or something similar
				("shapekeys1", np.int32),
				# sometimes, only the last is set, the rest being 00 00 C0 7F (NaN)
				("floats", np.float32, (4,)),
			])
		elif self.flag == 545:
			dt.extend([
				# cz_glasspanel_4m_02.mdl2
				("uvs", np.ushort, (1, 2)),
				("zeros2", np.uint32, (7,)),
			])
		# bone weights
		if self.flag.weights:
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

	def read_verts(self):
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# read vertices of this mesh
		self.fur_length = 0.0
		self.stream_info.stream.seek(self.vertex_offset)
		logging.debug(f"Reading {self.vertex_count} verts at {self.stream_info.stream.tell()}")
		# read the packed ms2_file
		self.verts_data = np.empty(dtype=self.dt, shape=self.vertex_count)
		self.stream_info.stream.readinto(self.verts_data)
		# create arrays for the unpacked ms2_file
		self.init_arrays()
		# first cast to the float uvs array so unpacking doesn't use int division
		if self.uvs is not None:
			self.uvs[:] = self.verts_data["uvs"]
			self.uvs = unpack_ushort_vector(self.uvs)
		if self.colors is not None:
			# first cast to the float colors array so unpacking doesn't use int division
			self.colors[:] = self.verts_data["colors"]
			self.colors /= 255
		# todo - PZ uses many more bits, while JWE2 pre-Biosyn uses really just the one bit
		# print(self.verts_data["winding"], set(self.verts_data["winding"]))
		self.windings = self.verts_data["winding"] // 128
		self.normals[:] = self.verts_data["normal"]
		self.tangents[:] = self.verts_data["tangent"]
		start_time = time.time()
		if "bone weights" in self.dt.fields:
			self.bone_weights = self.verts_data["bone weights"].astype(np.float32) / 255
			self.get_weights(self.verts_data["bone ids"], self.bone_weights, self.verts_data["bone index"])
		# before = np.copy(self.verts_data["pos"])
		# first = int(np.copy(before[0]))
		# print("before", bin(int(first)))
		# for i in range(3):
		# 	# grab the last 21 bits with bitand
		# 	twentyone_bits = first & 0b111111111111111111111
		# 	first >>= 21
		# 	print(bin(twentyone_bits))
		unpack_int64_vector(self.verts_data["pos"], self.vertices, self.residues)
		# int21_vec = np.copy(self.vertices)
		scale_unpack_vectorized(self.vertices, self.base)

		# print("start")
		# # print(int21_vec)
		# scale_pack_vectorized(self.vertices, self.base)
		# # print(self.vertices)
		# print("int21_vec", np.allclose(int21_vec, self.vertices))
		# pack_int64_vector(self.verts_data["pos"], self.vertices.astype(np.int64), self.residues)
		# for v in (int21_vec[0], self.vertices[0]):
		# 	print([bin(int(c)) for c in v])
		# print(bin(before[0]), type(before[0]))
		# print(bin(self.verts_data["pos"][0]))
		# print("packed int64", np.allclose(before, self.verts_data["pos"]))

		unpack_ubyte_vector(self.normals)
		unpack_ubyte_vector(self.tangents)
		unpack_swizzle_vectorized(self.vertices)
		unpack_swizzle_vectorized(self.normals)
		unpack_swizzle_vectorized(self.tangents)

		# unpack the shapekeys
		if self.shapekeys is not None:
			shapes_combined = self.verts_data["shapekeys1"].astype(np.int64)
			shapes_combined <<= 32
			shapes_combined |= self.verts_data["shapekeys0"]
			unpack_int64_vector(shapes_combined, self.shapekeys, self.shape_residues)
			scale_unpack_vectorized(self.shapekeys, self.base)
			unpack_swizzle_vectorized(self.shapekeys)

		for vertex_index, res in enumerate(self.residues):
			self.add_to_weights("residue", vertex_index, res)
		logging.info(f"Unpacked mesh in {time.time() - start_time:.2f} seconds")

	def set_verts(self, verts):
		"""Store verts as flat lists for each component"""
		# need to update the count here
		self.vertices, self.residues, self.normals, self.windings, self.tangents, self.uvs, \
		self.colors, self.weights, self.shapekeys = zip(*verts)
		# if packing isn't done right after set_verts the plugin chokes, but that is probably just due tris setter
		self.pack_verts()

	def pack_verts(self):
		"""Repack flat lists into verts_data"""
		logging.info("Packing vertices")
		# get dtype according to which the vertices are packed
		self.update_dtype()
		self.verts_data = np.zeros(len(self.vertices), dtype=self.dt)

		if not isinstance(self.vertices, np.ndarray):
			self.vertices = np.array(self.vertices, dtype=np.float32)
		if not isinstance(self.residues, np.ndarray):
			self.residues = np.array(self.residues, dtype=np.bool)
		pack_swizzle_vectorized(self.vertices)
		scale_pack_vectorized(self.vertices, self.base)
		pack_int64_vector(self.verts_data["pos"], self.vertices.astype(np.int64), self.residues)
		for i, vert in enumerate(self.verts_data):
			# residue = 1 -> 4 bones per vertex, no alpha blending
			# residue = 0 -> 1 bone per vertex, alpha blending (whiskers)
			vert["normal"] = pack_ubyte_vector(pack_swizzle(self.normals[i]))
			vert["tangent"] = pack_ubyte_vector(pack_swizzle(self.tangents[i]))

			# winding seems to be a bitflag (flipped UV toggles the first bit of all its vertices to 1)
			# 0 = natural winding matching the geometry
			# 128 = UV's winding is flipped / inverted compared to geometry
			vert["winding"] = self.windings[i] * 128
			# bone index of the strongest weight
			if self.weights[i]:
				vert["bone index"] = self.weights[i][0][0]
			# else:
			# 	print(f"bad weight {i}, {self.weights[i]}")
			if "bone ids" in self.dt.fields:
				vert["bone ids"], vert["bone weights"] = self.unpack_weights_list(self.weights[i])
			if "uvs" in self.dt.fields:
				vert["uvs"] = list(pack_ushort_vector(uv) for uv in self.uvs[i])
			if "colors" in self.dt.fields:
				vert["colors"] = list(list(round(c * 255) for c in vcol) for vcol in self.colors[i])
			if "shapekeys0" in self.dt.fields:
				# first pack it as uint64
				raw_packed = pack_longint_vec(pack_swizzle(self.shapekeys[i]), residue, self.base)
				if raw_packed < 0:
					logging.error(f"Shapekey {raw_packed} could not be packed into uint64")
					raw_packed = 0
				raw_bytes = struct.pack("Q", raw_packed)
				# unpack to 2 uints again and assign data
				first, second = struct.unpack("LL", raw_bytes)
				vert["shapekeys0"] = first
				vert["shapekeys1"] = second

	def unpack_weights_list(self, weights_sorted):
		# pad the weight list to 4 bones, ie. add empty bones if missing
		for i in range(0, 4 - len(weights_sorted)):
			weights_sorted.append([0, 0])
		assert len(weights_sorted) == 4
		ids, weights = zip(*weights_sorted)
		return ids, self.quantize_bone_weights(weights)


