import os
import io
import time
import traceback
import logging

from generated.formats.ms2.compound.Ms2InfoHeader import Ms2InfoHeader
from generated.formats.ms2.versions import *
from generated.formats.ovl_base.basic import ConvStream
from generated.formats.ovl.basic import basic_map
from generated.io import IoFile
from modules.formats.shared import get_padding_size, djb2, get_padding

logging.basicConfig(level=logging.DEBUG)


class Ms2Context:
	def __init__(self):
		self.version = 0

	def __repr__(self):
		return f"{self.version}"


class Ms2File(Ms2InfoHeader, IoFile):

	basic_map = basic_map

	def __init__(self, ):
		super().__init__(Ms2Context())

	def assign_joints(self, bone_info):
		if not hasattr(bone_info, "joints"):
			logging.warning(f"Joints deactivated for debugging")
			return
		if self.context.version >= 47:
			for i, x in enumerate(bone_info.struct_7.unknown_list):
				# print(i)
				# print(self.bone_info.bones[x.child], x.child)
				# print(self.bone_info.bones[x.parent], x.parent)
				x.child_name = bone_info.bones[x.child].name
				x.parent_name = bone_info.bones[x.parent].name
				assert x.zero == 0
				assert x.one == 1
			assert bone_info.one == 1
		assert bone_info.name_count == bone_info.bind_matrix_count == bone_info.bone_count == bone_info.parents_count == bone_info.enum_count
		assert bone_info.zeros_count == 0 or bone_info.zeros_count == bone_info.name_count
		assert bone_info.unk_78_count == 0 and bone_info.unk_extra == 0
		joints = bone_info.joints
		for joint_info in joints.joint_infos:
			joint_info.name = joints.joint_names.get_str_at(joint_info.name_offset)
			for hit in joint_info.hitchecks:
				hit.name = joints.joint_names.get_str_at(hit.name_offset)
		# print(joints)

		# for ix, li in enumerate((joints.first_list, joints.short_list, joints.long_list)):
		# 	print(f"List {ix}")
		# 	for i, x in enumerate(li):
		# 		print(i)
		# 		print(joints.joint_infos[x.parent].name, x.parent)
		# 		print(joints.joint_infos[x.child].name, x.child)

		if bone_info.joint_count:
			for bone_i, joint_info in zip(joints.joint_indices, joints.joint_infos):
				# usually, this corresponds - does not do for speedtree but does not matter
				joint_info.bone_name = bone_info.bones[bone_i].name
				if not joint_info.bone_name == joint_info.name:
					logging.warning(f"bone name [{joint_info.bone_name}] doesn't match joint name [{joint_info.name}]")
				if joints.joint_infos[joints.bone_indices[bone_i]] != joint_info:
					logging.warning(f"bone index [{bone_i}] doesn't point to expected joint info")

	def assign_bone_names(self, bone_info):
		try:
			for name_i, bone in zip(bone_info.name_indices, bone_info.bones):
				bone.name = self.buffer_0.names[name_i]
		except:
			logging.error("Names failed...")

	def load(self, filepath, read_bytes=False, read_editable=False):
		start_time = time.time()
		self.filepath = filepath
		self.dir, self.name = os.path.split(os.path.normpath(filepath))
		self.read_editable = read_editable
		logging.debug(f"Reading {self.filepath}")
		with self.reader(filepath) as stream:
			self.read(stream)
			if is_old(self.info):
				self.buffer_1_offset = self.buffer_infos.io_start
			else:
				self.buffer_1_offset = self.models_reader.bone_info_start
			self.buffer_2_offset = self.buffer_1_offset + self.bone_info_size

			# logging.info(self)
			# return
			# logging.debug(f"end of header: {self.buffer_1_offset}")

			logging.info(f"Vertex buffer starts at {self.buffer_2_offset}")
			try:
				for bone_info in self.models_reader.bone_infos:
					self.assign_bone_names(bone_info)
					self.assign_joints(bone_info)
			except:
				logging.warning(f"Joints or bones lookup failed")
				traceback.print_exc()
			try:
				self.lookup_material()
			except:
				logging.warning(f"Material lookup failed")
				traceback.print_exc()

			if read_bytes:
				stream.seek(self.buffer_0.io_start)
				self.buffer_0_bytes = stream.read(self.buffer_0.io_size)
				stream.seek(self.buffer_1_offset)
				self.buffer_1_bytes = stream.read(self.bone_info_size)
				self.buffer_2_bytes = stream.read()
			else:
				stream.seek(self.buffer_2_offset)
				self.buffer_2_bytes = stream.read()
		# attach the streams to each buffer_info
		for buffer_info, modelstream_name in zip(self.buffer_infos, self.modelstream_names):
			buffer_info.name = modelstream_name
			buffer_info.path = os.path.join(self.dir, buffer_info.name)
			logging.info(f"Loading {buffer_info.path}")
			with open(buffer_info.path, "rb") as modelstream_reader:
				buffer_info.stream = ConvStream(modelstream_reader.read())
		# attach the static stream to last buffer_info
		if self.buffer_infos:
			static_buffer_info = self.buffer_infos[-1]
			static_buffer_info.stream = ConvStream(self.buffer_2_bytes)
			static_buffer_info.name = "STATIC"
			static_buffer_info.path = None
		if read_editable:
			self.load_meshes()

		logging.debug(f"Read {self.name} in {time.time() - start_time:.2f} seconds")

	def load_meshes(self):
		for mdl2_name, model_info in zip(self.mdl_2_names, self.model_infos):
			logging.debug(f"Loading mesh data for {mdl2_name}")
			# sort by lod, read those with offset first
			# sorted_meshes = sorted(reversed(list(enumerate(model_info.model.meshes))), key=lambda x: (x[1].poweroftwo, x[1].vertex_offset))
			# sorted_meshes = sorted(reversed(list(enumerate(model_info.model.meshes))), key=lambda x: x[1].vertex_offset)
			sorted_meshes = list(enumerate(model_info.model.meshes))
			# logging.debug(f"PC mesh, {len(model_info.model.meshes)} meshes")
			sum_uv_dict = {}
			for i, wrapper in sorted_meshes:
				if wrapper.mesh.stream_index not in sum_uv_dict:
					sum_uv_dict[wrapper.mesh.stream_index] = 0
				sum_uv_dict[wrapper.mesh.stream_index] += wrapper.mesh.vertex_count

			last_vertex_offset = 0
			# for i, mesh in sorted_meshes:
			# 	print(i, mesh.vertex_offset, mesh.vertex_offset + mesh.vertex_count*24)
			if is_old(self.info):
				pack_offset = 512
			else:
				pack_offset = model_info.pack_offset
			try:
				for i, wrapper in sorted_meshes:
					logging.info(f"Populating mesh {i}")
					last_vertex_offset = wrapper.mesh.populate(self, pack_offset, last_vertex_offset=last_vertex_offset, sum_uv_dict=sum_uv_dict)
			except:
				traceback.print_exc()

	def update_joints(self, bone_info):
		bone_lut = {bone.name: bone_index for bone_index, bone in enumerate(bone_info.bones)}

		for entry in bone_info.struct_7.unknown_list:
			# indices into bones
			entry.parent = bone_lut[entry.parent_name]
			entry.child = bone_lut[entry.child_name]

		# print(bone_info.joints)
		joints = bone_info.joints
		for l_list in (joints.first_list, joints.short_list, joints.long_list,):
			for l_entry in l_list:
				# these link into joints.joint_infos
				# no need to update right now, but later
				pass
		# make sure these have the correct size
		joints.joint_indices.resize(joints.joint_count)
		joints.bone_indices.resize(joints.bone_count)
		# reset bone -> joint mapping since we don't catch them all if we loop over existing joints
		joints.bone_indices[:] = -1
		# link between bones and joints, in both directions
		for joint_i, joint_info in enumerate(joints.joint_infos):
			bone_i = bone_lut[joint_info.bone_name]
			joints.joint_indices[joint_i] = bone_i
			joints.bone_indices[bone_i] = joint_i

		# todo - update joint JointData.names buffer + JointInfo.name_offset

	def rename(self, name_tups):
		"""Renames strings in the main name buffer"""
		logging.info(f"Renaming in {self.name}")

		for model_info in self.model_infos:
			for material in model_info.model.materials:
				self._rename(material, name_tups)
			if model_info.bone_info:
				for bone in model_info.bone_info.bones:
					self._rename(bone, name_tups)

	def _rename(self, element, name_tups):
		# first a cases sensitive pass
		for old, new in name_tups:
			if old in element.name:
				logging.debug(f"Match for '{old}' in '{element.name}'")
				element.name = element.name.replace(old, new)
		for old, new in name_tups:
			if old.lower() in element.name.lower():
				logging.debug(f"Case-insensitive match '{old}' in '{element.name}'")
				element.name = element.name.lower().replace(old, new)

	def get_name_index(self, name):
		if name not in self.buffer_0.names:
			self.buffer_0.names.append(name)
		return self.buffer_0.names.index(name)

	def update_names(self):
		logging.info("Updating MS2 name buffer")
		self.buffer_0.names.clear()
		for model_info in self.model_infos:
			for material in model_info.model.materials:
				material.name_index = self.get_name_index(material.name)
			if model_info.bone_info:
				for bone_index, bone in enumerate(model_info.bone_info.bones):
					model_info.bone_info.name_indices[bone_index] = self.get_name_index(bone.name)
				self.update_joints(model_info.bone_info)
		# print(self.buffer_0.names)
		logging.info("Updating MS2 name hashes")
		# update hashes from new names
		self.info.name_count = len(self.buffer_0.names)
		self.buffer_0.name_hashes.resize(len(self.buffer_0.names))
		for name_i, name in enumerate(self.buffer_0.names):
			self.buffer_0.name_hashes[name_i] = djb2(name.lower())

	def update_buffer_0_bytes(self):
		with ConvStream() as temp_writer:
			self.buffer_0.write(temp_writer)
			self.buffer_0_bytes = temp_writer.getvalue()

	def update_buffer_1_bytes(self):
		with ConvStream() as temp_bone_writer:
			self.models_reader.write(temp_bone_writer)
			self.buffer_1_bytes = temp_bone_writer.getvalue()[self.models_reader.bone_info_start:]
			self.bone_info_size = self.models_reader.bone_info_size

	def update_buffer_2_bytes(self):
		if self.read_editable:
			logging.debug(f"Updating buffer 2")
			# first init all writers for the buffers
			for buffer_info in self.buffer_infos:
				# write each mesh's vert & tri block to a temporary buffer
				buffer_info.verts = io.BytesIO()
				buffer_info.tris = io.BytesIO()
			# now store each model
			for mdl2_name, model_info in zip(self.mdl_2_names, self.model_infos):
				logging.debug(f"Storing {mdl2_name}")
				# update ModelInfo
				model_info.num_materials = len(model_info.model.materials)
				model_info.num_lods = len(model_info.model.lods)
				model_info.num_objects = len(model_info.model.objects)
				model_info.num_meshes = len(model_info.model.meshes)
				# update MeshData
				for wrapper in model_info.model.meshes:
					wrapper.mesh.assign_stream(self.buffer_infos)
					wrapper.mesh.write_data()
				# update LodInfo
				logging.debug(f"Updating lod vertex counts...")
				for lod in model_info.model.lods:
					lod.vertex_count = sum(wrapper.mesh.vertex_count for wrapper in lod.meshes)
					lod.tri_index_count = sum(wrapper.mesh.tri_index_count for wrapper in lod.meshes)
					logging.debug(f"lod.vertex_count = {lod.vertex_count}")
					logging.debug(f"lod.tri_index_count = {lod.tri_index_count}")
			# modify buffer size
			for buffer_info in self.buffer_infos:
				# get bytes from IO obj
				buffer_info.vert_bytes = buffer_info.verts.getvalue()
				buffer_info.tris_bytes = buffer_info.tris.getvalue()
				buffer_info.vertex_buffer_size = len(buffer_info.vert_bytes)
				buffer_info.tris_buffer_size = len(buffer_info.tris_bytes)
			# store static buffer
			if self.buffer_infos:
				static_buffer_info = self.buffer_infos[-1]
				self.buffer_2_bytes = static_buffer_info.vert_bytes + static_buffer_info.tris_bytes

	@property
	def buffers(self):
		return self.buffer_0_bytes, self.buffer_1_bytes, self.buffer_2_bytes

	def save(self, filepath):
		self.dir, self.name = os.path.split(os.path.normpath(filepath))
		logging.info("Pre-writing buffers")
		self.update_names()
		self.update_buffer_0_bytes()
		self.update_buffer_1_bytes()
		self.update_buffer_2_bytes()
		logging.info(f"Writing to {filepath}")
		with self.writer(filepath) as f:
			self.write(f)
			f.write(self.buffer_2_bytes)
		# save multiple buffer_infos
		for buffer_info in self.buffer_infos:
			if buffer_info.name != "STATIC":
				buffer_info.path = os.path.join(self.dir, buffer_info.name)
				with open(buffer_info.path, "wb") as f:
					f.write(buffer_info.vert_bytes + buffer_info.tris_bytes)

	def lookup_material(self):
		for name, model_info in zip(self.mdl_2_names, self.model_infos):
			logging.debug(f"Mapping links for {name}")
			for lod_index, lod in enumerate(model_info.model.lods):
				lod.objects = model_info.model.objects[lod.first_object_index:lod.last_object_index]
				# todo - investigate how duplicate meshes are handled for the lod's vertex count0
				lod.meshes = tuple(model_info.model.meshes[obj.mesh_index] for obj in lod.objects)
				logging.debug(f"LOD{lod_index}")
				for obj in lod.objects:
					try:
						material = model_info.model.materials[obj.material_index]
						material.name = self.buffer_0.names[material.name_index]
						obj.mesh = model_info.model.meshes[obj.mesh_index].mesh
						obj.material = material
						flag = int(obj.mesh.flag) if hasattr(obj.mesh, "flag") else None
						logging.debug(
							f"Mesh: {obj.mesh_index} Material: {material.name} Material Unk: {material.some_index} "
							f"Lod Index: {obj.mesh.poweroftwo} Flag: {flag}")
					except Exception as err:
						logging.error(err)
						logging.error(f"Couldn't match material {obj.material_index} to mesh {obj.mesh_index}")

	def clear(self):
		for model_info in self.model_infos:
			model_info.model.materials.clear()
			model_info.model.lods.clear()
			model_info.model.objects.clear()
			model_info.model.meshes.clear()


if __name__ == "__main__":
	m = Ms2File()
	# m.load("C:/Users/arnfi/Desktop/rhinoblack_female_.ms2", read_editable=True)
	m.load("C:/Users/arnfi/Desktop/pine/tree_pine_blackspruce.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/dilophosaurus.ms2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/diplodocus.ms2", read_editable=True)
	# m.save("C:/Users/arnfi/Desktop/test.ms2")
	# print(m)
	# print(m.model_infos[1].bone_info.joints.joint_infos)
