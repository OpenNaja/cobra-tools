import logging

DISCARD_STATIC_TRIS = 16
DYNAMIC_ID = -1
NO_BONES_ID = -2
# the hard max is 255 vertices - stay far away from that to be safe with the current algorithm
SOFT_MAX_VERTS_SHELLS = 8
SOFT_MAX_TRIS_SHELLS = 8
SOFT_MAX_VERTS = 60
SOFT_MAX_TRIS = 60


class ChunkedMesh:
	def __init__(self, in_tris, in_verts, out_tris_chunks, out_verts, bone_id, is_shell_ob):

		self.in_tris = set(in_tris)
		self.in_verts = in_verts
		self.out_tris_chunks = out_tris_chunks
		self.out_verts = out_verts
		self.bone_id = bone_id
		# track added tris across all local chunks
		self.added_tris = set()
		self.tris = ()
		self.chunks = []
		# build table of neighbors
		self.tris_per_v_index = get_tris_per_v_index(self.in_tris, len(self.in_verts))
		# for the current algorithm, shells need to use less tris per chunk than other meshes to avoid flickering
		if is_shell_ob:
			self.max_v = SOFT_MAX_VERTS_SHELLS
			self.max_t = SOFT_MAX_TRIS_SHELLS
		else:
			self.max_v = SOFT_MAX_VERTS
			self.max_t = SOFT_MAX_TRIS

	def get_random_tri(self):
		tri = next(iter(self.in_tris))
		# logging.debug(f"Picked tri {tri}")
		return tri

	def partition(self):
		# start with any tri
		next_tri = self.get_random_tri()
		while self.in_tris:
			# pick a random starting tri / take one where the last chunk left off?
			if not next_tri:
				next_tri = self.get_random_tri()
			# create a chunk and fill it
			chunk = Chunk(self, self.bone_id)
			next_tri = chunk.grow(next_tri)
			self.chunks.append(chunk)
		# todo - maybe do some optimization of chunks, such as merging by distance?
		# finally store the chunks' data
		for chunk in self.chunks:
			chunk.remap()


class Chunk:
	def __init__(self, chunked_mesh, bone_id):
		self.mesh = chunked_mesh
		self.tris = []
		self.v_indices = set()
		self.added_tris = set()
		self.bone_id = bone_id

	def check_add_tri(self, tri):
		"""Checks if tri can be added to this chunk"""
		assert len(tri) == 3, f"{tri} is not a tri"
		if tri not in self.mesh.in_tris:
			# logging.debug(f"Tri {tri} can not be added, as it has been taken already.")
			return
		if len(self.tris) + 1 > self.mesh.max_t:
			# logging.debug(f"Tri {tri} can not be added, as chunk {self.bone_id} has {len(self.tris)}/{self.mesh.max_t} tris already.")
			return
		new_verts = [i for i in tri if i not in self.v_indices]
		if len(self.v_indices) + len(new_verts) > self.mesh.max_v:
			# logging.debug(f"Tri {tri} can not be added, as it would add {len(new_verts)} to chunk {self.bone_id}, which has {len(self.verts)}/{self.mesh.max_v} verts already.")
			return
		# can add it!
		# logging.debug(f"Tri {tri} is added to chunk {self.bone_id}.")
		self.mesh.in_tris.remove(tri)
		self.tris.append(tri)
		self.added_tris.add(tri)
		self.v_indices.update(tri)
		# return tri

	def grow(self, tri):
		self.check_add_tri(tri)
		while True:
			# for the next iteration, all the neighbors have to be checked, not just the last one
			# so make a copy of the ones that have been added in the last round
			check_neighbors = tuple(self.added_tris)
			# now clear to keep track of the new tris
			self.added_tris = set()
			for tri in check_neighbors:
				# pick direct neighbors
				for v in tri:
					for tri in self.mesh.tris_per_v_index.get(v):
						self.check_add_tri(tri)
			# have any tris been added during this run?
			if not self.added_tris:
				# dynamic chunks should stop if no more neighbors are available
				if self.bone_id == DYNAMIC_ID:
					break
				else:
					# static chunk with no more direct neighbors, keep growing
					break
					# avoid tiny chunks
					# if len(self.tris) < DISCARD_STATIC_TRIS:
					# 	tri = self.mesh.get_random_tri()
					# 	# but stop if all tris have been processed
					# 	if not tri:
					# 		break
		return None

	def remap(self):
		# pick local verts
		v_indices = list(sorted(self.v_indices))
		new_verts = [self.mesh.in_verts[old_vert_i] for old_vert_i in v_indices]
		# update tri indices into local chunk verts
		v_map = {old_vert_i: new_vert_i for new_vert_i, old_vert_i in enumerate(v_indices)}
		new_tris = [[v_map[old_vert_i] for old_vert_i in tri] for tri in self.tris]
		# finally extend lists by local chunk data
		self.mesh.out_tris_chunks.append((self.bone_id, new_tris))
		self.mesh.out_verts.extend(new_verts)


def get_tris_per_v_index(tris, num_verts):
	"""Create a map between each vertex index and the tris using it"""
	tris_per_v_index = {v_index: set() for v_index in range(num_verts)}
	for tri in tris:
		for v_index in tri:
			tris_per_v_index[v_index].add(tri)
	logging.debug(f"Built neighbors table for {len(tris_per_v_index)} verts")
	return tris_per_v_index

