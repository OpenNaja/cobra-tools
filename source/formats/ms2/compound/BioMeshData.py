# START_GLOBALS
import logging
import numpy as np
import struct

from generated.array import Array
from generated.formats.ms2.compound.OffsetChunk import OffsetChunk
from generated.formats.ms2.compound.PosChunk import PosChunk
from generated.formats.ms2.compound.packing_utils import *
from plugin.utils.tristrip import triangulate


# END_GLOBALS


class BioMeshData:

	# START_CLASS

	# @property
	def get_stream_index(self):
		# logging.debug(f"Using stream {self.buffer_info.offset}")
		return self.buffer_info.offset

	def get_vcol_count(self, ):
		if "colors" in self.dt.fields:
			return self.dt["colors"].shape[0]
		return 0

	def get_uv_count(self, ):
		if "uvs" in self.dt.fields:
			return self.dt["uvs"].shape[0]
		return 0

	@property
	def tris_start_address(self):
		return self.stream_info.vertex_buffer_size

	@property
	def tris_address(self):
		# just a guess here, not guaranteed to be the right starting offset
		return self.tris_start_address + self.pos_chunks[0].tris_offset

	def read_tris(self):
		pass

	def read_tris_bio(self):
		# read all tri indices for this mesh, but only as many as needed if there are shells
		self.stream_info.stream.seek(self.tris_address)
		index_count = self.tris_count * 3  # // self.shell_count
		logging.info(f"Reading {index_count} indices at {self.stream_info.stream.tell()}")
		_tri_indices = np.empty(dtype=np.uint8, shape=index_count)
		self.stream_info.stream.readinto(_tri_indices)
		self.tri_indices = _tri_indices.astype(np.uint32)

	@property
	def pos_chunks_address(self):
		size_of_chunk = 64
		rel_chunks_offset = self.chunks_offset * size_of_chunk
		return self.stream_info.vertex_buffer_size + self.stream_info.tris_buffer_size + rel_chunks_offset

	@property
	def offset_chunks_address(self):
		size_of_chunk = 16
		rel_chunks_offset = self.chunks_offset * size_of_chunk
		return self.stream_info.vertex_buffer_size + self.stream_info.tris_buffer_size + self.stream_info.chunk_pos_size + rel_chunks_offset

	def read_verts(self):
		# the format differs if its flat or interleaved
		if self.flag.flat_arrays:
			# 16 bytes of metadata that follows the vertices array
			dt_list = [
				("normal", np.ubyte, (3,)),
				("winding", np.ubyte),
				("uvs", np.ushort, (2, 2)),
				("colors", np.ubyte, (1, 4))
			]
		else:
			# 32 bytes per vertex, with all data interleaved
			dt_list = [
				("pos", np.float16, (3,)),
				("shapekey", np.float16, (3,)),  # used for lod fading
				("sth", np.float16, (4,)),
				("normal", np.ubyte, (3,)),
				("winding", np.ubyte),
				("uvs", np.ushort, (1, 2)),
				("colors", np.ubyte, (1, 4))
			]
		# create arrays for this mesh
		self.vertices = np.empty(dtype=np.float, shape=(self.vertex_count, 3))
		self.normals = np.empty(dtype=np.float, shape=(self.vertex_count, 3))
		self.dt = np.dtype(dt_list)
		uv_shape = self.dt["uvs"].shape
		self.uvs = np.empty((self.vertex_count, *uv_shape), np.float32)
		colors_shape = self.dt["colors"].shape
		self.colors = np.empty((self.vertex_count, *colors_shape), np.float32)

		self.read_chunk_infos()

		first_tris_offs = self.pos_chunks[0].tris_offset
		v_off = 0
		offs = 0
		flags = set()
		us = set()

		self.read_tris_bio()
		self.weights = []

		for i, (pos, off) in enumerate(zip(self.pos_chunks, self.offset_chunks)):
			abs_tris = self.tris_start_address + pos.tris_offset
			print("\n", i, pos, off)
			print("\n", i, pos.u_1)
			print(f"chunk {i} tris at {abs_tris}, weights_flag {off.weights_flag}")

			self.stream_info.stream.seek(off.vertex_offset)
			print(f"verts {i} start {self.stream_info.stream.tell()}, count {off.vertex_count}")

			if self.flag.flat_arrays:
				# verts packed into uint64
				off.raw_verts = np.empty(dtype=np.uint64, shape=off.vertex_count)
				self.stream_info.stream.readinto(off.raw_verts)

				# check if weights chunk is present
				if off.weights_flag.has_weights:
					# read a index data for each vertex
					dt_weights = [
						("bone ids", np.ubyte, (4,)),
						("bone weights", np.ubyte, (4,)),
					]
					self.dt_weights = np.dtype(dt_weights)
					off.weights = np.empty(dtype=self.dt_weights, shape=off.vertex_count)
					self.stream_info.stream.readinto(off.weights)
					chunk_weights = [[(i, w) for i, w in zip(vert["bone ids"], vert["bone weights"]) if w > 0] for vert in off.weights]
				else:
					# use the chunk's bone index for each vertex in chunk
					chunk_weights = [[(off.weights_flag.bone_index, 255), ] for _ in range(off.vertex_count)]
				self.weights.extend(chunk_weights)

				# uv, normals etc
				print(f"meta {i} start {self.stream_info.stream.tell()}")
				off.raw_meta = np.empty(dtype=self.dt, shape=off.vertex_count)
				self.stream_info.stream.readinto(off.raw_meta)

				# store chunk's data
				self.vertices[offs:offs + off.vertex_count] = [unpack_swizzle(unpack_longint_vec(i, off.pack_offset)[0]) for i in off.raw_verts]
				self.uvs[offs:offs + off.vertex_count] = off.raw_meta["uvs"]
				self.colors[offs:offs + off.vertex_count] = off.raw_meta["colors"]
				self.normals[offs:offs + off.vertex_count] = off.raw_meta["normal"]
			else:
				# read the interleaved vertex array, including all extra data
				off.raw_verts = np.empty(dtype=dt_list, shape=off.vertex_count)
				self.stream_info.stream.readinto(off.raw_verts)

				# store chunk's data
				self.vertices[offs:offs + off.vertex_count] = [unpack_swizzle(vec) for vec in off.raw_verts["pos"]]
				self.uvs[offs:offs + off.vertex_count] = off.raw_verts["uvs"]
				self.colors[offs:offs + off.vertex_count] = off.raw_verts["colors"]
				self.normals[offs:offs + off.vertex_count] = off.raw_verts["normal"]
			# same for all chunked meshes, regardless if flat or interleaved arrays
			flags.add(off.weights_flag)
			us.add(pos.u_1)
			self.tri_indices[pos.tris_offset - first_tris_offs:] += v_off
			v_off = off.vertex_count
			offs += off.vertex_count

		# print("weights_flags", flags, "u1s", us)

		# normalize
		self.normals = (self.normals - 128) / 128
		self.normals /= np.linalg.norm(self.normals, axis=1, keepdims=True)
		# pull out fur from UV data
		self.uvs = unpack_ushort_vector(self.uvs)
		self.fur_length = 0.0
		# transfer fur from uv to weights
		if self.flag.fur_shells:
			# fur is the 2nd uv layer
			fur = self.uvs[:, 1]
			self.import_fur_as_weights(fur)
			# don't store fur data as uv for blender
			self.uvs = self.uvs[:, :1]
		# just a sanity check
		assert self.vertex_count == sum(o.vertex_count for o in self.offset_chunks)

	def read_chunk_infos(self):
		# logging.debug(f"Reading {self.vertex_count} verts at {self.stream_info.stream.tell()}")
		self.stream_info.stream.seek(self.pos_chunks_address)
		self.pos_chunks = Array.from_stream(self.stream_info.stream, (self.chunks_count,), PosChunk, self.context, 0,
											None)
		print(self)
		print(f"{self.chunks_count} pos_chunks at {self.pos_chunks_address}")
		self.stream_info.stream.seek(self.offset_chunks_address)
		self.offset_chunks = Array.from_stream(self.stream_info.stream, (self.chunks_count,), OffsetChunk, self.context,
											   0, None)
		print(f"{self.chunks_count} offset_chunks at {self.offset_chunks_address}")

	@property
	def tris(self, ):
		# if self.flag.flat_arrays:
		# print(self.tri_indices)
		# create non-overlapping tris from flattened tri indices
		tris_raw = np.reshape(self.tri_indices, (len(self.tri_indices) // 3, 3))
		# reverse each tri to account for the flipped normals from mirroring in blender
		return np.flip(tris_raw, axis=-1)
		# else:
		# 	return triangulate((self.tri_indices,))

	# def set_verts(self, verts):
	# 	"""Update self.verts_data from list of new verts"""
	# 	self.verts_data = np.zeros(len(verts), dtype=self.dt)
	# 	for i, (
	# 			position, residue, normal, winding, tangent, bone_index, uvs, vcols, bone_ids, bone_weights,
	# 			fur_length, fur_width, shapekey) in enumerate(
	# 		verts):
	# 		# print("shapekey", shapekey)
	# 		self.verts_data[i]["pos"] = pack_longint_vec(pack_swizzle(position), residue, self.base)
	# 		self.verts_data[i]["normal"] = pack_ubyte_vector(pack_swizzle(normal))
	# 		self.verts_data[i]["tangent"] = pack_ubyte_vector(pack_swizzle(tangent))
	#
	# 		# winding seems to be a bitflag (flipped UV toggles the first bit of all its vertices to 1)
	# 		# 0 = natural winding matching the geometry
	# 		# 128 = UV's winding is flipped / inverted compared to geometry
	# 		self.verts_data[i]["winding"] = winding * 128
	# 		self.verts_data[i]["bone index"] = bone_index
	# 		if "bone ids" in self.dt.fields:
	# 			self.verts_data[i]["bone ids"] = bone_ids
	# 			# round is essential so the float is not truncated
	# 			self.verts_data[i]["bone weights"] = list(round(w * 255) for w in bone_weights)
	# 			# print(self.verts_data[i]["bone weights"], np.sum(self.verts_data[i]["bone weights"]))
	# 			# additional double check
	# 			d = np.sum(self.verts_data[i]["bone weights"]) - 255
	# 			self.verts_data[i]["bone weights"][0] -= d
	# 			assert np.sum(self.verts_data[i]["bone weights"]) == 255
	# 		if "uvs" in self.dt.fields:
	# 			self.verts_data[i]["uvs"] = list(pack_ushort_vector(uv) for uv in uvs)
	# 		if "fur_shell" in self.dt.fields and fur_length is not None:
	# 			self.verts_data[i]["fur_shell"] = pack_ushort_vector((fur_length, remap(fur_width, 0, 1, -16, 16)))
	# 		if "colors" in self.dt.fields:
	# 			self.verts_data[i]["colors"] = list(list(round(c * 255) for c in vcol) for vcol in vcols)
	# 		if "shapekeys0" in self.dt.fields:
	# 			# first pack it as uint64
	# 			raw_packed = pack_longint_vec(pack_swizzle(shapekey), 0, self.base)
	# 			if raw_packed < 0:
	# 				logging.error(f"Shapekey {raw_packed} could not be packed into uint64")
	# 				raw_packed = 0
	# 			raw_bytes = struct.pack("Q", raw_packed)
	# 			# unpack to 2 uints again and assign data
	# 			first, second = struct.unpack("LL", raw_bytes)
	# 			self.verts_data[i]["shapekeys0"] = first
	# 			self.verts_data[i]["shapekeys1"] = second
	# print(self.verts_data[:]["winding"])
