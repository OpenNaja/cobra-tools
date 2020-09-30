# START_GLOBALS
import struct
import math
import numpy as np

# END_GLOBALS


class ModelData:

	# START_CLASS

	def read_bytes_map(self, start_buffer2, stream):
		"""Used to document byte usage of different vertex formats"""
		# read a vertices of this model
		stream.seek(start_buffer2 + self.vertex_offset)
		# read the packed data
		data = np.fromfile(stream, dtype=np.ubyte, count=self.size_of_vertex * self.vertex_count)
		data = data.reshape((self.vertex_count, self.size_of_vertex))
		self.bytes_map = np.max(data, axis=0)
		if self.size_of_vertex != 48:
			raise AttributeError(f"size_of_vertex != 48: size_of_vertex {self.size_of_vertex}, flag {self.flag}", )

	# print(self.size_of_vertex, self.flag, self.bytes_map)

	def init_arrays(self, count):
		self.vertex_count = count
		self.vertices = np.empty((self.vertex_count, 3), np.float32)
		self.normals = np.empty((self.vertex_count, 3), np.float32)
		self.tangents = np.empty((self.vertex_count, 3), np.float32)
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
		"""Update ModelData.dt (numpy dtype) according to ModelData.flag"""
		# basic shared stuff
		dt = [
			("pos", np.uint64),
			("normal", np.ubyte, (3,)),
			("unk", np.ubyte),
			("tangent", np.ubyte, (3,)),
			("bone index", np.ubyte),
		]
		# uv variations
		if self.flag == 529:
			dt.extend([
				("uvs", np.ushort, (2, 2)),
				("zeros0", np.int32, (2,))
			])
		elif self.flag == 528:
			dt.extend([
				("uvs", np.ushort, (1, 2)),
				("zeros0", np.int32, (3,))
			])
		elif self.flag in (1013, 821):
			dt.extend([
				("uvs", np.ushort, (3, 2)),
				("zeros0", np.int32, (1,))
			])
		elif self.flag in (885, 565):
			dt.extend([
				("uvs", np.ushort, (3, 2)),
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
				# trees seem to have two uvs, then something like normals
				("uvs", np.ushort, (2, 2)),
				("colors", np.ubyte, (6, 4)),
			])

		# bone weights
		if self.flag in (529, 533, 885, 565, 1013, 528, 821):
			dt.extend([
				("bone ids", np.ubyte, (4,)),
				("bone weights", np.ubyte, (4,)),
				("zeros1", np.uint64)
			])
		self.dt = np.dtype(dt)
		if self.dt.itemsize != self.size_of_vertex:
			raise AttributeError(
				f"Vertex size for flag {self.flag} is wrong! Collected {self.dt.itemsize}, got {self.size_of_vertex}")

	def read_verts(self, stream, data):
		# read a vertices of this model
		stream.seek(self.start_buffer2 + self.vertex_offset)
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# read the packed data
		self.verts_data = np.fromfile(stream, dtype=self.dt, count=self.vertex_count)
		# create arrays for the unpacked data
		self.init_arrays(self.vertex_count)
		# first cast to the float uvs array so unpacking doesn't use int division
		if self.uvs is not None:
			self.uvs[:] = self.verts_data[:]["uvs"]
			# unpack uvs
			self.uvs = (self.uvs - 32768) / 2048
		if self.colors is not None:
			# first cast to the float colors array so unpacking doesn't use int division
			self.colors[:] = self.verts_data[:]["colors"]
			self.colors /= 255
		self.normals[:] = self.verts_data[:]["normal"]
		self.tangents[:] = self.verts_data[:]["tangent"]
		self.normals = (self.normals - 128) / 128
		self.tangents = (self.tangents - 128) / 128
		for i in range(self.vertex_count):
			in_pos_packed = self.verts_data[i]["pos"]
			vert, residue = self.unpack_longint_vec(in_pos_packed)
			self.vertices[i] = self.unpack_swizzle(vert)

			out_pos_packed = self.pack_longint_vec(self.pack_swizzle(self.vertices[i]), residue)
			# print(bin(in_pos_packed), type(in_pos_packed))
			# print(bin(out_pos_packed), type(out_pos_packed))
			# print(in_pos_packed-out_pos_packed)

			self.normals[i] = self.unpack_swizzle(self.normals[i])
			self.tangents[i] = self.unpack_swizzle(self.tangents[i])

			# stores all (bonename, weight) pairs of this vertex
			vert_w = []
			if self.bone_names:
				if "bone ids" in self.dt.fields and residue:
					weights = self.get_weights(self.verts_data[i]["bone ids"], self.verts_data[i]["bone weights"])
					vert_w = [(self.bone_names[bone_i], w) for bone_i, w in weights]
				# fallback: skin parition
				if not vert_w:
					try:
						vert_w = [(self.bone_names[self.verts_data[i]["bone index"]], 1), ]
					except IndexError:
						# aviary landscape
						vert_w = [(str(self.verts_data[i]["bone index"]), 1), ]

			# create fur length vgroup
			if self.flag in (1013, 821, 885):
				vert_w.append(("fur_length", self.uvs[i][1][0]))

			# the unknown 0, 128 byte
			vert_w.append(("unk0", self.verts_data[i]["unk"] / 255))
			# packing bit
			vert_w.append(("residue", residue))
			self.weights.append(vert_w)

	@staticmethod
	def unpack_ushort_vector(vec):
		return (vec - 32768) / 2048

	@staticmethod
	def unpack_swizzle(vec):
		# swizzle to avoid a matrix multiplication for global axis correction
		return -vec[0], -vec[2], vec[1]

	@staticmethod
	def pack_swizzle(vec):
		# swizzle to avoid a matrix multiplication for global axis correction
		return -vec[0], vec[2], -vec[1]

	@staticmethod
	def pack_ushort_vector(vec):
		return [min(int(round(coord * 2048 + 32768)), 65535) for coord in vec]

	@staticmethod
	def pack_ubyte_vector(vec):
		return [min(int(round(x * 128 + 128)), 255) for x in vec]

	@staticmethod
	def get_weights(bone_ids, bone_weights):
		return [(i, w / 255) for i, w in zip(bone_ids, bone_weights) if w > 0]

	def unpack_longint_vec(self, input):
		"""Unpacks and returns the self.raw_pos uint64"""
		# numpy uint64 does not like the bit operations so we cast to default int
		input = int(input)
		# correct for size according to base, relative to 512
		scale = self.base / 512 / 2048
		# input = self.raw_pos
		output = []
		# print("inp",bin(input))
		for i in range(3):
			# print("\nnew coord")
			# grab the last 20 bits with bitand
			# bit representation: 0b11111111111111111111
			twenty_bits = input & 0xFFFFF
			# print("input", bin(input))
			# print("twenty_bits = input & 0xFFFFF ", bin(twenty_bits), twenty_bits)
			input >>= 20
			# print("input >>= 20", bin(input))
			# print("1",bin(1))
			# get the rightmost bit
			rightmost_bit = input & 1
			# print("rightmost_bit = input & 1",bin(rightmost_bit))
			# print(rightmost_bit, twenty_bits)
			if not rightmost_bit:
				# rightmost bit was 0
				# print("rightmost_bit == 0")
				# bit representation: 0b100000000000000000000
				twenty_bits -= 0x100000
			# print("final int", twenty_bits)
			o = (twenty_bits + self.base) * scale
			output.append(o)
			# shift to skip the sign bit
			input >>= 1
		# input at this point is either 0 or 1
		return output, input

	def pack_longint_vec(self, vec, residue):
		"""Packs the input vector + residue bit into a uint64 (1, 21, 21, 21)"""
		# correct for size according to base, relative to 512
		scale = self.base / 512 / 2048
		output = 0
		for i, f in enumerate(vec):
			o = int(round(f / scale - self.base))
			# print("restored int", o)
			if o < 0x100000:
				# 0b100000000000000000000
				o += 0x100000
			else:
				# set the 1 bit flag
				output |= 1 << (21 * (i + 1) - 1)
			# print("restored int + correction", o)
			output |= o << (21 * i)
		# print("bef",bin(output))
		output |= residue << 63
		# thing = struct.unpack("<d", struct.pack("<Q",output))
		# thing2 = -1.0*float(thing[0])
		# output = struct.unpack("<Q", struct.pack("<d",thing2))[0]
		return output

	def write_verts(self, stream, data):
		# if writing directly to file, doesn't support io bytes
		# self.verts_data.tofile(stream)
		stream.write(self.verts_data.tobytes())

	def read_tris(self, stream, data):
		# read all tri indices for this model
		stream.seek(self.start_buffer2 + data.ms2_header.buffer_info.vertexdatasize + self.tri_offset)
		# print("tris offset",stream.tell())
		# read all tri indices for this model segment
		self.tri_indices = list(struct.unpack(str(self.tri_index_count) + "H", stream.read(self.tri_index_count * 2)))

	def write_tris(self, stream, data):
		stream.write(struct.pack(str(len(self.tri_indices)) + "H", *self.tri_indices))

	@property
	def lod_index(self, ):
		try:
			lod_i = int(math.log2(self.poweroftwo))
		except:
			lod_i = 0
			print("EXCEPTION: math domain for lod", self.poweroftwo)
		return lod_i

	@lod_index.setter
	def lod_index(self, lod_i):
		self.poweroftwo = int(math.pow(2, lod_i))

	def set_verts(self, verts):
		"""Update self.verts_data from list of new verts"""
		self.verts = verts
		self.verts_data = np.zeros(len(verts), dtype=self.dt)
		for i, (
		position, residue, normal, unk_0, tangent, bone_index, uvs, vcols, bone_ids, bone_weights, fur) in enumerate(
				verts):
			self.verts_data[i]["pos"] = self.pack_longint_vec(self.pack_swizzle(position), residue)
			self.verts_data[i]["normal"] = self.pack_ubyte_vector(self.pack_swizzle(normal))
			self.verts_data[i]["tangent"] = self.pack_ubyte_vector(self.pack_swizzle(tangent))
			self.verts_data[i]["unk"] = unk_0 * 255
			self.verts_data[i]["bone index"] = bone_index
			if "bone ids" in self.dt.fields:
				self.verts_data[i]["bone ids"] = bone_ids
				# round is essential so the float is not truncated
				self.verts_data[i]["bone weights"] = list(round(w * 255) for w in bone_weights)
				# additional double check
				d = np.sum(self.verts_data[i]["bone weights"]) - 255
				self.verts_data[i]["bone weights"][0] -= d
			if "uvs" in self.dt.fields:
				self.verts_data[i]["uvs"] = list(self.pack_ushort_vector(uv) for uv in uvs)
				if fur is not None:
					self.verts_data[i]["uvs"][1][0], _ = self.pack_ushort_vector((fur, 0))
			if "colors" in self.dt.fields:
				self.verts_data[i]["colors"] = list(list(c * 255 for c in vcol) for vcol in vcols)

	@property
	def tris(self, ):
		# create non-overlapping tris
		# reverse to account for the flipped normals from mirroring in blender
		return [(self.tri_indices[i + 2], self.tri_indices[i + 1], self.tri_indices[i]) for i in
				range(0, len(self.tri_indices), 3)]

	@tris.setter
	def tris(self, b_tris):
		# clear tri array
		self.tri_indices = []
		for tri in b_tris:
			# reverse to account for the flipped normals from mirroring in blender
			self.tri_indices.extend(reversed(tri))

	def populate(self, data, ms2_stream, start_buffer2, bone_names=[], base=512):
		self.start_buffer2 = start_buffer2
		self.data = data
		self.base = base
		self.bone_names = bone_names
		self.read_verts(ms2_stream, self.data)
		self.read_tris(ms2_stream, self.data)
