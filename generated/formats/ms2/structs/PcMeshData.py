import math
import logging
import numpy as np

from generated.formats.base.structs.PadAlign import get_padding
from generated.formats.ms2.structs.packing_utils import *
from generated.formats.ms2.imports import name_type_map
from generated.formats.ms2.structs.MeshData import MeshData


class PcMeshData(MeshData):

	"""
	72 bytes total
	"""

	__name__ = 'PcMeshData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# repeat
		self.tri_index_count_a = name_type_map['Uint'](self.context, 0, None)
		self.vertex_count = name_type_map['Uint'](self.context, 0, None)

		# x*16 = offset
		self.tri_offset = name_type_map['Uint'](self.context, 0, None)

		# number of index entries in the triangle index list; (not: number of triangles, byte count of tri buffer)
		self.tri_index_count = name_type_map['Uint'](self.context, 0, None)

		# x*16 = offset
		self.vertex_offset = name_type_map['Uint'](self.context, 0, None)

		# x*16 = offset
		self.weights_offset = name_type_map['Uint'](self.context, 0, None)

		# x*16 = offset
		self.uv_offset = name_type_map['Uint'](self.context, 0, None)

		# x*16 = offset
		self.uv_offset_2 = name_type_map['Uint'](self.context, 0, None)

		# x*16 = offset
		self.vertex_color_offset = name_type_map['Uint'](self.context, 0, None)

		# cumulative count of vertices in mesh's lod before this mesh
		self.vertex_offset_within_lod = name_type_map['Uint'](self.context, 0, None)

		# power of 2 increasing with lod index
		self.poweroftwo = name_type_map['Uint'](self.context, 0, None)
		self.zero_b = name_type_map['Uint'].from_value(0)

		# ?
		self.unk_float_0 = name_type_map['Float'](self.context, 0, None)

		# bitfield
		self.flag = name_type_map['ModelFlag'](self.context, 0, None)
		self.zero_c = name_type_map['Uint'].from_value(0)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'tri_index_count_a', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'vertex_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'tri_offset', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'tri_index_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'vertex_offset', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'weights_offset', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'uv_offset', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'uv_offset_2', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'vertex_color_offset', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'vertex_offset_within_lod', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'poweroftwo', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'zero_b', name_type_map['Uint'], (0, None), (False, 0), (None, None)
		yield 'unk_float_0', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'flag', name_type_map['ModelFlag'], (0, None), (False, None), (None, None)
		yield 'zero_c', name_type_map['Uint'], (0, None), (False, 0), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'tri_index_count_a', name_type_map['Uint'], (0, None), (False, None)
		yield 'vertex_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'tri_offset', name_type_map['Uint'], (0, None), (False, None)
		yield 'tri_index_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'vertex_offset', name_type_map['Uint'], (0, None), (False, None)
		yield 'weights_offset', name_type_map['Uint'], (0, None), (False, None)
		yield 'uv_offset', name_type_map['Uint'], (0, None), (False, None)
		yield 'uv_offset_2', name_type_map['Uint'], (0, None), (False, None)
		yield 'vertex_color_offset', name_type_map['Uint'], (0, None), (False, None)
		yield 'vertex_offset_within_lod', name_type_map['Uint'], (0, None), (False, None)
		yield 'poweroftwo', name_type_map['Uint'], (0, None), (False, None)
		yield 'zero_b', name_type_map['Uint'], (0, None), (False, 0)
		yield 'unk_float_0', name_type_map['Float'], (0, None), (False, None)
		yield 'flag', name_type_map['ModelFlag'], (0, None), (False, None)
		yield 'zero_c', name_type_map['Uint'], (0, None), (False, 0)

	def get_uv_count(self):
		# apparently not correlated to flag, walker: {(False, 9), (False, 25), (True, 25), (True, 9)}
		if self.uv_offset_2:
			return 2
		# elif self.uv_offset:
		# 	return 1
		return 1

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
		dt_uv = [
			("uvs", np.ushort, 2),
		]
		dt_w = [
			("bone ids", np.ubyte, (4,)),
			("bone weights", np.ubyte, (4,)),
		]
		self.dt = np.dtype(dt)
		self.dt_uv = np.dtype(dt_uv)
		self.dt_w = np.dtype(dt_w)
		self.update_shell_count()
		# logging.debug(f"PC size of vertex: {self.dt.itemsize}")
		# logging.debug(f"PC size of uv: {self.dt_uv.itemsize}")
		# logging.debug(f"PC size of weights: {self.dt_w.itemsize}")

	def read_pc_array(self, dt, offset, count):
		arr = np.empty(dtype=dt, shape=count)
		self.buffer_info.verts.seek(offset * 16)
		# logging.debug(f"VERTS at {self.buffer_info.verts.tell()}")
		self.buffer_info.verts.readinto(arr)
		return arr

	def write_pc_array(self, arr):
		padding = get_padding(self.buffer_info.verts.tell(), alignment=16)
		self.buffer_info.verts.write(padding)
		offset = self.buffer_info.verts.tell()
		self.buffer_info.verts.write(arr.tobytes())
		# to be safe, also write padding at the end
		padding = get_padding(self.buffer_info.verts.tell(), alignment=16)
		self.buffer_info.verts.write(padding)
		return offset // 16

	def read_verts(self):
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# read vertices of this mesh
		self.verts_data = self.read_pc_array(self.dt, self.vertex_offset, self.vertex_count)
		self.uv_data = self.read_pc_array(self.dt_uv, self.uv_offset, self.vertex_count)
		self.uv_data_2 = self.read_pc_array(self.dt_uv, self.uv_offset_2, self.vertex_count)
		self.weights_data = self.read_pc_array(self.dt_w, self.weights_offset, self.vertex_count)
		# create arrays for the unpacked ms2_file
		self.init_arrays()
		# first cast to the float uvs array so unpacking doesn't use int division
		self.uvs[:, 0] = self.uv_data["uvs"]
		if self.get_uv_count() == 2:
			self.uvs[:, 1] = self.uv_data_2["uvs"]
		self.normals[:] = self.verts_data["normal"]
		self.tangents[:] = self.verts_data["tangent"]
		unpack_ushort_vector(self.uvs)
		unpack_int64_vector(self.verts_data["pos"], self.vertices, self.use_blended_weights)
		scale_unpack_vectorized(self.vertices, self.pack_base)
		unpack_ubyte_vector(self.normals)
		unpack_ubyte_vector(self.tangents)
		unpack_swizzle_vectorized(self.vertices)
		unpack_swizzle_vectorized(self.normals)
		unpack_swizzle_vectorized(self.tangents)

		# PC does not use use_blended_weights, nor a flag
		# PC ostrich download has self.weights_offset = 0 for eyes and lashes, which consequently get wrong weights
		self.use_weights = self.weights_offset != 0
		if self.use_weights:
			self.bone_indices[:] = self.weights_data["bone ids"]
			self.bone_weights[:] =  self.weights_data["bone weights"].astype(np.float32) / 255
		else:
			for v_i, use_blended_weights in enumerate(self.use_blended_weights):
				if not use_blended_weights:
					self.bone_indices[v_i] = (self.verts_data["bone index"][v_i], -1, -1, -1)
					self.bone_weights[v_i] = (1.0, 0.0, 0.0, 0.0)
		# print(self.verts_data["winding"])
		for bit in range(0, 8):
			for vertex_index, res in enumerate((self.verts_data["winding"] >> bit) & 1):
				self.add_to_weights(f"bit{bit}", vertex_index, res)
		self.mesh_in_lod = self.verts_data["winding"][0] & 0b111111
		self.negate_bitangents = (self.verts_data["winding"] >> 6) & 1
		# print(self.vertices)

	def pack_verts(self):
		"""Repack flat lists into verts_data"""
		logging.info("Packing vertices")
		self.verts_data = np.zeros(self.vertex_count, dtype=self.dt)
		self.weights_data = np.zeros(self.vertex_count, dtype=self.dt_w)
		self.uv_data = np.zeros(self.vertex_count, dtype=self.dt_uv)
		self.uv_data_2 = np.zeros(self.vertex_count, dtype=self.dt_uv)
		pack_swizzle_vectorized(self.vertices)
		pack_swizzle_vectorized(self.normals)
		pack_swizzle_vectorized(self.tangents)
		# print(self.use_blended_weights)
		scale_pack_vectorized(self.vertices, self.pack_base)
		pack_int64_vector(self.verts_data["pos"], self.vertices.astype(np.int64), self.use_blended_weights)
		pack_ubyte_vector(self.normals)
		pack_ubyte_vector(self.tangents)
		pack_ushort_vector(self.uvs)
		self.verts_data["normal"] = self.normals
		self.verts_data["tangent"] = self.tangents
		self.uv_data["uvs"] = self.uvs[:, 0]
		if self.get_uv_count() == 2:
			self.uv_data_2["uvs"] = self.uvs[:, 1]

		# determine from weights data
		if set(len(w) for w in self.weights) == {1, }:
			self.use_weights = False
		else:
			self.use_weights = True

		# winding is a bitfield
		self.verts_data["winding"] = self.mesh_in_lod
		self.verts_data["winding"] |= self.negate_bitangents << 6

		# non-vectorized data
		for vert, weight, weight_target in zip(self.verts_data, self.weights, self.weights_data):
			# bone index of the strongest weight
			if weight:
				vert["bone index"] = weight[0][0]
			weight_target["bone ids"], weight_target["bone weights"] = self.unpack_weights_list(weight)

	def read_tris(self):
		# tris are stored in the verts stream for PC
		# read all tri indices for this mesh, but only as many as needed if there are shells
		index_count = self.tri_index_count // self.shell_count
		self.tri_indices = self.read_pc_array(np.uint16, self.tri_offset, index_count)

	def write_verts(self):
		self.vertex_count = len(self.verts_data)
		self.vertex_offset = self.write_pc_array(self.verts_data)

	def write_weights(self):
		if self.use_weights:
			self.weights_offset = self.write_pc_array(self.weights_data)
		else:
			self.weights_offset = 0

	def write_tris(self):
		self.tri_index_count = self.tri_index_count_a = len(self.tri_indices) * self.shell_count
		self.tri_offset = self.write_pc_array(self.tri_indices)
		# todo shells?
		# extend tri array according to shell count
		# for shell in range(self.shell_count-1):
		# 	self.write_pc_array(self.tri_indices)

	def write_uvs(self):
		self.uv_offset = self.write_pc_array(self.uv_data)

	def write_uvs_2(self):
		if self.get_uv_count() == 2:
			self.uv_offset_2 = self.write_pc_array(self.uv_data_2)
		else:
			self.uv_offset_2 = 0

	def write_data(self):
		# order separately: verts, weights, tris, uvs
		pass

