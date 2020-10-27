
import struct
import math
import numpy as np
from generated.formats.ms2.compound.packing_utils import *
from utils.tristrip import triangulate
import typing
from generated.array import Array


class PcModelData:

	"""
	Defines one model's data. Both LODs and mdl2 files may contain several of these.
	This is a fragment from headers of type (0,0)
	If there is more than one of these, the fragments appear as a list according to
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# always zero
		self.zeros_a = Array()

		# repeat
		self.tri_index_count_a = 0

		# vertex count of model
		self.vertex_count = 0

		# x*16 = offset in buffer 2
		self.tri_offset = 0

		# number of index entries in the triangle index list; (not: number of triangles, byte count of tri buffer)
		self.tri_index_count = 0

		# x*16 = offset in buffer 2
		self.vertex_offset = 0

		# x*16 = offset in buffer 2
		self.weights_offset = 0

		# x*16 = offset in buffer 2
		self.uv_offset = 0

		# always zero
		self.zero_b = 0

		# x*16 = offset in buffer 2
		self.vertex_color_offset = 0

		# ?
		self.vert_offset_within_lod = 0

		# power of 2 increasing with lod index
		self.poweroftwo = 0

		# always zero
		self.zero = 0

		# some floats
		self.unknown_07 = 0

		# bitfield
		self.flag = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.zeros_a.read(stream, 'Uint', 4, None)
		if stream.version == 18:
			self.tri_index_count_a = stream.read_uint()
		self.vertex_count = stream.read_uint()
		self.tri_offset = stream.read_uint()
		self.tri_index_count = stream.read_uint()
		self.vertex_offset = stream.read_uint()
		self.weights_offset = stream.read_uint()
		self.uv_offset = stream.read_uint()
		self.zero_b = stream.read_uint()
		self.vertex_color_offset = stream.read_uint()
		self.vert_offset_within_lod = stream.read_uint()
		self.poweroftwo = stream.read_uint()
		self.zero = stream.read_uint()
		self.unknown_07 = stream.read_float()
		self.flag = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		self.zeros_a.write(stream, 'Uint', 4, None)
		if stream.version == 18:
			stream.write_uint(self.tri_index_count_a)
		stream.write_uint(self.vertex_count)
		stream.write_uint(self.tri_offset)
		stream.write_uint(self.tri_index_count)
		stream.write_uint(self.vertex_offset)
		stream.write_uint(self.weights_offset)
		stream.write_uint(self.uv_offset)
		stream.write_uint(self.zero_b)
		stream.write_uint(self.vertex_color_offset)
		stream.write_uint(self.vert_offset_within_lod)
		stream.write_uint(self.poweroftwo)
		stream.write_uint(self.zero)
		stream.write_float(self.unknown_07)
		stream.write_uint(self.flag)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'PcModelData [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* zeros_a = ' + self.zeros_a.__repr__()
		s += '\n	* tri_index_count_a = ' + self.tri_index_count_a.__repr__()
		s += '\n	* vertex_count = ' + self.vertex_count.__repr__()
		s += '\n	* tri_offset = ' + self.tri_offset.__repr__()
		s += '\n	* tri_index_count = ' + self.tri_index_count.__repr__()
		s += '\n	* vertex_offset = ' + self.vertex_offset.__repr__()
		s += '\n	* weights_offset = ' + self.weights_offset.__repr__()
		s += '\n	* uv_offset = ' + self.uv_offset.__repr__()
		s += '\n	* zero_b = ' + self.zero_b.__repr__()
		s += '\n	* vertex_color_offset = ' + self.vertex_color_offset.__repr__()
		s += '\n	* vert_offset_within_lod = ' + self.vert_offset_within_lod.__repr__()
		s += '\n	* poweroftwo = ' + self.poweroftwo.__repr__()
		s += '\n	* zero = ' + self.zero.__repr__()
		s += '\n	* unknown_07 = ' + self.unknown_07.__repr__()
		s += '\n	* flag = ' + self.flag.__repr__()
		s += '\n'
		return s

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

