# START_GLOBALS
import logging
import math
from itertools import pairwise

import numpy as np

from generated.formats.ms2.structs.packing_utils import FUR_OVERHEAD, remap, PACKEDVEC_MAX
from ovl_util.tristrip import triangulate, stripify


# END_GLOBALS


class MeshData:

	# START_CLASS

	@property
	def is_speedtree(self):
		return False

	# @property
	def get_stream_index(self):
		# logging.debug(f"Using stream {self.stream_index}")
		return self.stream_index

	def get_vcol_count(self, ):
		if "colors" in self.dt.fields:
			return 1
			# return self.dt["colors"].shape[0]
		return 0

	def get_uv_count(self, ):
		if "uvs" in self.dt.fields:
			return self.dt["uvs"].shape[0]
		return 0

	def assign_buffer_info(self, buffer_infos):
		self.buffer_info = buffer_infos[self.get_stream_index()]

	def guess_size(self, val, offset, count):
		# self.buffer_info.uvs_offsets
		try:
			sorted_l = list(sorted(val))
			i = sorted_l.index(offset)
			next_offset = sorted_l[i+1]
			return (next_offset-offset) // count
		except:
			logging.exception(f"Size value guessing failed")
			return 0

	def populate(self, pack_base=512, expect_shapekeys=True):
		self.mesh_format = None
		self.pack_base = pack_base
		self.expect_shapekeys = expect_shapekeys
		self.lod_keys = None
		self.read_verts()
		self.read_tris()
		# self.validate_tris()

	def init_arrays(self):
		# create arrays for this mesh, set to zero to avoid underflow errors when unpacking arrays that weren't filled
		self.vertices = np.zeros((self.vertex_count, 3), np.float32)
		self.normals = np.zeros((self.vertex_count, 3), np.float32)
		self.normals_custom = np.zeros((self.vertex_count, 3), np.float32)
		self.tangents = np.zeros((self.vertex_count, 3), np.float32)
		self.use_blended_weights = np.zeros(self.vertex_count, np.uint8)
		self.shape_residues = np.zeros(self.vertex_count, np.uint8)
		self.negate_bitangents = np.zeros(self.vertex_count, np.uint8)
		self.wind = np.zeros(self.vertex_count, np.float32)
		self.whatever = np.zeros(self.vertex_count, np.float32)
		self.uvs = np.zeros((self.vertex_count, self.get_uv_count(), 2), np.float32)
		self.colors = np.zeros((self.vertex_count, 4), np.float32)
		self.center_keys = np.zeros((self.vertex_count, 3), np.float32)
		self.lod_keys = np.zeros((self.vertex_count, 3), np.float32)
		self.bone_indices = np.zeros((self.vertex_count, 4), np.short)
		self.bone_weights = np.zeros((self.vertex_count, 4), np.float32)
		self.weights_info = {}

	def set_verts(self, verts):
		"""Store verts as flat lists for each component"""
		# need to update the count here
		# use_blended_weights = 1 -> 4 bones per vertex, no alpha blending
		# use_blended_weights = 0 -> 1 bone per vertex, alpha blending (whiskers)
		self.vertex_count = len(verts)
		self.update_dtype()
		self.init_arrays()
		self.vertices[:], self.use_blended_weights[:], self.normals[:], self.normals_custom[:], self.negate_bitangents[:], self.tangents[:], self.uvs[:], \
		self.colors[:], self.weights, self.wind[:], self.whatever[:], self.lod_keys[:], self.center_keys[:] = zip(*verts)
		# if packing isn't done right after set_verts the plugin chokes, but that is probably just due tris setter
		self.pack_verts()

	def pack_verts(self):
		pass

	def write_data(self):
		# write to the buffer_info that has been assigned to mesh
		self.vertex_offset = self.buffer_info.verts.tell()
		self.tri_offset = self.buffer_info.tris.tell()
		self.vertex_count = len(self.verts_data)
		self.tri_index_count = len(self.tri_indices) * self.shell_count
		# write vertices
		self.buffer_info.verts.write(self.verts_data.tobytes())
		# write tris
		tri_bytes = self.tri_indices.tobytes()
		# extend tri array according to shell count
		logging.debug(f"Writing {self.shell_count} shells of {len(self.tri_indices)} triangles")
		for shell in range(self.shell_count):
			self.buffer_info.tris.write(tri_bytes)

	def read_tris(self):
		# read all tri indices for this mesh, but only as many as needed if there are shells
		self.buffer_info.tris.seek(self.tri_offset)
		index_count = self.tri_index_count // self.shell_count
		# logging.debug(f"Reading {index_count} indices at {self.buffer_info.tris.tell()}")
		self.tri_indices = np.empty(dtype=np.uint16, shape=index_count)
		self.buffer_info.tris.readinto(self.tri_indices)

	@property
	def lod_index(self, ):
		try:
			lod_i = int(math.log2(self.poweroftwo))
		except:
			lod_i = 0
			logging.warning(f"math domain for lod {self.poweroftwo}")
		return lod_i

	@lod_index.setter
	def lod_index(self, lod_i):
		self.poweroftwo = int(math.pow(2, lod_i))

	def update_shell_count(self):
		# 853 in aardvark is a shell mesh, but has no tri shells
		if hasattr(self, "flag") and hasattr(self.flag, "repeat_tris") and self.flag.repeat_tris:
			self.shell_count = 6
		else:
			self.shell_count = 1

	@property
	def tris(self, ):
		if hasattr(self.flag, "stripify") and self.flag.stripify:
			return np.flip(triangulate((self.tri_indices,)), axis=-1)
		else:
			try:
				# create non-overlapping tris from flattened tri indices
				tris_raw = np.reshape(self.tri_indices, (len(self.tri_indices)//3, 3))
				# reverse each tri to account for the flipped normals from mirroring in blender
				return np.flip(tris_raw, axis=-1)
			except ValueError:
				logging.exception(f"Reshaping tris failed for {self}, {self.tri_indices}")
				# raise
				return ()

	@tris.setter
	def tris(self, list_of_b_tris):
		# just take the first and only chunk
		assert len(list_of_b_tris) == 1
		b_bone_id, b_tris = list_of_b_tris[0]

		if hasattr(self.flag, "stripify") and self.flag.stripify:
			strip_whole = stripify(np.flip(b_tris, axis=-1), stitchstrips=True)[0]
			# add degenerate tris at either end to avoid breaking strips
			strip = [strip_whole[0], strip_whole[0]]
			strip.extend(strip_whole)
			# stock PC uses even length strips exclusively (?)
			if len(strip) % 2:
				strip.append(strip[-1])
			strip.append(strip[-1])
			strip.append(strip[-1])
			self.tri_indices = np.array(strip, dtype=np.uint16)
		else:
			# cast to uint16
			raw_tris = np.array(b_tris, dtype=np.uint16)
			# reverse tris
			raw_tris = np.flip(raw_tris, axis=-1)
			# flatten array
			self.tri_indices = np.reshape(raw_tris, len(raw_tris) * 3)

	def validate_tris(self):
		"""See if all tri indices point into the vertex buffer, raise an error if they don't"""
		# this is fairly costly (10 % of total loading time), so don't do it by default
		# max_ind = np.max(self.tri_indices)
		# if max_ind >= self.vertex_count:
		for max_ind in self.tri_indices:
			if max_ind >= self.vertex_count:
				raise IndexError(f"Tri index {max_ind} does not point into {self.vertex_count} vertices for {self}")
		logging.debug("All tri indices are valid")

	def import_fur_as_weights(self, fur):
		# get max of fur length value for all verts
		self.fur_length = np.max(fur[:, 0]) * FUR_OVERHEAD
		# fur length can be set to 0 for the whole mesh, so make sure we don't divide in that case
		if self.fur_length:
			# normalize with some overhead
			fur[:, 0] /= self.fur_length
		# value range of fur width is +-16 - squash it into 0 - 1
		fur[:, 1] = remap(fur[:, 1], -16, 16, 0, 1)
		for vertex_index, fur_vert in enumerate(fur):
			self.add_to_weights("fur_length", vertex_index, fur_vert[0])
			self.add_to_weights("fur_width", vertex_index, fur_vert[1])

	def import_vcol_a_as_weights(self, rgba):
		for vertex_index, rgba_vert in enumerate(rgba):
			self.add_to_weights("fur_clump", vertex_index, 1.0 - rgba_vert[3])

	def add_to_weights(self, bone, vertex_index, weight):
		# create a dict for new bone key
		if bone not in self.weights_info:
			self.weights_info[bone] = {}
		# supplied weight
		if weight not in self.weights_info[bone]:
			# no performance gain in using a set() here instead
			self.weights_info[bone][weight] = []
		self.weights_info[bone][weight].append(vertex_index)

	@staticmethod
	def quantize_bone_weights(bone_weights):
		# normalize weights so that they sum to 1.0
		sw = sum(bone_weights)
		bone_weights = [x / sw for x in bone_weights]
		# round is essential so the float is not truncated
		bone_weights = list(round(w * 255) for w in bone_weights)
		# additional double check
		d = np.sum(bone_weights) - 255
		bone_weights[0] -= d
		assert np.sum(bone_weights) == 255
		return bone_weights

	def unpack_weights_list(self, weights_sorted):
		# pad the weight list to 4 bones, ie. add empty bones if missing
		if weights_sorted:
			for i in range(0, 4 - len(weights_sorted)):
				weights_sorted.append([0, 0])
			# assert len(weights_sorted) == 4
			ids, weights = zip(*weights_sorted)
			return ids, self.quantize_bone_weights(weights)
		else:
			return (0, 0, 0, 0), (0, 0, 0, 0)

