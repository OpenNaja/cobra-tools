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
	def __init__(self, in_tris, in_verts, out_tris_chunks, out_verts, bone_id):

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
		logging.debug(f"Built neighbors table for {len(self.tris_per_v_index)} verts")

	def get_random_tri(self):
		return self.in_tris.pop()

	def partition(self):
		next_tri = self.get_random_tri()
		while self.in_tris:
			if not next_tri:
				next_tri = self.get_random_tri()
			# pick a random starting tri / take one where the last chunk left off?
			chunk = Chunk(self, self.bone_id)
			next_tri = chunk.grow(next_tri)
			self.chunks.append(chunk)
		# maybe do some optimization in here?
		for chunk in self.chunks:
			chunk.remap()


class Chunk:
	MAX_ITER = 1000

	def __init__(self, chunked_mesh, bone_id):
		self.mesh = chunked_mesh
		self.tris = []
		self.verts = set()
		self.bone_id = bone_id
		# todo - enumerate?
		self.id = self.bone_id
		self.iterations = 0

	def check_add_tri(self, tri):
		"""Checks if tri can be added to this chunk"""
		self.iterations += 1
		if tri not in self.mesh.in_tris:
			logging.debug(f"Tri {tri} can not be added, as it has been taken already.")
			return
		if len(self.tris) + 1 > self.mesh.max_t:
			logging.debug(f"Tri {tri} can not be added, as chunk {self.id} has {len(self.tris)}/{self.mesh.max_t} tris already.")
			return
		new_verts = [i for i in tri if i not in self.verts]
		if len(self.verts) + len(new_verts) > self.mesh.max_v:
			logging.debug(f"Tri {tri} can not be added, as it would add {len(new_verts)} to chunk {self.id}, which has {len(self.verts)}/{self.mesh.max_v} verts already.")
			return
		# can add it!
		logging.debug(f"Tri {tri} is added to chunk {self.id}.")
		self.mesh.in_tris.pop(tri)
		self.tris.append(tri)
		self.verts.update(new_verts)
		return tri

	def grow(self, tri):
		# todo - how to check for stopping? - maybe counting how many times check_add_tri has been run?
		self.check_add_tri(tri)
		while self.iterations < self.MAX_ITER:
			# pick direct neighbors
			for v in tri:
				for tris in self.mesh.tris_per_v_index.get(v):
					for tri in tris:
						self.check_add_tri(tri)
		# todo - tie into the regular logic
		# no direct neighbors on a static mesh, keep growing
		if self.bone_id != DYNAMIC_ID:
			# pick new tri
			pass
		# todo - if we set a tri here, it could act as the start of the next chunk
		return None

	def remap(self):
		# pick local verts
		used_verts = list(sorted(self.verts))
		new_verts = [self.mesh.in_verts[old_vert_i] for old_vert_i in used_verts]
		# update tri indices into local chunk verts
		v_map = {old_vert_i: new_vert_i for new_vert_i, old_vert_i in enumerate(used_verts)}
		new_tris = [[v_map[old_vert_i] for old_vert_i in tri] for tri in self.tris]
		# finally extend lists by local chunk data
		self.mesh.out_tris_chunks.append((self.bone_id, new_tris))
		self.mesh.out_verts.extend(new_verts)
		# assert len(b_chunk_faces) == len(added_tris), f"Lost {len(b_chunk_faces) - len(added_tris)} tris in chunking"


def build_chunk(added_tris, b_chunk_bone_id, t_max, tris, tris_per_v_index, v_max):
	# create a local chunk
	new_tris = []
	used_verts = set()
	# pick random vertex from chunk faces if needed
	if not tris:
		v_index, tris = tris_per_v_index.popitem()
		logging.debug(f"Randomly picked vert {v_index} with {len(tris)} tris")
		# todo - what happens when a vertex is picked whose tris have all been added - can that happen?
	# assuming all the surrounding tris have been taken
	while True:
		# add more tris
		tris_for_next_round = set()
		# store verts and grab the last faces' neighbors
		for tri in tris:
			if len(used_verts) >= v_max or len(new_tris) >= t_max:
				logging.debug(f"Chunk is filled with {len(new_tris)} tris or {len(used_verts)} verts")
				# chunk is full, so stop adding tris, but add the newly found ones to the next chunk
				for t in tris:
					if t not in added_tris:
						tris_for_next_round.add(t)
				return used_verts, new_tris, tris_for_next_round
			if tri not in added_tris:
				added_tris.add(tri)
				new_tris.append(tri)
				for old_vert_i in tri:
					used_verts.add(old_vert_i)
					picked_tris = tris_per_v_index.pop(old_vert_i, ())
					for t in picked_tris:
						tris_for_next_round.add(t)
		# are direct neighbors are available?
		if tris_for_next_round:
			logging.debug(f"Found {len(tris_for_next_round)} new tris")
			tris = tris_for_next_round
		else:
			if b_chunk_bone_id == DYNAMIC_ID:
				logging.debug(f"Found no neighboring tris, gotta start a new chunk")
				# nope gotta pick a new one, and start a new chunk
				return used_verts, new_tris, ()
			else:
				# logging.debug(f"Allowing grouping of non-linked static verts into one chunk")
				if tris_per_v_index:
					v_index, tris = tris_per_v_index.popitem()
					logging.debug(f"Randomly picked vert {v_index} with {len(tris)} tris")
				else:
					return used_verts, new_tris, ()


def get_tris_per_v_index(tris, num_verts):
	tris_per_v_index = {v_index: set() for v_index in range(num_verts)}
	for tri in tris:
		for v_index in tri:
			tris_per_v_index[v_index].add(tri)
	return tris_per_v_index

