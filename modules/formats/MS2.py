import os
import shutil
import struct
import logging

from generated.formats.ms2.compound.ModelInfo import ModelInfo
from generated.formats.ms2 import Ms2File, Ms2Context
from generated.formats.ms2.compound.Ms2SizedStrData import Ms2SizedStrData

import generated.formats.ovl.versions as ovl_versions

from modules.formats.shared import get_versions, get_padding
from modules.formats.BaseFormat import BaseFile
from modules.helpers import as_bytes
from ovl_util import interaction


class Ms2Loader(BaseFile):

	def get_version(self):
		ss_pointer = self.sized_str_entry.pointers[0]
		version = struct.unpack(f"I", ss_pointer.data[:4])[0]
		vdic = {"version": version}
		self.context = Ms2Context()
		self.context.version = version
		return vdic

	def collect(self):
		self.assign_ss_entry()
		self.get_version()
		ss_pointer = self.sized_str_entry.pointers[0]
		if not (ovl_versions.is_pc(self.ovl) or ovl_versions.is_ztuac(self.ovl)):
			self.sized_str_entry.fragments = self.ovs.frags_from_pointer(ss_pointer, 3)
			# second pass: collect mesh fragments
			if ss_pointer.data_size != 48:
				logging.warning(f"Unexpected SS ptr size ({ss_pointer.data_size}) for {self.file_entry.name}")
			if self.sized_str_entry.fragments[2].pointers[1].data not in (struct.pack("<ii", -1, 0), b""):
				logging.warning(
					f"Unexpected frag 2 ptr data ({self.sized_str_entry.fragments[2].pointers[1].data}) for {self.file_entry.name}")

			# assign the mdl2 frags to their sized str entry

			# 3 fixed fragments laid out like
			# 48 bytes in total
			# sse p0: ms2_general_info_data (24 bytes) + 24 bytes for 3 pointers
			# 0 - p0: 8*00 				p1: buffer_info or empty (if no buffers)
			# 1 - p0: 8*00 				p1: core_model_info for first mdl2 file
			# 2 - p0: 8*00 				p1: 2 unk uints: -1, 0 or empty (if no buffers)
			f_1 = self.sized_str_entry.fragments[1]
			model_infos = f_1.pointers[1].load_as(ModelInfo, context=self.context, num=len(self.sized_str_entry.children))
			for mdl2_entry, mdl2_info in zip(self.sized_str_entry.children, model_infos):
				assert mdl2_entry.ext == ".mdl2"
				self.collect_mdl2(mdl2_entry, mdl2_info, f_1.pointers[1])
		else:
			self.sized_str_entry.fragments = self.ovs.frags_from_pointer(ss_pointer, 1)

	def collect_mdl2(self, mdl2_entry, mdl2_info, mdl2_pointer):
		logging.info(f"MDL2: {mdl2_entry.name}")
		mdl2_entry.fragments = self.ovs.frags_from_pointer(mdl2_pointer, 5)
		# these 5 fixed fragments are laid out like
		# 0 - p0: 8*00 				p1: materials
		# 1 - p0: 8*00 				p1: lods
		# 2 - p0: 8*00 				p1: objects
		# 3 - p0: 8*00 				p1: -> first MeshData, start of MeshData fragments block
		# 4 - p0: next_model_info	p1: -> materials of the first mdl2
		#         or just 40 bytes
		# plus fragments counted by num_meshes
		# i - p0: MeshData (64b)	p1: -> buffer_info
		materials, lods, objects, meshes, model_info = mdl2_entry.fragments
		# remove padding
		objects_ptr = objects.pointers[1]
		objects_ptr.split_data_padding(4 * mdl2_info.num_objects)
		logging.debug(f"Objects data {objects_ptr.data_size}, padding {objects_ptr.padding_size}")
		logging.debug(f"Sum {objects_ptr.data_size + objects_ptr.padding_size}")
		logging.debug(f"rel offset {meshes.pointers[1].data_offset-materials.pointers[1].data_offset}")
		logging.debug(f"rel mod 8 {(meshes.pointers[1].data_offset-materials.pointers[1].data_offset) % 8}")
		# get and set fragments
		logging.debug(f"Num model data frags = {mdl2_info.num_meshes}")
		mdl2_entry.model_data_frags = self.ovs.frags_from_pointer(
			meshes.pointers[1], mdl2_info.num_meshes)
		# just assign name for those here
		for f in mdl2_entry.model_data_frags:
			f.name = mdl2_entry.name

	def create(self):
		ms2_file = Ms2File()
		ms2_file.load(self.file_entry.path, read_bytes=True)
		ms2_dir = os.path.dirname(self.file_entry.path)

		ms2_entry = self.create_ss_entry(self.file_entry)
		ms2_entry.children = []

		versions = get_versions(self.ovl)

		# 1 for the ms2, 2 for each mdl2
		# pool.num_files += 1
		# create sized str entries and mesh data fragments
		for model_info, mdl2_name in zip(ms2_file.model_infos, ms2_file.mdl_2_names):
			# pool.num_files += 2
			mdl2_path = os.path.join(ms2_dir, mdl2_name)
			mdl2_file_entry = self.get_file_entry(mdl2_path)

			mdl2_entry = self.create_ss_entry(mdl2_file_entry)
			mdl2_entry.pointers[0].pool_index = -1
			ms2_entry.children.append(mdl2_entry)

			# first, create all MeshData structs as fragments
			mdl2_entry.model_data_frags = [self.create_fragment() for _ in range(model_info.num_meshes)]

		first_materials_ptr = None
		# create the 5 fixed frags per MDL2 and write their data
		for model_info, mdl2_entry in zip(ms2_file.model_infos, ms2_entry.children):
			mdl2_entry.fragments = [self.create_fragment() for _ in range(5)]
			materials, lods, objects, meshes, model_info_ptr = mdl2_entry.fragments

			if first_materials_ptr is None:
				first_materials_ptr = materials.pointers[1]

			self.write_to_pool(materials.pointers[1], 2, as_bytes(model_info.model.materials, version_info=versions))
			self.write_to_pool(lods.pointers[1], 2, as_bytes(model_info.model.lods, version_info=versions))
			objects_bytes = as_bytes(model_info.model.objects, version_info=versions)
			# todo - padding like this is likely wrong, probably relative to start of materials
			self.write_to_pool(objects.pointers[1], 2, objects_bytes + get_padding(len(objects_bytes), alignment=8))
			self.write_to_pool(meshes.pointers[1], 2, as_bytes(model_info.model.meshes, version_info=versions))

			self.ptr_relative(model_info_ptr.pointers[1], first_materials_ptr)
			# point to start of each modeldata
			offset = 0
			for frag in mdl2_entry.model_data_frags:
				self.ptr_relative(frag.pointers[0], meshes.pointers[1], rel_offset=offset)
				offset += 64
		# create fragments for ms2
		buffer_info_frag, model_info_frag, end_frag = self.create_fragments(ms2_entry, 3)

		# write mesh info
		self.write_to_pool(model_info_frag.pointers[1], 2, as_bytes(ms2_file.model_infos, version_info=versions))
		offset = 0
		for mdl2_entry in ms2_entry.children:
			# byte size of modelinfo varies - JWE1 (176 bytes total)
			if ovl_versions.is_jwe(self.ovl):
				offset += 104
			# 16 additional bytes for PZ/PZ16/JWE2 (192 bytes total)
			else:
				offset += 120
			for frag in mdl2_entry.fragments:
				self.ptr_relative(frag.pointers[0], model_info_frag.pointers[1], rel_offset=offset)
				offset += 8
			offset += 32
		# buffer info data
		buffer_info_bytes = as_bytes(ms2_file.buffer_info, version_info=versions)
		self.write_to_pool(buffer_info_frag.pointers[1], 2, buffer_info_bytes)
		# set ptr to buffer info for each MeshData frag
		for mdl2_entry in ms2_entry.children:
			for frag in mdl2_entry.model_data_frags:
				self.ptr_relative(frag.pointers[1], buffer_info_frag.pointers[1])

		# ms2 ss data
		ms2_ss_bytes = as_bytes(ms2_file.info, version_info=versions)
		self.write_to_pool(ms2_entry.pointers[0], 2, ms2_ss_bytes)
		# set frag ptr 0
		for frag, offset in zip(ms2_entry.fragments, (24, 32, 40)):
			self.ptr_relative(frag.pointers[0], ms2_entry.pointers[0], rel_offset=offset)

		# the last ms2 fragment
		self.write_to_pool(end_frag.pointers[1], 2, struct.pack("<ii", -1, 0))
		# create ms2 data
		self.create_data_entry(ms2_entry, ms2_file.buffers)

	def update(self):
		if ovl_versions.is_pz16(self.ovl):
			logging.info(f"Updating MS2 buffer 0 with padding for {self.sized_str_entry.name}")
			name_buffer, bone_infos, verts = self.get_ms2_buffer_datas()
			# make sure buffer 0 is padded to 4 bytes
			padding = get_padding(len(name_buffer), 4)
			if padding:
				self.sized_str_entry.data_entry.update_data([name_buffer + padding, bone_infos, verts])
	
	def extract(self, out_dir, show_temp_files, progress_callback):
		self.get_version()
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")
		name_buffer, bone_infos, verts = self.get_ms2_buffer_datas()
		# truncate to 48 bytes for PZ af_keeperbodyparts
		ms2_general_info_data = self.sized_str_entry.pointers[0].data[:48]
		# ms2_info = self.sized_str_entry.pointers[0].load_as(Ms2SizedStrData, context=self.context)[0]

		ms2_header = struct.pack("<I", len(bone_infos))
	
		# for i, buffer in enumerate(buffers):
		# 	p = out_dir(name+str(i)+".ms2")
		# 	with open(p, 'wb') as outfile:
		# 		outfile.write(buffer)
	
		# Planet coaster
		if ovl_versions.is_pc(self.ovl) or ovl_versions.is_ztuac(self.ovl):
			# only ss entry holds any useful stuff
			ms2_buffer_info_data = b""
		# Planet Zoo, JWE
		else:
			if len(self.sized_str_entry.fragments) != 3:
				raise AttributeError(f"{name} must have 3 fragments")

			buffer_info_frag, model_info_frag, end_frag = self.sized_str_entry.fragments
			# information on vert & tri buffer sizes
			ms2_buffer_info_data = buffer_info_frag.pointers[1].data
			# this fragment informs us about the mesh count of the next mdl2 that is read
			# so we can use it to collect the variable mdl2 fragments describing a mesh each
			model_infos = model_info_frag.pointers[1].load_as(ModelInfo, context=self.context, num=len(self.sized_str_entry.children))
		# write the ms2 file
		out_path = out_dir(name)
		with open(out_path, 'wb') as outfile:
			outfile.write(ms2_header)
			outfile.write(ms2_general_info_data)
			for mdl2_entry in self.sized_str_entry.children:
				logging.debug(f"Writing {mdl2_entry.name}")
				outfile.write(as_bytes(mdl2_entry.basename))
			outfile.write(name_buffer)
			# this corresponds to pc buffer 1 already
			outfile.write(ms2_buffer_info_data)
			# export each mdl2
			if not (ovl_versions.is_pc(self.ovl) or ovl_versions.is_ztuac(self.ovl)):
				outfile.write(model_info_frag.pointers[1].data)
				for mdl2_info, mdl2_entry in zip(model_infos, self.sized_str_entry.children):
					materials, lods, objects, meshes, model_info = mdl2_entry.fragments

					# avoid writing bad fragments that should be empty
					if mdl2_info.num_objects:
						for f in (materials, lods, objects, meshes):
							outfile.write(f.pointers[1].data)
			outfile.write(bone_infos)
			outfile.write(verts)

		# m = Ms2File()
		# m.load(out_path, read_editable=True)
		# m.save(out_path+"_.ms2")
		# print(m)
		return out_path,
	
	def get_ms2_buffer_datas(self):
		assert self.sized_str_entry.data_entry
		buffers_in_order = list(sorted(self.get_streams(), key=lambda b: b.index))
		for buff in buffers_in_order:
			logging.debug(f"buffer {buff.index}, size {buff.size} bytes")
		all_buffer_bytes = [buffer.data for buffer in buffers_in_order]
		name_buffer = all_buffer_bytes[0]
		bone_infos = all_buffer_bytes[1]
		verts = b"".join(all_buffer_bytes[2:])
		for i, vbuff in enumerate(all_buffer_bytes[2:]):
			logging.debug(f"Vertex buffer {i}, size {len(vbuff)} bytes")
		logging.debug(f"len buffers: {len(all_buffer_bytes)}")
		logging.debug(f"name_buffer: {len(name_buffer)}, bone_infos: {len(bone_infos)}, verts: {len(verts)}")
		return name_buffer, bone_infos, verts
	
	def load(self, ms2_file_path):
		logging.info(f"Injecting MS2")
		versions = get_versions(self.ovl)

		ms2_file = Ms2File()
		ms2_file.load(ms2_file_path, read_bytes=True)

		missing_materials = set()
		for model_info, mdl2_name, mdl2_entry in zip(ms2_file.model_infos, ms2_file.mdl_2_names, self.sized_str_entry.children):
			for material in model_info.model.materials:
				fgm_name = f"{material.name.lower()}.fgm"
				if ovl_versions.is_jwe(self.ovl) or ovl_versions.is_jwe2(self.ovl) and fgm_name == "airliftstraps.fgm":
					# don't cry about this
					continue
				if fgm_name not in self.ovl._ss_dict:
					missing_materials.add(fgm_name)
			if len(mdl2_entry.model_data_frags) != len(model_info.model.meshes):
				raise AttributeError(
					f"{mdl2_entry.name} ({len(model_info.model.meshes)}) doesn't have the "
					f"expected amount ({len(mdl2_entry.model_data_frags)}) of meshes!")
		if missing_materials:
			mats = '\n'.join(missing_materials)
			msg = f"The following materials are used by {self.file_entry.name}, but are missing from the OVL:\n" \
				f"{mats}\n" \
				f"This will crash unless you are importing the materials from another OVL. Inject anyway?"
			if not interaction.showdialog(msg, ask=True):
				logging.info("Injection was canceled by the user")
				return

		for mdl2_entry, model_info in zip(self.sized_str_entry.children, ms2_file.model_infos):
			logging.debug(f"Injecting {mdl2_entry.name} ")
	
			materials, lods, objects, meshes, model_info_ptr = mdl2_entry.fragments
			for frag, mdl2_list in (
					(materials, model_info.model.materials,),
					(lods, model_info.model.lods),
					(objects, model_info.model.objects),
					(meshes, model_info.model.meshes)):
				if len(mdl2_list) > 0:
					data = as_bytes(mdl2_list, version_info=versions)
					# objects.pointers[1] has padding in stock, apparently as each entry is 4 bytes
					logging.debug(f"Injecting mdl2 data {len(data)} into {len(frag.pointers[1].data)} ({len(frag.pointers[1].padding)})")
					# frag.pointers[1].update_data(data, pad_to=8)
					# the above breaks injecting minmi
					frag.pointers[1].update_data(data)
					logging.debug(f"Result {len(frag.pointers[1].data)} ({len(frag.pointers[1].padding)})")

		# load ms2 ss data
		self.sized_str_entry.pointers[0].update_data(as_bytes(ms2_file.info, version_info=versions))
	
		buffer_info_frag, model_info_frag, end_frag = self.sized_str_entry.fragments
		buffer_info_frag.pointers[1].update_data(as_bytes(ms2_file.buffer_info, version_info=versions), update_copies=True)
		model_info_frag.pointers[1].update_data(as_bytes(ms2_file.model_infos, version_info=versions))
	
		# update ms2 data
		self.sized_str_entry.data_entry.update_data(ms2_file.buffers)

	def rename_content(self, name_tuples):
		temp_dir, out_dir_func = self.get_tmp_dir()
		try:
			ms2_path = self.extract(out_dir_func, False, None)[0]
			# open the ms2 file
			ms2_file = Ms2File()
			ms2_file.load(ms2_path, read_bytes=True)
			# rename the materials
			ms2_file.rename(name_tuples)
			# update the hashes & save
			ms2_file.save(ms2_path)
			# inject again
			self.load(ms2_path)
		except BaseException as err:
			logging.warning(err)
		# delete temp dir again
		shutil.rmtree(temp_dir)
