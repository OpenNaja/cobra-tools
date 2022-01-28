import os
import io
import time
import traceback
import logging

from generated.formats.ms2.compound.Ms2InfoHeader import Ms2InfoHeader
from generated.formats.ms2.versions import *
from generated.io import IoFile, BinaryStream
from modules.formats.shared import get_padding_size, djb, get_padding

logging.basicConfig(level=logging.DEBUG)


class Ms2Context:
	def __init__(self):
		self.version = 0

	def __repr__(self):
		return f"{self.version}"


class Ms2File(Ms2InfoHeader, IoFile):

	def __init__(self, ):
		super().__init__(Ms2Context())

	def assign_joints(self, bone_info):
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
		self.filepath = filepath
		self.dir, self.basename = os.path.split(os.path.normpath(filepath))
		self.read_editable = read_editable
		logging.debug(f"Reading {self.basename}")
		with self.reader(filepath) as stream:
			self.read(stream)
			if is_old(self.info):
				self.buffer_1_offset = self.buffer_info.io_start
			else:
				self.buffer_1_offset = self.models_reader.bone_info_start
			self.buffer_2_offset = self.buffer_1_offset + self.bone_info_size
			# logging.debug(self)
			# logging.debug(f"end of header: {self.buffer_1_offset}")
			for bone_info in self.models_reader.bone_infos:
				self.assign_bone_names(bone_info)
				self.assign_joints(bone_info)

			self.lookup_material()
			if read_editable:
				self.load_mesh()
			if read_bytes:
				# make all 3 buffers accesible as bytes
				self.update_buffer_0_bytes()
				stream.seek(self.buffer_1_offset)
				self.buffer_1_bytes = stream.read(self.bone_info_size)
				self.buffer_2_bytes = stream.read()

	def load_mesh(self):
		# numpy chokes on bytes io objects
		with open(self.filepath, "rb") as stream:
			stream.seek(self.buffer_2_offset)
			logging.debug(f"buffer_2_offset {self.buffer_2_offset}")
			for mdl2_name, model_info in zip(self.mdl_2_names, self.model_infos):
				if is_old(self.info):
					# logging.debug(f"PC mesh, {len(model_info.model.meshes)} meshes")
					sum_uv_dict = {}
					for mesh in model_info.model.meshes:
						if mesh.stream_index not in sum_uv_dict:
							sum_uv_dict[mesh.stream_index] = 0
						sum_uv_dict[mesh.stream_index] += mesh.vertex_count
					last_vertex_offset = 0
					# sort by lod, read those with offset first
					# sorted_meshes = sorted(reversed(list(enumerate(model_info.model.meshes))), key=lambda x: (x[1].poweroftwo, x[1].vertex_offset))
					# sorted_meshes = sorted(reversed(list(enumerate(model_info.model.meshes))), key=lambda x: x[1].vertex_offset)
					sorted_meshes = list(enumerate(model_info.model.meshes))
					for i, mesh in sorted_meshes:
						print(i, mesh.vertex_offset, mesh.vertex_offset + mesh.vertex_count*24)
					try:
						for i, mesh in sorted_meshes:
							logging.info(f"Populating mesh {i}")
							last_vertex_offset = mesh.populate(
								self, stream, self.buffer_2_offset, 512, last_vertex_offset=last_vertex_offset, sum_uv_dict=sum_uv_dict)
					except:
						traceback.print_exc()
						# print(self)
				else:
					# if mdl2.read_editable:
					logging.debug(f"Loading editable mesh data for {mdl2_name}")
					for mesh in model_info.model.meshes:
						mesh.populate(self, stream, self.buffer_2_offset, model_info.pack_offset)
					#
					# elif mdl2.map_bytes:
					# 	logging.debug(f"Reading mesh statistics for {mdl2_name}")
					# 	for model in mdl2.model.meshes:
					# 		model.read_bytes_map(self.buffer_2_offset, stream)
					#
					# # store binary data for verts and tris on the mesh
					# elif mdl2.read_bytes:
					# 	logging.debug(f"Copying mesh data for {mdl2_name}")
					# 	for model in mdl2.model.meshes:
					# 		model.read_bytes(self.buffer_2_offset, self.buffer_info.vertexdatasize, stream)

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
		logging.info(f"Renaming on {self.basename}")
		for i, name in enumerate(self.buffer_0.names):
			# first a cases sensitive pass
			for old, new in name_tups:
				name = self.buffer_0.names[i]
				if old in self.buffer_0.names[i]:
					logging.debug(f"Match for '{old}' in '{name}'")
					self.buffer_0.names[i] = name.replace(old, new)
			for old, new in name_tups:
				name = self.buffer_0.names[i]
				if old.lower() in name.lower():
					logging.debug(f"Case-insensitive match '{old}' in '{name}'")
					self.buffer_0.names[i] = name.lower().replace(old, new)

	def update_names(self):
		logging.info("Updating MS2 name buffer")
		# only update the names buffer if mdl2s have been loaded
		if self.model_infos:
			self.buffer_0.names.clear()
			for model_info in self.model_infos:
				for material in model_info.model.materials:
					if material.name not in self.buffer_0.names:
						self.buffer_0.names.append(material.name)
					material.name_index = self.buffer_0.names.index(material.name)
				for bone_index, bone in enumerate(model_info.bone_info.bones):
					if bone.name not in self.buffer_0.names:
						self.buffer_0.names.append(bone.name)
					model_info.bone_info.name_indices[bone_index] = self.buffer_0.names.index(bone.name)
				self.update_joints(model_info.bone_info)
		# print(self.buffer_0.names)
		logging.info("Updating MS2 name hashes")
		# update hashes from new names
		self.info.name_count = len(self.buffer_0.names)
		self.buffer_0.name_hashes.resize(len(self.buffer_0.names))
		for name_i, name in enumerate(self.buffer_0.names):
			self.buffer_0.name_hashes[name_i] = djb(name.lower())

	def update_buffer_0_bytes(self):
		with BinaryStream() as temp_writer:
			self.buffer_0.write(temp_writer)
			self.buffer_0_bytes = temp_writer.getvalue()

	def update_buffer_1_bytes(self):
		with BinaryStream() as temp_bone_writer:
			self.write_all_bone_infos(temp_bone_writer)
			self.buffer_1_bytes = temp_bone_writer.getvalue()
			self.bone_info_size = temp_bone_writer.tell() - self.models_reader.bone_info_start

	def update_buffer_2_bytes(self):
		if self.read_editable:
			logging.debug(f"Updating buffer 2")
			# write each mesh's vert & tri block to a temporary buffer
			temp_vert_writer = io.BytesIO()
			temp_tris_writer = io.BytesIO()
			for mdl2_name, model_info in zip(self.mdl_2_names, self.model_infos):
				for mesh in model_info.model.meshes:
					# update MeshData struct
					mesh.vertex_offset = temp_vert_writer.tell()
					mesh.tri_offset = temp_tris_writer.tell()
					logging.debug(f"Storing {mdl2_name}")
					mesh.vertex_count = len(mesh.verts)
					mesh.tri_index_count = len(mesh.tri_indices) * mesh.shell_count
					# write data
					mesh.write_verts(temp_vert_writer)
					mesh.write_tris(temp_tris_writer)
			self.update_lod_vertex_counts()
			# get bytes from IO obj
			vert_bytes = temp_vert_writer.getvalue()
			tris_bytes = temp_tris_writer.getvalue()
			# modify buffer size
			self.buffer_info.vertexdatasize = len(vert_bytes)
			self.buffer_info.facesdatasize = len(tris_bytes)
			self.buffer_2_bytes = vert_bytes + tris_bytes

	def save(self, filepath):
		# exp = "export"
		# exp_dir = os.path.join(self.dir, exp)
		# os.makedirs(exp_dir, exist_ok=True)

		logging.info("Writing verts and tris to temporary buffer")
		self.update_names()

		self.update_buffer_0_bytes()
		self.update_buffer_1_bytes()
		self.update_buffer_2_bytes()
		# write output ms2
		logging.info("Writing final output")
		with self.writer(filepath) as f:
			self.write(f)
			f.write(self.buffer_1_bytes)
			f.write(self.buffer_2_bytes)

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
						obj.mesh = model_info.model.meshes[obj.mesh_index]
						obj.material = material
						logging.debug(
							f"Mesh: {obj.mesh_index} Material: {material.name} Material Unk: {material.some_index} "
							f"Lod Index: {obj.mesh.poweroftwo} Flag: {int(obj.mesh.flag)}")
					except Exception as err:
						logging.error(err)
						logging.error(f"Couldn't match material {obj.material_index} to mesh {obj.mesh_index}")

	def clear(self):
		for model_info in self.model_infos:
			model_info.model.materials.clear()
			model_info.model.lods.clear()
			model_info.model.objects.clear()
			model_info.model.meshes.clear()

	def update_counts(self):
		for model_info in self.model_infos:
			model_info.num_materials = len(model_info.model.materials)
			model_info.num_lods = len(model_info.model.lods)
			model_info.num_objects = len(model_info.model.objects)
			model_info.num_meshes = len(model_info.model.meshes)

	def update_lod_vertex_counts(self):
		logging.debug(f"Updating lod vertex counts...")
		for model_info in self.model_infos:
			for lod in model_info.model.lods:
				lod.vertex_count = sum(model.vertex_count for model in lod.meshes)
				lod.tri_index_count = sum(model.tri_index_count for model in lod.meshes)
				logging.debug(f"lod.vertex_count = {lod.vertex_count}")
				logging.debug(f"lod.tri_index_count = {lod.tri_index_count}")


if __name__ == "__main__":
	m = Ms2File()
	m.load("C:/Users/arnfi/Desktop/ichthyo/ichthyosaurus.mdl2", read_editable=True)
	# m.load("C:/Users/arnfi/Desktop/frb/frbmodel_rock_tree_branch_01.mdl2", entry=True, read_editable=True)
	# for mesh in m.meshes:
	# 	print(mesh.tris)
	# 	mesh.validate_tris()
	# m.load("C:/Users/arnfi/Desktop/fra/framodel_rock_tree_branch_01.mdl2", entry=True, read_editable=True)

	# m.load("C:/Users/arnfi/Desktop/armadillo/ninebanded_armadillo.mdl2", entry=True)
	# m.load("C:/Users/arnfi/Desktop/test/fine/wm_skeleton_base_02.mdl2")
	# m.load("C:/Users/arnfi/Desktop/test/test/wm_skeleton_base_02.mdl2")
# m.load("C:/Users/arnfi/Desktop/redwood/tris1_scr_redwood_01.mdl2", read_editable=True)
# m.load("C:/Users/arnfi/Desktop/Coding/ovl/dev/out/PZ/Main PZ big/widgetball_test.mdl2")
# m.load("C:/Users/arnfi/Desktop/redwood/tris1_scr_redwood_01.mdl2")
# m.load("C:/Users/arnfi/Desktop/rhinos/rhinoblacksouthcentral_child.mdl2")
# m.load("C:/Users/arnfi/Desktop/rhinos/rhinoblack_female.mdl2")
# m.load("C:/Users/arnfi/Desktop/rhinos/africanelephant_child.mdl2")
# m.load("C:/Users/arnfi/Desktop/rhinos/platypus.mdl2")
# m.load("C:/Users/arnfi/Desktop/rattle/western_diamondback_rattlesnake.mdl2")
# m.load("C:/Users/arnfi/Desktop/anteater/giant_anteater.mdl2")
# m.load("C:/Users/arnfi/Desktop/ele/africanelephant_female.mdl2")
# m.load("C:/Users/arnfi/Desktop/ostrich/ugcres.mdl2")
# m.load("C:/Users/arnfi/Desktop/ostrich/ugcres_hitcheck.mdl2")
# 	m.load("C:/Users/arnfi/Desktop/anubis/cc_anubis_carf.mdl2", entry=True, read_editable=True)
# 	for mesh in m.meshes:
# 		b = list(mesh.tris)
# m.load("C:/Users/arnfi/Desktop/anubis/cc_anubis_bogfl.mdl2")
# m.load("C:/Users/arnfi/Desktop/anubis/cc_anubis_carf_hitcheck.mdl2")
# m.load("C:/Users/arnfi/Desktop/gharial/gharial_male.mdl2")
# m = Mdl2File()
# # m.load("C:/Users/arnfi/Desktop/prim/meshes.ms2")
# print(m)
#
# idir = "C:/Users/arnfi/Desktop/out"
# # idir = "C:/Users/arnfi/Desktop/Coding/ovl/export_save/detailobjects"
# dic = {}
# name = "nat_grassdune_02.mdl2"
# name = "nat_groundcover_searocket_patchy_01.mdl2"
# indices = []
#
# for fp in walker.walk_type(idir, ".mdl2"):
# 	if "hitcheck" in fp or "skeleton" in fp or "airliftstraps" in fp:
# 		continue
# 	print(fp)
# 	m.load(fp, read_editable=True)
# 	# indices.append(m.index)
# 	print(fp)
# 	# print(list(lod.bone_index for lod in m.lods))
# 	# print(m.model_info)
# 	# lod_indices = list(lod.bone_index for lod in m.lods)
# 	flags = list(mo.flag for mo in m.meshes)
# 	print(flags)
# 	# indices.extend(unk)
# # 		dic[file] = lod_indices
# # 		if file.lower() == name:
# # 			print(m.ms2_file.bone_info)
# # 		# print(m.ms2_file.bone_info)
# # 		print(m.ms2_file.bone_info.name_indices, lod_indices)
# # 		lod_names = [m.ms2_file.bone_names[i-1] for i in lod_indices]
# # 		print(lod_names)
# # print(dic)
# # # print(m.ms2_file.buffer_0.names)
# # for i, n in enumerate(m.ms2_file.buffer_0.names):
# # 	print(i,n)
# # l = dic[name]
# # print(l)
# # print(indices, max(indices))
# # fp = os.path.join(idir, name)
# # m.load(fp, read_editable=True)
#
# print(set(indices))
