from generated.formats.ms2.imports import name_type_map
from io import BytesIO
import os
import time
import logging
from copy import copy

import numpy as np

from generated.formats.ms2.compounds.packing_utils import PACKEDVEC_MAX

# raise warnings to traceable errors
# np.seterr(all='raise')
np.seterr(all='warn')
np.set_printoptions(precision=3, suppress=True)

from generated.formats.base.compounds.PadAlign import get_padding
from generated.formats.ms2.compounds.Ms2InfoHeader import Ms2InfoHeader
from generated.formats.ms2.versions import *
from generated.io import IoFile
from modules.formats.shared import djb2

logging.basicConfig(level=logging.DEBUG)

BUFFER_NAMES = ("verts", "tris", "uvs", "tri_chunks", "vert_chunks")


class Ms2Context:
	def __init__(self):
		self.version = 0
		self.biosyn = 0
		self.joint_names = None

	def __repr__(self):
		return f"{self.version} | {self.biosyn}"


class Ms2File(Ms2InfoHeader, IoFile):

	def __init__(self, ):
		super().__init__(Ms2Context())

	@property
	def game(self):
		return get_game(self.context)[0].value

	@game.setter
	def game(self, game_name):
		set_game(self.context, game_name)
		set_game(self.info, game_name)

	def assign_joints(self, bone_info):
		if self.context.version >= 47:
			assert bone_info.one == 1
		# rearranged in war, possibly related to bone index size change
		# assert bone_info.knownff == -1
		assert bone_info.name_count == bone_info.bind_matrix_count == bone_info.bone_count == bone_info.parents_count == bone_info.enum_count
		assert bone_info.zeros_count == 0 or bone_info.zeros_count == bone_info.name_count
		assert bone_info.zero_0 == bone_info.zero_1 == bone_info.zero_2 == bone_info.zero_3 == 0

		if bone_info.joint_count:
			if not hasattr(bone_info, "joints"):
				logging.warning(f"Joints deactivated for debugging")
				return
			joints = bone_info.joints
			if not joints:
				logging.debug(f"Joints not used")
				return
			# test for orthogonal vecs
			# for ragdoll in joints.ragdoll_constraints:
			# 	r = ragdoll.rot.data
			# 	# dot: 0 = orthogonal, 1 = parallel
			# 	# a = np.cross(r[0], (1.0, 0.0, 0.0))
			# 	a = np.cross(r[0], r[1])
			# 	# b = np.dot(r[1], r[2])
			# 	# c = np.dot(r[0], r[2])
			# 	# print(a, b, c)
			# 	print(ragdoll.child.joint.name)
			# 	# print(np.dot(r[1], ragdoll.vec_b))
			# 	# print(np.dot(r[2], ragdoll.vec_b))
			# 	print(ragdoll.vec_b, a)
			for bone_i, joint_info, joint_transform, rigidbody in zip(
				joints.joint_to_bone, joints.joint_infos, joints.joint_transforms, joints.rigid_body_list):

				joint_transform.name = rigidbody.name = joint_info.name
				# usually, this corresponds - does not do for speedtree but does not matter
				joint_info.bone_name = bone_info.bones[bone_i].name
				# if joints.bone_count:
				# 	if joints.joint_infos[joints.bone_to_joint[bone_i]] != joint_info:
				# 		logging.warning(f"bone index [{bone_i}] doesn't point to expected joint info")

			# print(joints.joint_infos[joints.root_joint_index].name)

	def assign_bone_names(self, bone_info):
		try:
			for name_i, bone in zip(bone_info.name_indices, bone_info.bones):
				bone.name = self.buffer_0.names[name_i]
		except:
			logging.error("Names failed...")

	def load(self, filepath, read_bytes=False, read_editable=False, dump=False):
		start_time = time.time()
		self.filepath = filepath
		self.dir, self.name = os.path.split(os.path.normpath(filepath))
		self.read_editable = read_editable
		logging.info(f"Reading {self.filepath}")
		with open(filepath, "rb") as stream:
			self.read_fields(stream, self)
			self.buffer_1_offset = self.models_reader.buffer_1_start
			self.buffer_2_offset = self.buffer_1_offset + self.bone_info_size

			# logging.info(f"self.buffer_2_offset {self.buffer_2_offset}")
			# logging.info(self)
			# return
			# logging.debug(f"end of header: {self.buffer_1_offset}")

			logging.debug(f"Vertex buffer starts at {self.buffer_2_offset}")
			for i, bone_info in enumerate(self.models_reader.bone_infos):
				try:
					self.assign_bone_names(bone_info)
					self.assign_joints(bone_info)
				except:
					logging.exception(f"Joints or bones {i} lookup failed")
			try:
				self.lookup_material()
			except:
				logging.exception(f"Material lookup failed")
			if read_bytes:
				stream.seek(self.buffer_0.io_start)
				self.buffer_0_bytes = stream.read(self.buffer_0.io_size)
				stream.seek(self.buffer_1_offset)
				self.buffer_1_bytes = stream.read(self.bone_info_size)
			try:
				self.load_buffers(stream, dump)
			except:
				logging.exception(f"Buffer lookup failed")
			if read_bytes:
				static_buffer = self.get_static_buffer()
				self.buffer_2_bytes = self.get_all_bytes(static_buffer)
			if read_editable:
				expect_shapekeys = "SpeedtreeHitcheck" in self.buffer_0.names
				self.load_meshes(expect_shapekeys)
		logging.debug(f"Read {self.name} in {time.time() - start_time:.2f} seconds")

	def load_buffers(self, stream, dump):
		stream.seek(self.buffer_2_offset)
		self.init_buffers()
		# attach the static stream to the right buffer_info
		if self.buffer_infos and self.info.static_buffer_index > -1:
			i = self.info.static_buffer_index
			# hack for DLA, static buffer index is different here
			if self.context.version == 7:
				i = 0
			# ZTUAC does not use static_buffer_index eg.
			# * vertex_buffer_count = 4
			# * static_buffer_index = 3
			# all four buffer_infos use modelstream files, and ms2 just has names and bones buffers
			if self.context.version != 13:
				static_buffer_info = self.buffer_infos[i]
				static_buffer_info.name = "STATIC"
				stream.seek(self.buffer_2_offset)
				self.attach_streams(static_buffer_info, stream, dump=dump)
		# attach the streams to all other buffer_infos
		for buffer_info, modelstream_name in zip(self.external_streams(), self.modelstream_names):
			buffer_info.name = modelstream_name
			self.attach_streams(buffer_info, stream, dump=dump)

	def init_buffers(self):
		for i, buffer_info in enumerate(self.buffer_infos):
			buffer_info.name = None
			buffer_info.index = i

	def external_streams(self):
		return [buffer_info for buffer_info in self.buffer_infos if buffer_info.name != "STATIC"]

	def attach_streams(self, buffer_info, in_stream=None, dump=False):
		"""Attaches streams to a buffer info for each section, and fills them if an input stream is provided"""
		logging.debug(f"Attaching streams to {buffer_info.name}")
		for buffer_name in BUFFER_NAMES:
			if in_stream:
				buff_size = getattr(buffer_info, f"{buffer_name}_size")
				# create a set to be able to guess the size of any entry
				setattr(buffer_info, f"{buffer_name}_offsets", {buff_size})
				logging.debug(f"Loading {buffer_name} size {buff_size} at {in_stream.tell()}")
				b = in_stream.read(buff_size)
				# dump each for easy debugging
				if dump:
					with open(f"{self.filepath}_{buffer_name}.dmp", "wb") as f:
						f.write(b)
			else:
				b = b""
			# attach a reader with the bytes we have read to the buffer_info
			setattr(buffer_info, buffer_name, BytesIO(b))

	def lacks_mesh(self, model_info, model_i):
		if not hasattr(model_info, "model"):
			logging.warning(f"Model {model_i} '{model_info.name}' has no mesh attached")
			return True
		else:
			return False

	def load_meshes(self, expect_shapekeys):
		for model_i, model_info in enumerate(self.model_infos):
			if self.lacks_mesh(model_info, model_i):
				continue
			logging.debug(f"Loading mesh data for {model_info.name}")
			for wrapper in model_info.model.meshes:
				wrapper.mesh.assign_buffer_info(self.buffer_infos)
				if hasattr(wrapper.mesh, "uv_offset"):
					wrapper.mesh.buffer_info.uvs_offsets.add(wrapper.mesh.uv_offset)
			if self.context.version > 32:
				pack_base = model_info.pack_base
			else:
				pack_base = 512.0
			try:
				for i, wrapper in enumerate(model_info.model.meshes):
					# logging.info(f"Populating mesh {i}")
					wrapper.mesh.populate(pack_base, expect_shapekeys)
				# logging.info(f"Populating mesh worked {model_info}, {model_info.model}")
			except:
				logging.exception(f"Populating mesh failed for model {model_info}, {model_info.model}")

	def resize(self, fac=1.0):
		for bone_info in self.models_reader.bone_infos:
			for bindmat in bone_info.inverse_bind_matrices:
				bindmat.data[3][:3] *= fac
			for bone in bone_info.bones:
				bone.loc *= fac
			if bone_info.joint_count:
				joints = bone_info.joints
				for jt in joints.joint_transforms:
					jt.loc *= fac
				for rb in joints.rigid_body_list:
					rb.loc *= fac
				for ragdoll in joints.ragdoll_constraints:
					ragdoll.loc *= fac
				for joint_info in joints.joint_infos:
					for hc in joint_info.hitchecks:
						c = hc.collider
						if hasattr(c, "center"):
							c.center *= fac
						if hasattr(c, "radius"):
							c.radius *= fac
						if hasattr(c, "extent"):
							c.extent *= fac
						if hasattr(c, "offset"):
							c.offset *= fac
			# print(bone_info)
		for model_i, model_info in enumerate(self.model_infos):
			if self.lacks_mesh(model_info, model_i):
				continue
			model_info.bounds_min *= fac
			model_info.bounds_max *= fac
			model_info.bounds_min_repeat *= fac
			model_info.bounds_max_repeat *= fac
			model_info.center *= fac
			model_info.radius *= fac
			model_info.pack_base = self.get_pack_base(model_info.bounds_min, model_info.bounds_max)
			model_info.precision = self.get_precision(model_info.pack_base)
			for wrapper in model_info.model.meshes:
				mesh = wrapper.mesh
				mesh.resize_vertices(model_info, fac)

	def name_used(self, new_name):
		for model_info in self.model_infos:
			if model_info.name == new_name:
				return True
		return False

	def rename_file(self, old, new):
		logging.info(f"Renaming .mdl2s in {self.name}")
		for model_info in self.model_infos:
			if model_info.name == old:
				model_info.name = new

	def remove(self, mdl2_names):
		logging.info(f"Removing {len(mdl2_names)} .mdl2 files in {self.name}")
		for model_info in reversed(self.model_infos):
			if model_info.name in mdl2_names:
				self.model_infos.remove(model_info)

	def duplicate(self, mdl2_names):
		logging.info(f"Duplicating {len(mdl2_names)} .mdl2 files in {self.name}")
		for model_info in reversed(self.model_infos):
			if model_info.name in mdl2_names:
				model_info_copy = copy(model_info)
				# add as many suffixes as needed to make new_name unique
				self.make_name_unique(model_info_copy)
				self.model_infos.append(model_info_copy)
		self.model_infos.sort(key=lambda model_info: model_info.name)

	def make_name_unique(self, model_info_copy):
		new_name = model_info_copy.name
		while self.name_used(new_name):
			new_name = f"{new_name}_copy"
		model_info_copy.name = new_name

	def rename(self, name_tups):
		"""Renames strings in the main name buffer"""
		logging.info(f"Renaming in {self.name}")

		for model_info in self.model_infos:
			for material in model_info.model.materials:
				material.name = self._rename(material.name, name_tups)
			if model_info.bone_info:
				bi = model_info.bone_info
				for bone in bi.bones:
					bone.name = self._rename(bone.name, name_tups)
				ji = bi.joints
				if ji:
					for joint_info in ji.joint_infos:
						joint_info.bone_name = self._rename(joint_info.bone_name, name_tups)

	def _rename(self, s, name_tups):
		for old, new in name_tups:
			if old in s:
				logging.debug(f"Match for '{old}' in '{s}'")
				s = s.replace(old, new)
		return s

	def get_name_index(self, name, arr):
		if name not in arr:
			arr.append(name)
		return arr.index(name)

	def update_names(self):
		logging.debug("Updating MS2 name buffer")
		self.reset_field("mdl_2_names")
		_names = []
		for i, model_info in enumerate(self.model_infos):
			self.mdl_2_names[i] = model_info.name
			for material in model_info.model.materials:
				material.name_index = self.get_name_index(material.name, _names)
			if model_info.bone_info:
				for bone_index, bone in enumerate(model_info.bone_info.bones):
					model_info.bone_info.name_indices[bone_index] = self.get_name_index(bone.name, _names)
		logging.debug("Updating MS2 name hashes")
		# update hashes from new names
		self.info.name_count = len(_names)
		self.reset_field("buffer_0")
		for name_i, name in enumerate(_names):
			self.buffer_0.names[name_i] = name
			self.buffer_0.name_hashes[name_i] = djb2(name.lower())

	def update_buffer_0_bytes(self):
		with BytesIO() as temp_writer:
			self.buffer_0.to_stream(self.buffer_0, temp_writer, self.context)
			self.buffer_0_bytes = temp_writer.getvalue()

	def update_buffer_1_bytes(self):
		with BytesIO() as temp_bone_writer:
			self.buffer_infos.to_stream(self.buffer_infos, temp_bone_writer, self.context)
			self.model_infos.to_stream(self.model_infos, temp_bone_writer, self.context)
			self.models_reader.to_stream(self.models_reader, temp_bone_writer, self.context)
			# todo - maybe wrong for PC?
			self.buffer_1_bytes = temp_bone_writer.getvalue()[self.models_reader.buffer_1_start:]
			self.bone_info_size = self.models_reader.bone_info_size

	def update_buffer_2_bytes(self):
		logging.debug(f"update_buffer_2_bytes")
		if self.read_editable:
			logging.debug(f"Updating buffer 2")
			# determine how many streams we need
			max_stream_index = -1
			for model_info in self.model_infos:
				for wrapper in model_info.model.meshes:
					max_stream_index = max(max_stream_index, wrapper.mesh.get_stream_index())
			#  and update self.buffer_infos, count, and names
			self.info.vertex_buffer_count = max_stream_index + 1
			# this is the rule for JWE2, except trike93 STATIC=0
			self.info.static_buffer_index = max_stream_index
			self.num_streams = max(0, max_stream_index)
			self.reset_field("buffer_pointers")
			self.reset_field("buffer_infos")
			self.reset_field("modelstream_names")
			# first init all writers for the buffers
			self.init_buffers()
			for buffer_info in self.buffer_infos:
				self.attach_streams(buffer_info)
				if is_pc(self.context):
					arr = np.empty(dtype=np.uint8, shape=16)
					arr[:] = range(16)
					buffer_info.verts.write(arr.tobytes())
					# 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
			# now store each model
			for model_info in self.model_infos:
				logging.debug(f"Storing {model_info.name}")
				# update ModelInfo
				model = model_info.model
				model_info.num_materials = len(model.materials)
				model_info.num_lods = len(model.lods)
				model_info.num_objects = len(model.objects)
				model_info.num_meshes = len(model.meshes)
				# write each mesh's data blocks to the right temporary buffer
				for wrapper in model.meshes:
					wrapper.mesh.assign_buffer_info(self.buffer_infos)
					wrapper.mesh.write_data()
				if is_pc(self.context):
					for wrapper in model.meshes:
						wrapper.mesh.write_verts()
					for wrapper in model.meshes:
						wrapper.mesh.write_weights()
					for wrapper in model.meshes:
						wrapper.mesh.write_tris()
					for wrapper in model.meshes:
						wrapper.mesh.write_uvs()
					for wrapper in model.meshes:
						wrapper.mesh.write_uvs_2()
				# update LodInfo
				logging.debug(f"Updating lod vertex counts")
				for lod in model.lods:
					lod.vertex_count = sum(ob.mesh.vertex_count for ob in lod.objects)
					lod.tri_index_count = sum(ob.mesh.tri_index_count for ob in lod.objects)
					if is_pc(self.context):
						lod.tri_index_count -= (4 * len(lod.objects))
					# only used by PC
					vertex_offset_within_lod = 0
					for ob in lod.objects:
						ob.mesh.vertex_offset_within_lod = vertex_offset_within_lod
						vertex_offset_within_lod += ob.mesh.vertex_count
			# modify buffer size
			for buffer_info in self.buffer_infos:
				# get bytes from IO obj, pad, and update size in BufferInfo
				for buffer_name in BUFFER_NAMES:
					buff = getattr(buffer_info, buffer_name)
					buff_bytes = self.get_bytes(buff)
					setattr(buffer_info, f"{buffer_name}_size", len(buff_bytes))
				
			# store static buffer
			static_buffer = self.get_static_buffer()
			if static_buffer:
				static_buffer.name = "STATIC"
				self.buffer_2_bytes = self.get_all_bytes(static_buffer)
			else:
				# assign an empty buffer, maybe it is better to add an 'if attrib' in the saving?
				self.buffer_2_bytes = b""

	# @property
	def get_static_buffer(self):
		if self.buffer_infos and self.info.static_buffer_index > -1:
			return self.buffer_infos[self.info.static_buffer_index]

	@staticmethod
	def get_bytes(buffer_reader):
		if buffer_reader:
			buffer_reader.seek(0, 2)
			buffer_reader.write(get_padding(buffer_reader.tell(), alignment=16))
			return buffer_reader.getvalue()
		return b""

	def get_all_bytes(self, buffer_info):
		return b"".join(self.get_bytes(getattr(buffer_info, b_name, None)) for b_name in BUFFER_NAMES)

	@property
	def buffers(self):
		yield self.buffer_0_bytes
		yield self.buffer_1_bytes
		# JWE1 and PZ use only two buffers in this case, JWE2 keeps an empty third buffer
		if not self.buffer_2_bytes and self.context.version <= 50:
			return
		yield self.buffer_2_bytes

	def save(self, filepath):
		self.dir, self.name = os.path.split(os.path.normpath(filepath))
		# for modelstreams, trailing _ is ignored
		self.basename = os.path.splitext(self.name)[0].rstrip("_")
		# logging.debug("Pre-writing buffers")
		# just a quick hack to support WH
		for model_info in self.model_infos:
			if hasattr(model_info.bone_info, "bone_limits"):
				if self.context.version < 53:
					model_info.bone_info.bone_limits.index = 255
		self.info.mdl_2_count = len(self.model_infos)
		self.update_names()
		self.update_buffer_0_bytes()
		# do 2 before 1 to ensure the buffer infos have been created
		self.update_buffer_2_bytes()
		self.update_buffer_1_bytes()
		# save multiple buffer_infos
		streams = self.external_streams()
		for buffer_info in streams:
			# update the modelstram name just incase
			buffer_info.name = f"{self.basename}{buffer_info.index}"
		self.modelstream_names[:] = [buffer_info.name for buffer_info in streams]
		logging.info(f"Writing to {filepath}")
		with open(filepath, "wb") as stream:
			self.write_fields(stream, self)
			stream.write(self.buffer_2_bytes)
			for buffer_info in streams:
				stream.write(self.get_all_bytes(buffer_info))

	def lookup_material(self):
		for model_i, model_info in enumerate(self.model_infos):
			# logging.debug(f"Mapping links for {name}")
			if self.lacks_mesh(model_info, model_i):
				continue
			for lod_index, lod in enumerate(model_info.model.lods):
				# logging.debug(f"Mapping LOD{lod_index}")
				lod.objects = model_info.model.objects[lod.first_object_index:lod.last_object_index]
				for obj in lod.objects:
					try:
						material = model_info.model.materials[obj.material_index]
						material.name = self.buffer_0.names[material.name_index]
						obj.mesh = model_info.model.meshes[obj.mesh_index].mesh
						obj.material = material
						# flag = int(obj.mesh.flag) if hasattr(obj.mesh, "flag") else None
						# logging.debug(
						# 	f"Mesh: {obj.mesh_index} Material: {material.name} Blend Mode: {material.blend_mode} "
						# 	f"Lod: {obj.mesh.poweroftwo} Flag: {flag}")
					except:
						logging.exception(f"Couldn't match material {obj.material_index} to mesh {obj.mesh_index}")

	def get_pack_base(self, bounds_min, bounds_max):
		"""Detect a suitable pack_base value depending on the bounds extent"""
		if self.context.version > 32:
			coord_min = np.min(bounds_min)
			coord_max = np.max(bounds_max)
			# just fall back to default when there are no models
			if coord_min != 0.0 or coord_max != 0.0:
				# use some slight tolerance to avoid wrapping the edge values
				tolerance = 1.05
				for pack_base in [float(2 ** x) for x in range(1, 16)]:
					if -pack_base < coord_min * tolerance and coord_max * tolerance < pack_base:
						return pack_base
		return 512.0

	def get_precision(self, pack_base):
		# precision is close to pack_base / PACKEDVEC_MAX but with some error
		return (pack_base + (pack_base * pack_base / PACKEDVEC_MAX)) / PACKEDVEC_MAX

	def clear(self):
		for model_info in self.model_infos:
			model_info.model.materials.clear()
			model_info.model.lods.clear()
			model_info.model.objects.clear()
			model_info.model.meshes.clear()


if __name__ == "__main__":
	m = Ms2File()
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC ovls/walker_export/SP_Scarecrow not working atm.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/Warhammer/Annihilator/annihilatormodels.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/acro/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/ceara/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/rhinoblack_child_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/StreetFoxCoffee/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/SP_Grave_Stones/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content0/Environment/Scenery/Themes/FT_FairyTale/FT_Topiary/FT_Topiary/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content0/Environment/Scenery/Themes/PR_Pirate/PR_Redcoat/PR_Redcoat/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content0/Rides/FlatRides/Chair-O-Plane/FR_COP/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/dino_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/models_polyp.ms2", read_editable=True)
	# for mo in m.model_infos:
	# 	for me in mo.model.meshes:
	# 		me.mesh.pack_verts()
	# 		# print("mesh")
	# 		# print(me.mesh.tri_indices)
	# 		me.mesh.tris = ((-1, list(me.mesh.tris)), )
	# 		# print(me.mesh.tri_indices)
	# 		# print(m)
	# m.save("C:/Users/arnfi/Desktop/models.ms2")
	m.load("C:/Users/arnfi/Desktop/resize/resized/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/models.ms2", read_editable=True)
	print(m)

	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content0/Rides/FlatRides/360_Power/FR_360PWR/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content0/Rides/FlatRides/Genie/Genie/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content0/Rides/Coasters/Tracks/Shared/TracksShared/css_004_models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content0/Rides/FlatRides/Hammer_Swing/FR_HSwing/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content0/Rides/FlatRides/The_Screaminator/FR_Scream/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content0/Rides/FlatRides/Wild_Blue/FR_WBlue/models.ms2", read_editable=True)

	# broken
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content4/Rides/Flat_Rides/Weisshorn/FR_WHorn/models.ms2", read_editable=True)
	
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/PDLC_WorldFair/Rides/Powered_Track_Rides/Tracks/Track_302/Track_302/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/PDLC_Vintage/Environment/Scenery/Themes/VT_Vintage/VT_Bandstand/VT_Bandstand/models.ms2", read_editable=True)

	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content0/Rides/FlatRides/Orbiter/FR_Orb/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content0/Rides/FlatRides/Star_Wheel/FR_StarW/models.ms2", read_editable=True)

	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content0/Environment/Scenery/Wallsets/ST_Stone/ST_Stone/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content0/Environment/Scenery/Themes/PR_Pirate/PR_Kraken/PR_Kraken/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content0/Environment/Scenery/Themes/PC_PlanetCoaster/PC_Archway/PC_Archway/models.ms2", read_editable=True)
	# m.load("C:/Program Files (x86)/Steam/steamapps/common/Planet Zoo/win64/ovldata/walker_export/Content2/Environment/Scenery/Wallsets/GL_Roof_02/GL_Roof_02/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/Content0/Characters/Mascots/Dino/Mascot_Dino/dino_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/PC OVLs/walker_export/PC_Primitives_01/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/doors/dlc11_stripdoors_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/rhinoblack_female_.ms2", read_editable=True, dump=True)
	# m.load("C:/Program Files (x86)/Steam/steamapps/common/Jurassic World Evolution 2/Win64/ovldata/walker_export/ContentPDLC5/Buildings/ModularStructures/LAG_NaturalWaterPool_Malta_Walls/LAG_NaturalWaterPool_Malta_Walls/models.ms2", read_editable=True)
	# m.load("C:/Program Files (x86)/Steam/steamapps/common/Jurassic World Evolution 2/Win64/ovldata/walker_export/ContentPDLC5/Buildings/ModularStructures/LAG_NaturalWaterPool_Malta/LAG_NaturalWaterPool_Malta/models.ms2", read_editable=True)
	# m.load("C:/Program Files (x86)/Steam/steamapps/common/Jurassic World Evolution 2/Win64/ovldata/walker_export/Content0/Buildings/Shared/Props/CharacterScale/CharacterScale/models.ms2", read_editable=True)
	# m.load("C:/Program Files (x86)/Steam/steamapps/common/Planet Zoo/win64/ovldata/walker_export/Content0/Animals/Aardvarks/Aardvark/Aardvark_Female/Aardvark_Female/aardvark_female_.ms2", read_editable=True)
	# m.load("C:/Program Files (x86)/Steam/steamapps/common/Planet Zoo/win64/ovldata/walker_export/Content0/Animals/Big_Cats/Bengal_Tiger/Bengal_Tiger_Male/Bengal_Tiger_Male/bengal_tiger_male_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/visual_lagoon_working.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/visual_lagoon_no_optimizer.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/ankylosaurus.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/calamite/tree_paleo_calamite.ms2", read_editable=True, dump=True)
	# m.load("C:/Users/arnfi/Desktop/mango/tree_mango.ms2", read_editable=True, dump=True)
	# m.load("C:/Users/arnfi/Desktop/ao_offroadvehicle_ - stock.ms2", read_editable=True)
	# print(m)
	# m.load("C:/Users/arnfi/Desktop/ao_offroadvehicle_.ms2", read_editable=True)
	# print(m)
	# m.load("C:/Users/arnfi/Desktop/models.ms2", read_editable=True)
	# for i, bone_info in enumerate(m.models_reader.bone_infos):
	# 	# for bi, bone in enumerate(bone_info.bones):
	# 		# print(bi, bone.name)
	# 	joints = bone_info.joints
	# 	for j in joints.joint_infos:
	# 		for hc in j.hitchecks:
	# 			print(hc)
	# 			hc.collider.is_optimized = 0
	# # 	# test for orthogonal vecs
	# # 	# for ragdoll in joints.ragdoll_constraints:
	# # 	# 	ragdoll.x.max = 0
	# # 	# 	ragdoll.x.min = 0
	# # 		# # ragdoll.z.max = 0
	# # 		# ragdoll.z.min = 0
	# # 		# print(ragdoll.parent, ragdoll.child)
	# # 		# print(ragdoll.rot.data)
	# # 		# print(np.linalg.inv(ragdoll.rot.data))
	# m.save("C:/Users/arnfi/Desktop/ankylosaurus_.ms2")
	# print(m)

# INFO | size 8 / count 1 = 8.0 in /PDLC_WorldFair/Rides/Coasters/Tracks/Track_003/Track_003/models.ms2; 0
# INFO | size 16 / count 1 = 16.0 in /PDLC_WorldFair/Rides/Powered_Track_Rides/Tracks/Track_302/Track_302/models.ms2; 0
# INFO | size 16 / count 2 = 8.0 in /PDLC_WorldFair/Environment/Scenery/Wallsets/WF_USA/WF_USA/models.ms2; 0
# INFO | size 32 / count 3 = 10.666666666666666 in /PDLC_WorldFair/Environment/Scenery/Wallsets/WF_USA/WF_USA/models.ms2; 0
# INFO | size 32 / count 4 = 8.0 in /PDLC_WorldFair/Environment/Scenery/Wallsets/WF_CHN/WF_CHN/models.ms2; 0
# INFO | size 40 / count 5 = 8.0 in /PDLC_Vintage/Environment/Scenery/Wallset/VT_Wood/VT_Wood/vt_wood_merge_arch_half_4m.ms2; 0
# INFO | size 80 / count 10 = 8.0 in /PDLC_Spooky/Environment/Scenery/Wallsets/SP_HauntedHouse/SP_HauntedHouse/models.ms2; 0
# INFO | size 24 / count 3 = 8.0 in /PDLC_WorldFair/Environment/Scenery/Wallsets/WF_SPN/WF_SPN/models.ms2; 0
# INFO | size 24 / count 2 = 12.0 in /PDLC_WorldFair/Environment/Scenery/Wallsets/WF_USA/WF_USA/models.ms2; 0
# INFO | size 80 / count 9 = 8.88888888888889 in /PDLC_Adventure/Environment/Scenery/Themes/AD_Adventure/AD_Statue_Snake/AD_Statue_Snake/models.ms2; 0
# INFO | size 72 / count 9 = 8.0 in /PDLC_Vintage/Environment/Scenery/Wallset/VT_Wood/VT_Wood/vt_wood_merge_arch_4m.ms2; 0
# INFO | size 136 / count 16 = 8.5 in /Content0/Environment/Scenery/Themes/FT_FairyTale/FT_RoyalGazebo/FT_RoyalGazebo/models.ms2; 0
# INFO | size 48 / count 5 = 9.6 in /PDLC_Vintage/Environment/Scenery/Themes/VT_Vintage/VT_Arch_Pillar_Roofs/VT_Arch_Pillar_Roofs/models.ms2; 0
# INFO | size 64 / count 7 = 9.142857142857142 in /PDLC_WorldFair/Environment/Scenery/Themes/WF_WorldFair/WF_Planter_FRA/WF_Planter_FRA/models.ms2; 0
# INFO | size 96 / count 11 = 8.727272727272727 in /Content0/Environment/Scenery/Themes/PC_PlanetCoaster/PC_Archway/PC_Archway/models.ms2; 0
# INFO | size 40 / count 4 = 10.0 in /PDLC_WorldFair/Environment/Scenery/Wallsets/WF_USA/WF_USA/models.ms2; 0
# INFO | size 72 / count 8 = 9.0 in /Content0/Environment/Scenery/Wallsets/WD_Wood/WD_Wood/models.ms2; 0
# INFO | size 56 / count 6 = 9.333333333333334 in /PDLC_WorldFair/Environment/Scenery/Themes/WF_WorldFair/WF_Gondola_ITA/WF_Gondola_ITA/models.ms2; 0
# INFO | size 184 / count 23 = 8.0 in /Content0/Environment/Scenery/Themes/WS_Western/WS_PaddleSteamer/WS_PaddleSteamer/models.ms2; 0
# INFO | size 48 / count 6 = 8.0 in /PDLC_Spooky/Environment/Scenery/Wallsets/SP_HauntedHouse/SP_HauntedHouse/models.ms2; 0
# INFO | size 96 / count 12 = 8.0 in /Content0/Environment/Scenery/Wallsets/ST_Stone_B/ST_Stone_B/models.ms2; 0
# INFO | size 88 / count 11 = 8.0 in /Content0/Environment/Scenery/Wallsets/ST_Stone_B/ST_Stone_B/models.ms2; 0
# INFO | size 88 / count 10 = 8.8 in /Content2/Environment/Scenery/Themes/FT_Fairytale/FT_Rope_Pieces/FT_Rope_Pieces/models.ms2; 0
# INFO | size 56 / count 6 = 9.333333333333334 in /Content0/Rides/TransportRides/Cars/Connie/TR_Connie/models.ms2; 1
# INFO | size 40 / count 5 = 8.0 in /PDLC_Adventure/Rides/Coasters/Cars/GoldFever/CC_GoldFever/models.ms2; 1
# INFO | size 40 / count 4 = 10.0 in /Content3/Rides/Coasters/Cars/ViperOne/CC_ViperOne/models.ms2; 1
# INFO | size 56 / count 7 = 8.0 in /Content0/Rides/Coasters/Cars/Barghest/CC_Barghest/models.ms2; 1
# INFO | size 32 / count 3 = 10.666666666666666 in /PDLC_RidePack1/Rides/Coasters/Cars/SteelMultiRole/CC_SteelMultiRole/models.ms2; 1
# INFO | size 32 / count 4 = 8.0 in /Content4/Rides/Coasters/Cars/Zenith/CC_Zenith/models.ms2; 1
# INFO | size 24 / count 3 = 8.0 in /PDLC_WorldFair/Rides/Coasters/Cars/Jixxer/CC_Jixxer/models.ms2; 1
# INFO | size 24 / count 2 = 12.0 in /PDLC_Vintage/Rides/Coasters/Cars/CC_FTurns/CC_FTurns/models.ms2; 1
# INFO | size 16 / count 1 = 16.0 in /Content3/Rides/Coasters/Cars/Degen/CC_Degen/models.ms2; 1
# INFO | size 48 / count 5 = 9.6 in /Content1/Rides/TransportRides/Cars/IronHorse/TR_IronHorse/models.ms2; 1
# INFO | size 16 / count 2 = 8.0 in /PDLC_WorldFair/Rides/Powered_Track_Rides/Cars/PMover/TR_PMover/models.ms2; 1
# INFO | size 8 / count 1 = 8.0 in /PDLC_Spooky/Rides/Powered_Track_Rides/The_Huntsman/PTR_Huntsman/models.ms2; 1
# INFO | size 80 / count 9 = 8.88888888888889 in /Content0/Rides/Coasters/Cars/Stingray/CC_SRay/models.ms2; 1
# INFO | size 48 / count 6 = 8.0 in /PDLC_WorldFair/Rides/Coasters/Cars/Jixxer/CC_Jixxer/models.ms2; 1
# INFO | size 112 / count 13 = 8.615384615384615 in /PDLC_Vintage/Environment/Scenery/Themes/VT_Vintage/VT_Bandstand/VT_Bandstand/models.ms2; 0
# INFO | size 104 / count 12 = 8.666666666666666 in /Content1/Environment/Scenery/Wallsets/HOL_GBread/HOL_Gbread/models.ms2; 0
# INFO | size 56 / count 7 = 8.0 in /PDLC_Vintage/Environment/Scenery/Themes/VT_Vintage/VT_Arch_Pillar_Roofs/VT_Arch_Pillar_Roofs/models.ms2; 0
# INFO | size 24 / count 1 = 24.0 in /GameMain/Main/nullphysicsskeleton_.ms2; 1
# INFO | size 64 / count 8 = 8.0 in /PDLC_RidePack1/Environment/Scenery/RP1_CycloidSpinBackboards/RP1_CycloidSpinBackboards/models.ms2; 0

	#


	# m.load("C:/Users/arnfi/Desktop/ptera_JWE1/pteranodon_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/anky_JWE1/ankylosaurus.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/moose/alaskan_moose_male_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/janitormale_.ms2", read_editable=True)
	# m.save("C:/Users/arnfi/Desktop/test.ms2")
	# m.load("C:/Users/arnfi/Desktop/jwe2/pyro/export/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/pyro/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/moros/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/ankylodocus.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/pteranodon_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/rabbit_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/bush_berry_bear.ms2", read_editable=True)
	# print(m.models_reader.bone_infos[0])
	# print(m)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/MeshCollision/JWE2/CharacterScale/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/MeshCollision/PZ/widgetball_test_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/MeshCollision/PZ/CM_Common_Roofs.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/MeshCollision/JWE2dev/groundplane_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/Coding/Frontier/MeshCollision/JWE2dev/footplantingtest_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/export/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/hazard_ceilingfan_.ms2", read_editable=True)
	# print(m.models_reader.bone_infos[0])
	# mods = set()
	# flags = set()
	# for bone_info in m.models_reader.bone_infos:
	# 	# print(bone_info)
	# 	if bone_info.joint_count:
	# 		for ji in bone_info.joints.joint_infos:
	# 			for hc in ji.hitchecks:
	# 				if hc.dtype == CollisionType.MESH_COLLISION:
	# 					print(hc)
	# for mo in m.model_infos:
	# 	# print(mo.bone_info)
	# 	# print(mo.model.lods)
	# 	# print(mo.model.objects)
	# 	for i, me in enumerate(mo.model.meshes):
	# 		# print(i, me)
	# # 		# for t, v in zip(me.mesh.tri_chunks, me.mesh.vert_chunks):
	# # 		# 	t.rot.a = 1.0
	# # 		# 	t.rot.x = t.rot.y = t.rot.z = 0.0
	# # 		# 	t.loc.x = t.loc.y = t.loc.z = 0.0
	# 		for t, v in zip(me.mesh.tri_chunks, me.mesh.vert_chunks):
	# 			# print(t, v)
	# 			print(v)
	# 			s = v.pack_base / v.scale
	# 			print(s)
	# 			break
	# 			# flags.add(tuple(v.flags))
	# 		print(flags)
			# 	pass
			# 	# print(i, t.tris_offset)
			# 	# print(i, v.vertex_offset % 16)
			# 	mods.add(v.vertex_offset % 16)
	# 		flags.add(me.mesh.flag)
	# print(mods)
			# if i in (12, 13, 14):
			# if i in (12, ):
			# 	print(i)
			# 	for ch_i in range(10):
			# 		tri_ch = me.mesh.tri_chunks[ch_i]
			# 		vert_ch = me.mesh.vert_chunks[ch_i]
			# 		# print(tri_ch)
			# 		av = np.mean(vert_ch.normals, axis=0)
			# 		md = np.median(vert_ch.normals, axis=0)
			# 		# print(tri_ch.rot, pack_swizzle(av / np.linalg.norm(av)), pack_swizzle(md / np.linalg.norm(md)), vert_ch.normals[0])
			# 		print(tri_ch.rot, pack_swizzle(vert_ch.normals[0]), pack_swizzle(vert_ch.normals[-1]), )
			# 		print(np.linalg.norm((tri_ch.rot.x, tri_ch.rot.y, tri_ch.rot.z, )), )
	# m.save("C:/Users/arnfi/Desktop/export/models.ms2")

	# m.load("C:/Users/arnfi/Desktop/park_captainhook_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/export/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/baryo/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/park_snowwhite_.ms2", read_editable=True)
	# print(m.models_reader.bone_infos[0].bone_names)
	# print(m.buffer_0.names[142])
	# m.load("C:/Users/arnfi/Desktop/shop_mainstreet_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/c_bz_shipparts_.ms2", read_editable=True)
	# print(m)
	# m.load("C:/Users/arnfi/Desktop/nile_lechwe_male_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/tree_palm_coconut_desert.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/export/tree_palm_coconut_desert.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/export/tree_palm_coconut.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/rhinoblack_female_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/caribou/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/models.ms2", read_editable=True)
	# m.load("C:/Program Files (x86)/Steam/steamapps/common/Jurassic World Evolution 2/Win64/ovldata/walker_export/ContentPDLC3/Dinosaurs/Land/Therizinosaurus/Therizinosaurus/models.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/pine/tree_pine_blackspruce.ms2", read_editable=True)

	# m.load("C:/Users/arnfi/Desktop/tree_palm_coconut_desert.ms2", read_editable=True)
	# for model_info in m.model_infos:
	# 	for w in model_info.model.meshes:
	# 		me = w.mesh
	# 		me.vertices[:, 1] += np.sin(np.pi * me.vertices[:, 2] * 0.2) * 2
	# 		# me.vertices[:, 2] *= 2
	# 		me.pack_verts()
	# m.save("C:/Users/arnfi/Desktop/export/tree_palm_coconut_desert.ms2")

	# m.load("C:/Users/arnfi/Desktop/dilophosaurus.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/diplodocus.ms2", read_editable=True)
	# m.save("C:/Users/arnfi/Desktop/models.ms2")
	# m.load("C:/Users/arnfi/Desktop/paths_new/strips.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/bornean_orangutan_male_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/acacia/tree_acacia_umbrella_thorn.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/scimitar_horned_oryx_female_.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/quetz.ms2", read_editable=True)
	# m.save("C:/Users/arnfi/Desktop/models.ms2")
	# print(m)
	# print(m.model_infos[1].bone_info.joints.joint_infos)
