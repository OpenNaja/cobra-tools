# START_GLOBALS
import struct
import math
import numpy as np
from generated.formats.ms2.compound.packing_utils import *
from utils.tristrip import triangulate
# END_GLOBALS


class PcModelData:

	# START_CLASS

	def populate(self, ms2_file, ms2_stream, start_buffer2, bone_names=[], base=512):
		self.start_buffer2 = start_buffer2
		self.ms2_file = ms2_file
		self.base = base
		self.bone_names = bone_names
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
		"""Update ModelData.dt (numpy dtype) according to ModelData.flag"""
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
		print("PC size of vertex:", self.dt.itemsize)
		print("PC size of uv:", self.dt_uv.itemsize)
		print("PC size of weights:", self.dt_w.itemsize)

	def read_tris(self, stream):
		# read all tri indices for this model
		stream.seek(self.start_buffer2 + (self.tri_offset * 16))
		# print("tris offset",stream.tell())
		# read all tri indices for this model segment
		self.tri_indices = list(struct.unpack(str(self.tri_index_count) + "H", stream.read(self.tri_index_count * 2)))

	@property
	def tris(self, ):
		# tri strip
		return triangulate((self.tri_indices,))

	def read_verts(self, stream):
		# read a vertices of this model
		stream.seek(self.start_buffer2 + (self.vertex_offset * 16))
		print("VERTS", stream.tell())
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# read the packed ms2_file
		self.verts_data = np.fromfile(stream, dtype=self.dt, count=self.vertex_count)
		stream.seek(self.start_buffer2 + (self.uv_offset * 16))
		print("UV", stream.tell())
		self.uv_data = np.fromfile(stream, dtype=self.dt_uv, count=self.vertex_count)
		stream.seek(self.start_buffer2 + (self.weights_offset * 16))
		print("WEIGHtS", stream.tell())
		self.weights_data = np.fromfile(stream, dtype=self.dt_w, count=self.vertex_count)
		# print(self.verts_data)
		# create arrays for the unpacked ms2_file
		self.init_arrays(self.vertex_count)
		# first cast to the float uvs array so unpacking doesn't use int division
		if self.uvs is not None:
			self.uvs[:] = self.uv_data[:]["uvs"]
			# unpack uvs
			self.uvs = (self.uvs - 32768) / 2048
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

			# stores all (bonename, weight) pairs of this vertex
			vert_w = []
			if self.bone_names:
				if "bone ids" in self.dt.fields and residue:
					weights = self.get_weights(self.weights_data[i]["bone ids"], self.weights_data[i]["bone weights"])
					vert_w = [(self.bone_names[bone_i], w) for bone_i, w in weights]
				# fallback: skin parition
				if not vert_w:
					try:
						vert_w = [(self.bone_names[self.verts_data[i]["bone index"]], 1), ]
					except IndexError:
						# aviary landscape
						vert_w = [(str(self.verts_data[i]["bone index"]), 1), ]
			#
			# # create fur length vgroup
			# if self.flag in (1013, 821, 885):
			# 	vert_w.append(("fur_length", self.uvs[i][1][0]))

			# the unknown 0, 128 byte
			vert_w.append(("unk0", self.verts_data[i]["unk"] / 255))
			# packing bit
			vert_w.append(("residue", residue))
			self.weights.append(vert_w)
		# print(self.vertices)

	@staticmethod
	def get_weights(bone_ids, bone_weights):
		return [(i, w / 255) for i, w in zip(bone_ids, bone_weights) if w > 0]

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
