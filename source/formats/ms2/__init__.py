import os
import time
import traceback
import logging

from generated.formats.ms2.compound.Ms2InfoHeader import Ms2InfoHeader
from generated.formats.ms2.versions import *
from generated.formats.ovl_base.basic import ConvStream
from generated.formats.ovl.basic import basic_map
from generated.io import IoFile
from modules.formats.shared import djb2, get_padding

logging.basicConfig(level=logging.DEBUG)

BUFFER_NAMES = ("verts", "tris", "uvs", "tri_chunks", "vert_chunks")


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

			# logging.info(f"self.buffer_2_offset {self.buffer_2_offset}")
			# logging.info(self)
			# return
			# logging.debug(f"end of header: {self.buffer_1_offset}")

			logging.info(f"Vertex buffer starts at {self.buffer_2_offset}")
			try:
				for bone_info in self.models_reader.bone_infos:
					self.assign_bone_names(bone_info)
					self.assign_joints(bone_info)
			except:
				logging.exception(f"Joints or bones lookup failed")
			try:
				self.lookup_material()
			except:
				logging.exception(f"Material lookup failed")
			if read_bytes:
				stream.seek(self.buffer_0.io_start)
				self.buffer_0_bytes = stream.read(self.buffer_0.io_size)
				stream.seek(self.buffer_1_offset)
				self.buffer_1_bytes = stream.read(self.bone_info_size)
				self.buffer_2_bytes = stream.read()
			# attach the streams to each buffer_info
			for buffer_info, modelstream_name in zip(self.buffer_infos, self.modelstream_names):
				buffer_info.name = modelstream_name
				buffer_info.path = os.path.join(self.dir, buffer_info.name)
				logging.info(f"Loading {buffer_info.path}")
				with open(buffer_info.path, "rb") as modelstream_reader:
					self.attach_streams(buffer_info, modelstream_reader)
			# attach the static stream to last buffer_info
			# some older models do not have a static stream (eg. ZTUAC rhino)
			if self.buffer_infos and len(self.buffer_infos) != len(self.modelstream_names):
				static_buffer_info = self.buffer_infos[-1]
				stream.seek(self.buffer_2_offset)
				static_buffer_info.name = "STATIC"
				static_buffer_info.path = filepath
				self.attach_streams(static_buffer_info, stream)
			if read_editable:
				self.load_meshes()

		logging.debug(f"Read {self.name} in {time.time() - start_time:.2f} seconds")

	def attach_streams(self, buffer_info, in_stream=None):
		"""Attaches streams to a buffer info for each section, and fills them if an input stream is provided"""
		# logging.info(buffer_info)
		for buffer_name in BUFFER_NAMES:
			if in_stream:
				buff_size = getattr(buffer_info, f"{buffer_name}_size")
				# create a set to be able to guess the size of any entry
				setattr(buffer_info, f"{buffer_name}_offsets", {buff_size})
				logging.info(f"Loading {buffer_name} size {buff_size} at {in_stream.tell()}")
				b = in_stream.read(buff_size)
				with open(f"{buffer_info.path}_{buffer_name}.dmp", "wb") as f:
					f.write(b)
			else:
				b = b""
			setattr(buffer_info, buffer_name, ConvStream(b))

	def load_meshes(self):
		for mdl2_name, model_info in zip(self.mdl_2_names, self.model_infos):
			logging.debug(f"Loading mesh data for {mdl2_name}")
			for wrapper in model_info.model.meshes:
				wrapper.mesh.assign_buffer_info(self.buffer_infos)
				if hasattr(wrapper.mesh, "uv_offset"):
					wrapper.mesh.buffer_info.uvs_offsets.add(wrapper.mesh.uv_offset)
			if is_old(self.info):
				pack_base = 512
			else:
				pack_base = model_info.pack_base
			try:
				for i, wrapper in enumerate(model_info.model.meshes):
					logging.info(f"Populating mesh {i}")
					wrapper.mesh.populate(pack_base)
			except:
				logging.exception(f"Populating mesh failed")

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
				self.attach_streams(buffer_info)
			# now store each model
			for mdl2_name, model_info in zip(self.mdl_2_names, self.model_infos):
				logging.debug(f"Storing {mdl2_name}")
				# update ModelInfo
				model_info.num_materials = len(model_info.model.materials)
				model_info.num_lods = len(model_info.model.lods)
				model_info.num_objects = len(model_info.model.objects)
				model_info.num_meshes = len(model_info.model.meshes)
				# write each mesh's data blocks to the right temporary buffer
				for wrapper in model_info.model.meshes:
					wrapper.mesh.assign_buffer_info(self.buffer_infos)
					wrapper.mesh.write_data()
				# update LodInfo
				logging.debug(f"Updating lod vertex counts...")
				for lod in model_info.model.lods:
					lod.vertex_count = sum(wrapper.mesh.vertex_count for wrapper in lod.meshes)
					lod.tri_index_count = sum(wrapper.mesh.tri_index_count for wrapper in lod.meshes)
			# modify buffer size
			for buffer_info in self.buffer_infos:
				# get bytes from IO obj, pad, and update size in BufferInfo
				for buffer_name in BUFFER_NAMES:
					buff = getattr(buffer_info, buffer_name)
					buff_bytes = buff.getvalue()
					buff_bytes += get_padding(len(buff_bytes), alignment=16)
					setattr(buffer_info, f"{buffer_name}_bytes", buff_bytes)
					setattr(buffer_info, f"{buffer_name}_size", len(buff_bytes))
				
			# store static buffer
			if self.buffer_infos:
				buffer_info = self.buffer_infos[-1]
				self.buffer_2_bytes = b"".join((getattr(buffer_info, f"{b_name}_bytes") for b_name in BUFFER_NAMES))


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
			print("buffer_info.name", buffer_info.name)
			if buffer_info.name != "STATIC":
				buffer_info.path = os.path.join(self.dir, buffer_info.name)
				with open(buffer_info.path, "wb") as f:
					f.write(b"".join((getattr(buffer_info, f"{b_name}_bytes") for b_name in BUFFER_NAMES)))

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
	m.load("C:/Users/arnfi/Desktop/shop_mainstreet_.ms2", read_editable=True)
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
