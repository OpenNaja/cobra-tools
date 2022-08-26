
import logging
import time
from generated.formats.ms2.compounds.packing_utils import *


import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ms2.bitfields.ModelFlag import ModelFlag
from generated.formats.ms2.compounds.MeshData import MeshData


class NewMeshData(MeshData):

	"""
	PZ, JWE2 - 64 bytes incl. inheritance
	"""

	__name__ = 'NewMeshData'

	_import_path = 'generated.formats.ms2.compounds.NewMeshData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.vertex_count = 0

		# number of index entries in the triangle index list; (not: number of triangles, byte count of tri buffer)
		self.tri_index_count = 0

		# always zero
		self.zero_1 = 0

		# power of 2 increasing with lod index
		self.poweroftwo = 0

		# in bytes
		self.vertex_offset = 0

		# usually 48
		self.size_of_vertex = 0

		# in bytes
		self.tri_offset = 0

		# always zero
		self.zero_2 = 0

		# some floats, purpose unknown
		self.unk_floats = Array((0,), Float, self.context, 0, None)

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

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.vertex_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.tri_index_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.zero_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.poweroftwo = Uint.from_stream(stream, instance.context, 0, None)
		instance.vertex_offset = Uint.from_stream(stream, instance.context, 0, None)
		instance.size_of_vertex = Uint.from_stream(stream, instance.context, 0, None)
		instance.tri_offset = Uint.from_stream(stream, instance.context, 0, None)
		instance.zero_2 = Uint.from_stream(stream, instance.context, 0, None)
		instance.unk_floats = Array.from_stream(stream, instance.context, 0, None, (2,), Float)
		instance.zero_3 = Uint.from_stream(stream, instance.context, 0, None)
		instance.flag = ModelFlag.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.vertex_count)
		Uint.to_stream(stream, instance.tri_index_count)
		Uint.to_stream(stream, instance.zero_1)
		Uint.to_stream(stream, instance.poweroftwo)
		Uint.to_stream(stream, instance.vertex_offset)
		Uint.to_stream(stream, instance.size_of_vertex)
		Uint.to_stream(stream, instance.tri_offset)
		Uint.to_stream(stream, instance.zero_2)
		Array.to_stream(stream, instance.unk_floats, (2,), Float, instance.context, 0, None)
		Uint.to_stream(stream, instance.zero_3)
		ModelFlag.to_stream(stream, instance.flag)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'vertex_count', Uint, (0, None), (False, None)
		yield 'tri_index_count', Uint, (0, None), (False, None)
		yield 'zero_1', Uint, (0, None), (False, None)
		yield 'poweroftwo', Uint, (0, None), (False, None)
		yield 'vertex_offset', Uint, (0, None), (False, None)
		yield 'size_of_vertex', Uint, (0, None), (False, None)
		yield 'tri_offset', Uint, (0, None), (False, None)
		yield 'zero_2', Uint, (0, None), (False, None)
		yield 'unk_floats', Array, ((2,), Float, 0, None), (False, None)
		yield 'zero_3', Uint, (0, None), (False, None)
		yield 'flag', ModelFlag, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'NewMeshData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* vertex_count = {self.fmt_member(self.vertex_count, indent+1)}'
		s += f'\n	* tri_index_count = {self.fmt_member(self.tri_index_count, indent+1)}'
		s += f'\n	* zero_1 = {self.fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* poweroftwo = {self.fmt_member(self.poweroftwo, indent+1)}'
		s += f'\n	* vertex_offset = {self.fmt_member(self.vertex_offset, indent+1)}'
		s += f'\n	* size_of_vertex = {self.fmt_member(self.size_of_vertex, indent+1)}'
		s += f'\n	* tri_offset = {self.fmt_member(self.tri_offset, indent+1)}'
		s += f'\n	* zero_2 = {self.fmt_member(self.zero_2, indent+1)}'
		s += f'\n	* unk_floats = {self.fmt_member(self.unk_floats, indent+1)}'
		s += f'\n	* zero_3 = {self.fmt_member(self.zero_3, indent+1)}'
		s += f'\n	* flag = {self.fmt_member(self.flag, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s

	# @property
	def get_stream_index(self):
		# logging.debug(f"Using stream {self.stream_info.offset}")
		return self.stream_info.offset

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
				("colors", np.ubyte, 4),  # these appear to be directional vectors
				("zeros0", np.int32)
			])
		elif self.flag == 513:
			dt.extend([
				("uvs", np.ushort, (2, 2)),
				# ("colors", np.ubyte, 4),
				("zeros2", np.uint64, (3,))
			])
		elif self.flag == 512:
			dt.extend([
				# last lod of many tree meshes (eg. tree_birch_white_03)
				# 8 uvs for an impostor texture atlas aka flipbook
				# a different unpacking factor is used here
				("uvs", np.ushort, (8, 2)),
			])
		elif self.flag == 517:
			dt.extend([
				("uvs", np.ushort, (1, 2)),
				("shapekeys0", np.uint32),
				("colors", np.ubyte, 4),  # this appears to be normals, or something similar
				("shapekeys1", np.int32),
				# sometimes, only the last is set, the rest being 00 00 C0 7F (NaN)
				("floats", np.float32, 4),
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
		self.fur_length = 0.0
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# create arrays for the unpacked ms2_file
		self.init_arrays()
		# create array to populate with packed vertices
		self.verts_data = np.empty(dtype=self.dt, shape=self.vertex_count)
		# read the packed data
		self.buffer_info.verts.seek(self.vertex_offset)
		self.buffer_info.verts.readinto(self.verts_data)
		# logging.debug(f"Reading {self.vertex_count} verts at {self.buffer_info.verts.tell()}")
		# first cast to the float uvs array so unpacking doesn't use int division
		self.uvs[:] = self.verts_data["uvs"]
		if self.flag == 512:
			unpack_ushort_vector_impostor(self.uvs)
		else:
			unpack_ushort_vector(self.uvs)
		if self.get_vcol_count():
			# first cast to the float colors array so unpacking doesn't use int division
			self.colors[:] = self.verts_data["colors"]
			unpack_ubyte_color(self.colors)
		# todo - PZ uses at least bits 4, 5, 6 with a random pattern, while JWE2 pre-Biosyn uses really just the one bit
		self.negate_bitangents[:] = (self.verts_data["winding"] >> 7) & 1
		self.normals[:] = self.verts_data["normal"]
		self.tangents[:] = self.verts_data["tangent"]
		if "floats" in self.dt.fields:
			self.floats[:] = self.verts_data["floats"]
		start_time = time.time()
		unpack_int64_vector(self.verts_data["pos"], self.vertices, self.use_blended_weights)
		scale_unpack_vectorized(self.vertices, self.pack_base)
		if "bone weights" in self.dt.fields:
			bone_weights = self.verts_data["bone weights"].astype(np.float32) / 255
			self.get_blended_weights(self.verts_data["bone ids"], bone_weights)
		self.get_static_weights(self.verts_data["bone index"], self.use_blended_weights)

		unpack_ubyte_vector(self.normals)
		unpack_ubyte_vector(self.tangents)
		unpack_swizzle_vectorized(self.vertices)
		unpack_swizzle_vectorized(self.normals)
		unpack_swizzle_vectorized(self.tangents)

		# unpack the shapekeys
		if self.flag == 517:
			# create the int64 by combining its two parts
			shapes_combined = self.verts_data["shapekeys1"].astype(np.int64)
			shapes_combined <<= 32
			shapes_combined |= self.verts_data["shapekeys0"]
			unpack_int64_vector(shapes_combined, self.shapekeys, self.shape_residues)
			scale_unpack_vectorized(self.shapekeys, self.pack_base)
			unpack_swizzle_vectorized(self.shapekeys)
		#
		# for bit in range(0, 8):
		# 	for vertex_index, res in enumerate((self.verts_data["winding"] >> bit) & 1):
		# 		# self.add_to_weights(f"bit{bit}", vertex_index, res/128)
		# 		self.add_to_weights(f"bit{bit}", vertex_index, res)
		logging.info(f"Unpacked mesh in {time.time() - start_time:.2f} seconds")

	def pack_verts(self):
		"""Repack flat lists into verts_data"""
		logging.info("Packing vertices")
		self.verts_data = np.zeros(self.vertex_count, dtype=self.dt)

		if self.flag == 517:
			pack_swizzle_vectorized(self.shapekeys)
			scale_pack_vectorized(self.shapekeys, self.pack_base)
			shapes_combined = np.zeros(self.vertex_count, dtype=np.int64)
			# todo - store separate shape_residues?
			pack_int64_vector(shapes_combined, self.shapekeys.astype(np.int64), self.use_blended_weights)
			self.verts_data["shapekeys1"][:] = (shapes_combined >> 32) & 0b11111111111111111111111111111111
			self.verts_data["shapekeys0"][:] = shapes_combined & 0b11111111111111111111111111111111

		pack_swizzle_vectorized(self.vertices)
		pack_swizzle_vectorized(self.normals)
		pack_swizzle_vectorized(self.tangents)
		# print(self.use_blended_weights)
		scale_pack_vectorized(self.vertices, self.pack_base)
		pack_int64_vector(self.verts_data["pos"], self.vertices.astype(np.int64), self.use_blended_weights)
		pack_ubyte_vector(self.normals)
		pack_ubyte_vector(self.tangents)
		if self.flag == 512:
			pack_ushort_vector_impostor(self.uvs)
		else:
			pack_ushort_vector(self.uvs)
		self.verts_data["normal"] = self.normals
		self.verts_data["tangent"] = self.tangents
		self.verts_data["uvs"] = self.uvs
		if "floats" in self.dt.fields:
			self.verts_data["floats"] = self.floats
		if self.get_vcol_count():
			self.colors = np.array(self.colors)
			pack_ubyte_color(self.colors)
			self.verts_data["colors"] = self.colors
		# winding is a bitfield
		# 0 = UV orientation matching the geometry
		# 128 = inverted UV orientation = bitangent
		self.verts_data["winding"] = self.negate_bitangents << 7
		# non-vectorized data
		for vert, weight in zip(self.verts_data, self.weights):
			# bone index of the strongest weight
			if weight:
				vert["bone index"] = weight[0][0]
			# else:
			# 	print(f"bad weight {i}, {self.weights[i]}")
			if "bone ids" in self.dt.fields:
				vert["bone ids"], vert["bone weights"] = self.unpack_weights_list(weight)

