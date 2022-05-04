# START_GLOBALS
import logging
import math
import numpy as np
from plugin.utils.tristrip import triangulate

FUR_OVERHEAD = 2


# END_GLOBALS


class MeshData:

	# START_CLASS

	# def read_bytes(self, buffer_2_offset, vertex_data_size, stream):
	# 	"""Used to store raw binary vertex and tri data on the mesh, for merging"""
	# 	# print("reading binary mesh data")
	# 	# read a vertices of this mesh
	# 	stream.seek(buffer_2_offset + self.vertex_offset)
	# 	self.verts_bytes = stream.read(self.size_of_vertex * self.vertex_count)
	# 	stream.seek(buffer_2_offset + vertex_data_size + self.tri_offset)
	# 	self.tris_bytes = stream.read(2 * self.tri_index_count)
	#
	# def read_bytes_map(self, buffer_2_offset, stream):
	# 	"""Used to document byte usage of different vertex formats"""
	# 	# read a vertices of this mesh
	# 	stream.seek(buffer_2_offset + self.vertex_offset)
	# 	# read the packed ms2_file
	# 	ms2_file = np.fromfile(stream, dtype=np.ubyte, count=self.size_of_vertex * self.vertex_count)
	# 	ms2_file = ms2_file.reshape((self.vertex_count, self.size_of_vertex))
	# 	self.bytes_max = np.max(ms2_file, axis=0)
	# 	self.bytes_min = np.min(ms2_file, axis=0)
	# 	self.bytes_mean = np.mean(ms2_file, axis=0)
	# 	if self.size_of_vertex != 48:
	# 		raise AttributeError(f"size_of_vertex != 48: size_of_vertex {self.size_of_vertex}, flag {self.flag}", )

	def write_verts(self, stream):
		stream.write(self.verts_data.tobytes())

	@property
	def tris_address(self):
		raise NotImplementedError("Subclass must overwrite tris_address")

	def read_tris(self, stream):
		# read all tri indices for this mesh, but only as many as needed if there are shells
		stream.seek(self.tris_address)
		index_count = self.tri_index_count // self.shell_count
		logging.debug(f"Reading {index_count} indices at {stream.tell()}")
		self.tri_indices = np.empty(dtype=np.uint16, shape=index_count)
		stream.readinto(self.tri_indices)
		# check if there's no empty value left in the array
		# if len(self.tri_indices) != index_count:
		# 	raise BufferError(f"{len(self.tri_indices)} were read into tri index buffer, should have {index_count}")

	def write_tris(self, stream):
		tri_bytes = self.tri_indices.tobytes()
		# extend tri array according to shell count
		logging.debug(f"Writing {self.shell_count} shells of {len(self.tri_indices)} triangles")
		for shell in range(self.shell_count):
			stream.write(tri_bytes)

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
		if self.flag.repeat_tris:
			self.shell_count = 6
		else:
			self.shell_count = 1

	@property
	def tris(self, ):
		if hasattr(self.flag, "stripify") and self.flag.stripify:
			return triangulate((self.tri_indices,))
		else:
			# create non-overlapping tris from flattened tri indices
			tris_raw = np.reshape(self.tri_indices, (len(self.tri_indices)//3, 3))
			# reverse each tri to account for the flipped normals from mirroring in blender
			return np.flip(tris_raw, axis=-1)

	@tris.setter
	def tris(self, b_tris):
		# cast to uint16
		raw_tris = np.array(b_tris, dtype=np.uint16)
		# reverse tris
		raw_tris = np.flip(raw_tris, axis=-1)
		# flatten array
		self.tri_indices = np.reshape(raw_tris, len(raw_tris)*3)

	def validate_tris(self):
		"""See if all tri indices point into the vertex buffer, raise an error if they don't"""
		pass
		# this is fairly costly (10 % of total loading time), so don't do it by default
		# # max_ind = np.max(self.tri_indices)
		# # if max_ind >= len(self.verts_data):
		# for max_ind in self.tri_indices:
		# 	if max_ind >= len(self.verts_data):
		# 		raise IndexError(f"Tri index {max_ind} does not point into {len(self.verts_data)} vertices")
		# logging.debug("All tri indices are valid")
