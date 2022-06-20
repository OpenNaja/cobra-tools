
import logging
import numpy as np
import struct

from generated.array import Array
from generated.formats.ms2.compound.OffsetChunk import OffsetChunk
from generated.formats.ms2.compound.PosChunk import PosChunk
from generated.formats.ms2.compound.packing_utils import *

FUR_OVERHEAD = 2


from source.formats.base.basic import fmt_member
import numpy
from generated.formats.ms2.compound.MeshData import MeshData


class BioMeshData(MeshData):

	"""
	JWE2 - 48 bytes incl. inheritance
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# unk
		self.chunks_offset = 0

		# unk
		self.chunks_count = 0
		self.tris_count = 0

		# num verts in mesh
		self.vertex_count = 0

		# unk, may be used in other models
		self.zero_1 = 0

		# power of 2 increasing with lod index
		self.poweroftwo = 0

		# some floats, purpose unknown
		self.unk_floats = numpy.zeros((2,), dtype=numpy.dtype('float32'))

		# seen 1 or 13
		self.flag = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.chunks_offset = 0
		self.chunks_count = 0
		self.tris_count = 0
		self.vertex_count = 0
		self.zero_1 = 0
		self.poweroftwo = 0
		self.unk_floats = numpy.zeros((2,), dtype=numpy.dtype('float32'))
		self.flag = 0

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
		instance.chunks_offset = stream.read_uint()
		instance.chunks_count = stream.read_uint()
		instance.tris_count = stream.read_uint()
		instance.vertex_count = stream.read_uint()
		instance.zero_1 = stream.read_uint64()
		instance.poweroftwo = stream.read_uint()
		instance.unk_floats = stream.read_floats((2,))
		instance.flag = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.chunks_offset)
		stream.write_uint(instance.chunks_count)
		stream.write_uint(instance.tris_count)
		stream.write_uint(instance.vertex_count)
		stream.write_uint64(instance.zero_1)
		stream.write_uint(instance.poweroftwo)
		stream.write_floats(instance.unk_floats)
		stream.write_uint(instance.flag)

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
		return f'BioMeshData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* chunks_offset = {fmt_member(self.chunks_offset, indent+1)}'
		s += f'\n	* chunks_count = {fmt_member(self.chunks_count, indent+1)}'
		s += f'\n	* tris_count = {fmt_member(self.tris_count, indent+1)}'
		s += f'\n	* vertex_count = {fmt_member(self.vertex_count, indent+1)}'
		s += f'\n	* zero_1 = {fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* poweroftwo = {fmt_member(self.poweroftwo, indent+1)}'
		s += f'\n	* unk_floats = {fmt_member(self.unk_floats, indent+1)}'
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
		self.tri_indices = np.empty(dtype=np.uint8, shape=index_count)
		self.stream_info.stream.readinto(self.tri_indices)
		# print(self.tri_indices)
		# create non-overlapping tris from flattened tri indices
		tris_raw = np.reshape(self.tri_indices, (len(self.tri_indices) // 3, 3))
		# reverse each tri to account for the flipped normals from mirroring in blender
		self._tris = np.flip(tris_raw, axis=-1).astype(np.uint32)

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
		# read vertices of this mesh
		# self.stream_info.stream.seek(self.vertex_offset)
		# self.update_shell_count()
		self.vertices = np.empty(dtype=np.float, shape=(self.vertex_count, 3))
		# the idea of the new method appears to be optimized tris, so use safe dtype here to avoid overflow in the complete list
		# self.tris_raw = np.empty(dtype=np.uint32, shape=(self.vertex_count, 3))

		# logging.debug(f"Reading {self.vertex_count} verts at {self.stream_info.stream.tell()}")
		self.stream_info.stream.seek(self.pos_chunks_address)
		self.pos_chunks = Array.from_stream(self.stream_info.stream, (self.chunks_count,), PosChunk, self.context, 0, None)
		print(self)
		print(f"{self.chunks_count} pos_chunks at {self.pos_chunks_address}")
		self.stream_info.stream.seek(self.offset_chunks_address)
		self.offset_chunks = Array.from_stream(self.stream_info.stream, (self.chunks_count,), OffsetChunk, self.context, 0, None)
		print(f"{self.chunks_count} offset_chunks at {self.offset_chunks_address}")
		# for i, (pos, off) in enumerate(zip(self.pos_chunks, self.offset_chunks)):
		# 	print("\n", i, pos, off)
		self.read_tris_bio()
		first_tris_offs = self.pos_chunks[0].tris_offset
		v_off = 0
		offs = 0
		flags = set()
		us = set()
		for i, (pos, off) in enumerate(zip(self.pos_chunks, self.offset_chunks)):
			abs_tris = self.tris_start_address + pos.tris_offset
			# print("\n", i, pos, off)
			print("\n", i, pos.u_1)
			print(f"chunk {i} tris at {abs_tris}, weights_flag {off.weights_flag}")

			self.stream_info.stream.seek(off.vertex_offset)
			print(f"verts {i} start {self.stream_info.stream.tell()}, count {off.vertex_count}")
			off.raw_verts = np.empty(dtype=np.uint64, shape=off.vertex_count)
			self.stream_info.stream.readinto(off.raw_verts)

			# check if weights chunk is present
			if off.weights_flag.has_weights:
				dt_weights = [
					("bone ids", np.ubyte, (4,)),
					("bone weights", np.ubyte, (4,)),
					# ("zeros1", np.uint64)
				]
				self.dt_weights = np.dtype(dt_weights)
				off.weights = np.empty(dtype=self.dt_weights, shape=off.vertex_count)
				self.stream_info.stream.readinto(off.weights)
			else:
				# use off.weights_flag.bone_index
				pass
				# print(off.weights)

			# print(off.raw_verts)
			# 16 bytes
			dt_list = [
				("normal", np.ubyte, (3,)),
				("winding", np.ubyte),
				("tangent", np.ubyte, (3,)),
				("bone index", np.ubyte),
				("uvs", np.ushort, (1, 2)),
				("zeros2", np.uint32, (1,)),
			]
			self.dt = np.dtype(dt_list)
			uv_shape = self.dt["uvs"].shape
			self.uvs = np.empty((self.vertex_count, *uv_shape), np.float32)
			print(f"meta {i} start {self.stream_info.stream.tell()}")
			off.raw_meta = np.empty(dtype=self.dt, shape=off.vertex_count)
			self.stream_info.stream.readinto(off.raw_meta)
			off.verts = [unpack_swizzle(unpack_longint_vec(i, off.pack_offset)[0]) for i in off.raw_verts]
			flags.add(off.weights_flag)
			us.add(pos.u_1)
			self._tris[(pos.tris_offset - first_tris_offs) // 3:] += v_off
			v_off = off.vertex_count
			self.vertices[offs:offs + len(off.verts)] = off.verts
			self.uvs[offs:offs + len(off.verts)] = off.raw_meta["uvs"]
			offs += len(off.verts)
			# if any(off.raw_meta["zeros2"]):
			# 	break
			# if i == 3:
			# 	break
		print("weights_flags", flags, "u1s", us)
		self.uvs = unpack_ushort_vector(self.uvs)
		# print(self.vertices)
		# confirmed
		assert self.vertex_count == sum(o.vertex_count for o in self.offset_chunks)

	@property
	def tris(self, ):
		return self._tris

	# # create non-overlapping tris from flattened tri indices
	# tris_raw = np.reshape(self.tri_indices, (len(self.tri_indices)//3, 3))
	# # reverse each tri to account for the flipped normals from mirroring in blender
	# return np.flip(tris_raw, axis=-1)

	def set_verts(self, verts):
		"""Update self.verts_data from list of new verts"""
		self.verts_data = np.zeros(len(verts), dtype=self.dt)
		for i, (
				position, residue, normal, winding, tangent, bone_index, uvs, vcols, bone_ids, bone_weights,
				fur_length, fur_width, shapekey) in enumerate(
			verts):
			# print("shapekey", shapekey)
			self.verts_data[i]["pos"] = pack_longint_vec(pack_swizzle(position), residue, self.base)
			self.verts_data[i]["normal"] = pack_ubyte_vector(pack_swizzle(normal))
			self.verts_data[i]["tangent"] = pack_ubyte_vector(pack_swizzle(tangent))

			# winding seems to be a bitflag (flipped UV toggles the first bit of all its vertices to 1)
			# 0 = natural winding matching the geometry
			# 128 = UV's winding is flipped / inverted compared to geometry
			self.verts_data[i]["winding"] = winding * 128
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
	# print(self.verts_data[:]["winding"])

