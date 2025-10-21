import logging
import time

from generated.formats.ms2.structs.MeshData import MeshData
from generated.formats.ms2.structs.packing_utils import *


from generated.formats.ms2.imports import name_type_map
from generated.formats.ms2.structs.MeshData import MeshData


class NewMeshData(MeshData):

	"""
	PZ, JWE2 - 64 bytes incl. inheritance
	"""

	__name__ = 'NewMeshData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.vertex_count = name_type_map['Uint'](self.context, 0, None)

		# number of index entries in the triangle index list; (not: number of triangles, byte count of tri buffer)
		self.tri_index_count = name_type_map['Uint'](self.context, 0, None)

		# always zero
		self.zero_1 = name_type_map['Uint'](self.context, 0, None)

		# power of 2 increasing with lod index
		self.poweroftwo = name_type_map['Uint'](self.context, 0, None)

		# in bytes
		self.vertex_offset = name_type_map['Uint'](self.context, 0, None)
		self.size_of_vertex = name_type_map['Uint'].from_value(48)

		# in bytes
		self.tri_offset = name_type_map['Uint'](self.context, 0, None)

		# always zero
		self.zero_2 = name_type_map['Uint'](self.context, 0, None)

		# ?
		self.unk_float_0 = name_type_map['Float'](self.context, 0, None)

		# ?
		self.unk_float_1 = name_type_map['Float'](self.context, 0, None)

		# always zero
		self.zero_3 = name_type_map['Uint'](self.context, 0, None)

		# bitfield, determines vertex format
		self.flag = name_type_map['ModelFlag'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'vertex_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'tri_index_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'zero_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'poweroftwo', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'vertex_offset', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'size_of_vertex', name_type_map['Uint'], (0, None), (False, 48), (None, None)
		yield 'tri_offset', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'zero_2', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_float_0', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_float_1', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'zero_3', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'flag', name_type_map['ModelFlag'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'vertex_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'tri_index_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'zero_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'poweroftwo', name_type_map['Uint'], (0, None), (False, None)
		yield 'vertex_offset', name_type_map['Uint'], (0, None), (False, None)
		yield 'size_of_vertex', name_type_map['Uint'], (0, None), (False, 48)
		yield 'tri_offset', name_type_map['Uint'], (0, None), (False, None)
		yield 'zero_2', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_float_0', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_float_1', name_type_map['Float'], (0, None), (False, None)
		yield 'zero_3', name_type_map['Uint'], (0, None), (False, None)
		yield 'flag', name_type_map['ModelFlag'], (0, None), (False, None)

	# @property
	def get_stream_index(self):
		# logging.debug(f"Using stream {self.stream_info.pool_index}")
		return self.stream_info.pool_index

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
		if self.flag.weights:
			if self.flag.unk == 0:
				# used exclusively on alpha blended hair cards (528)
				dt.extend([
					("uvs", np.ushort, (1, 2)),
					("zeros0", np.int32, (3,))
				])
			elif self.flag.unk == 1:
				# animal eyes, skin or feathers without alpha blending (529)
				dt.extend([
					("uvs", np.ushort, (2, 2)),
					("zeros0", np.int32, (2,))
				])
			elif self.flag.unk == 5:
				# animal fur or skin (533, 565, 821, 853, 885, 1013)
				dt.extend([
					("uvs", np.ushort, (2, 2)),  # second UV is either fins texcoords or fur length and shell tile scale
					("colors", np.ubyte, 4),  # fur direction
					("zeros0", np.int32)
				])
			# blended bone weights
			dt.extend([
				("bone ids", np.ubyte, (4,)),
				("bone weights", np.ubyte, (4,)),
				("zeros1", np.uint64)
			])
		else:
			if self.flag in (512,):
				dt.extend([
					# last lod of many tree meshes (eg. tree_birch_white_03)
					# 8 uvs for an impostor texture atlas aka flipbook
					# a different unpacking factor is used here
					("uvs", np.ushort, (8, 2)),
				])
			elif self.flag == 513:
				dt.extend([
					("uvs", np.ushort, (2, 2)),
					("zeros2", np.uint64, (3,))
				])
			elif self.flag == 517:
				# there is a version of 517 that has no shape keys, but 2 uv layers
				if self.expect_shapekeys:
					dt.extend([
						("uvs", np.ushort, (1, 2)),
						("lod_key_0", np.uint32),
						("normal_custom", np.ubyte, 3),  # edited normal
						("wind", np.ubyte),  # not sure for PZ
						("lod_key_1", np.int32),
						("center_key", np.float32, 3),  # may be 00 00 C0 7F (NaN)
						("whatever", np.float32),  # unlike JWE2 this is likely encoded as float
					])
				else:
					dt.extend([
						("uvs", np.ushort, (2, 2)),
						("colors", np.ubyte, 4),  # real color on PZ reward_statues
						("zeros", np.int32, 5),
					])
			elif self.flag == 545:
				dt.extend([
					# cz_glasspanel_4m_02.mdl2
					("uvs", np.ushort, (1, 2)),
					("zeros2", np.uint32, (7,)),
				])
			elif self.flag in (549,):  # PZ c2 GL_Roof_02
				dt.extend([
					("uvs", np.ushort, (2, 2)),  # only saw UV0 used
					("colors", np.ubyte, 4),  # maybe actual vertex color? all 1 in the cases I saw
					("zeros0", np.int32, (5,))  # no weights
				])
		self.dt = np.dtype(dt)
		self.update_shell_count()
		if self.dt.itemsize != self.size_of_vertex:
			raise AttributeError(
				f"Vertex size for flag {self.flag} is wrong! Collected {self.dt.itemsize}, expected {self.size_of_vertex} bytes.")

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
		unpack_int64_vector(self.verts_data["pos"], self.vertices, self.use_blended_weights)
		scale_unpack_vectorized(self.vertices, self.pack_base)
		if "bone weights" in self.dt.fields:
			self.bone_indices[:] = self.verts_data["bone ids"]
			self.bone_weights[:] = self.verts_data["bone weights"].astype(np.float32) / 255
		for v_i, use_blended_weights in enumerate(self.use_blended_weights):
			if not use_blended_weights:
				self.bone_indices[v_i] = (self.verts_data["bone index"][v_i], -1, -1, -1)
				self.bone_weights[v_i] = (1.0, 0.0, 0.0, 0.0)

		unpack_ubyte_vector(self.normals)
		unpack_ubyte_vector(self.tangents)
		unpack_swizzle_vectorized(self.vertices)
		unpack_swizzle_vectorized(self.normals)
		unpack_swizzle_vectorized(self.tangents)

		# unpack the lod_keys
		if self.is_speedtree:
			# create the int64 by combining its two parts
			shapes_combined = self.verts_data["lod_key_1"].astype(np.int64)
			shapes_combined <<= 32
			shapes_combined |= self.verts_data["lod_key_0"]
			unpack_int64_vector(shapes_combined, self.lod_keys, self.shape_residues)
			scale_unpack_vectorized(self.lod_keys, self.pack_base)
			unpack_swizzle_vectorized(self.lod_keys)

			self.normals_custom[:] = self.verts_data["normal_custom"]
			self.wind[:] = self.verts_data["wind"]
			self.whatever[:] = self.verts_data["whatever"]
			self.center_keys[:] = self.verts_data["center_key"]
			unpack_ubyte_vector(self.normals_custom)
			unpack_swizzle_vectorized(self.normals_custom)
			unpack_ubyte_color(self.wind)
			unpack_swizzle_vectorized(self.center_keys)
			for vertex_index, weight in enumerate(self.wind):
				self.add_to_weights("wind", vertex_index, weight)

			self.whatever_range = np.max(self.whatever)
			if self.whatever_range > 0.0:
				self.whatever /= self.whatever_range
			# print(self.whatever)
			for vertex_index, weight in enumerate(self.whatever):
				self.add_to_weights("whatever", vertex_index, weight)

		# for bit in range(0, 8):
		# 	for vertex_index, res in enumerate((self.verts_data["winding"] >> bit) & 1):
		# 		self.add_to_weights(f"bit{bit}", vertex_index, res)
		# logging.debug(f"Unpacked mesh in {time.time() - start_time:.2f} seconds")

	@property
	def is_speedtree(self):
		return self.flag == 517 and self.expect_shapekeys

	def pack_verts(self):
		"""Repack flat lists into verts_data"""
		logging.info("Packing vertices")
		self.verts_data = np.zeros(self.vertex_count, dtype=self.dt)

		if self.is_speedtree:
			pack_swizzle_vectorized(self.lod_keys)
			scale_pack_vectorized(self.lod_keys, self.pack_base)
			shapes_combined = np.zeros(self.vertex_count, dtype=np.int64)
			# todo - store separate shape_residues?
			pack_int64_vector(shapes_combined, self.lod_keys.astype(np.int64), self.use_blended_weights)
			self.verts_data["lod_key_1"][:] = (shapes_combined >> 32) & 0b11111111111111111111111111111111
			self.verts_data["lod_key_0"][:] = shapes_combined & 0b11111111111111111111111111111111

			pack_swizzle_vectorized(self.normals_custom)
			pack_swizzle_vectorized(self.center_keys)
			pack_ubyte_vector(self.normals_custom)
			pack_ubyte_color(self.wind)
			self.verts_data["normal_custom"][:] = self.normals_custom
			self.verts_data["wind"][:] = self.wind
			self.verts_data["center_key"][:] = self.center_keys
			self.verts_data["whatever"][:] = self.whatever
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

	def resize_vertices(self, model_info, fac):
		self.vertices *= fac
		self.pack_base = model_info.pack_base
		pack_swizzle_vectorized(self.vertices)
		scale_pack_vectorized(self.vertices, self.pack_base)
		pack_int64_vector(self.verts_data["pos"], self.vertices.astype(np.int64), self.use_blended_weights)

