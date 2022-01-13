import os
import shutil
import struct
import logging

from generated.formats.ms2.compound.ModelInfo import ModelInfo
from generated.formats.ms2 import Mdl2File, Ms2File, Ms2Context
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
		materials, lods, objects, models, model_info = mdl2_entry.fragments
		# remove padding
		objects.pointers[1].split_data_padding(4 * mdl2_info.num_objects)
		# get and set fragments
		logging.debug(f"Num model data frags = {mdl2_info.num_meshes}")
		mdl2_entry.model_data_frags = self.ovs.frags_from_pointer(
			models.pointers[1], mdl2_info.num_meshes)
		# just assign name for those here
		for f in mdl2_entry.model_data_frags:
			f.name = mdl2_entry.name

	def create(self):
		ms2_file = Ms2File()
		ms2_file.load(self.file_entry.path, read_bytes=True)

		ms2_entry = self.create_ss_entry(self.file_entry)
		ms2_entry.children = []

		versions = get_versions(self.ovl)

		ms2_dir, ms2_basename = os.path.split(self.file_entry.path)
		mdl2_names = [f for f in os.listdir(ms2_dir) if f.lower().endswith(".mdl2")]
		mdl2s = []
		for mdl2_name in mdl2_names:
			mdl2_path = os.path.join(ms2_dir, mdl2_name)
			mdl2 = Mdl2File()
			mdl2.load(mdl2_path)
			if mdl2.ms_2_name.lower() == ms2_basename:
				mdl2s.append(mdl2)
		# sort them by mesh index
		mdl2s.sort(key=lambda m: m.index)

		# 1 for the ms2, 2 for each mdl2
		# pool.num_files += 1
		# create sized str entries and mesh data fragments
		for mdl2 in mdl2s:
			# pool.num_files += 2
			mdl2_path = os.path.join(ms2_dir, mdl2.basename)
			mdl2_file_entry = self.get_file_entry(mdl2_path)

			mdl2_entry = self.create_ss_entry(mdl2_file_entry)
			mdl2_entry.pointers[0].pool_index = -1
			ms2_entry.children.append(mdl2_entry)

			# first, create all MeshData structs as fragments
			mdl2_entry.model_data_frags = [self.create_fragment() for _ in range(mdl2.model_info.num_meshes)]

		first_materials_ptr = None
		# create the 5 fixed frags per MDL2 and write their data
		for mdl2, mdl2_entry in zip(mdl2s, ms2_entry.children):
			mdl2_entry.fragments = [self.create_fragment() for _ in range(5)]
			materials, lods, objects, models, model_info = mdl2_entry.fragments

			if first_materials_ptr is None:
				first_materials_ptr = materials.pointers[1]

			self.write_to_pool(materials.pointers[1], 2, as_bytes(mdl2.materials, version_info=versions))
			self.write_to_pool(lods.pointers[1], 2, as_bytes(mdl2.lods, version_info=versions))
			objects_bytes = as_bytes(mdl2.objects, version_info=versions)
			self.write_to_pool(objects.pointers[1], 2, objects_bytes + get_padding(len(objects_bytes), alignment=8))
			self.write_to_pool(models.pointers[1], 2, as_bytes(mdl2.models, version_info=versions))

			self.ptr_relative(model_info.pointers[1], first_materials_ptr)
			# point to start of each modeldata
			offset = 0
			for frag in mdl2_entry.model_data_frags:
				self.ptr_relative(frag.pointers[0], models.pointers[1], rel_offset=offset)
				offset += 64
		# create fragments for ms2
		buffer_info_frag, model_info_frag, end_frag = self.create_fragments(ms2_entry, 3)

		# write mesh info
		self.write_to_pool(model_info_frag.pointers[1], 2, self.get_model_info_bytes(mdl2s, versions))
		offset = 0
		for mdl2, mdl2_entry in zip(mdl2s, ms2_entry.children):
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
		ms2_ss_bytes = as_bytes(ms2_file.general_info, version_info=versions)
		self.write_to_pool(ms2_entry.pointers[0], 2, ms2_ss_bytes)
		# set frag ptr 0
		for frag, offset in zip(ms2_entry.fragments, (24, 32, 40)):
			self.ptr_relative(frag.pointers[0], ms2_entry.pointers[0], rel_offset=offset)

		# the last ms2 fragment
		self.write_to_pool(end_frag.pointers[1], 2, struct.pack("<ii", -1, 0))
		# create ms2 data
		self.create_data_entry(ms2_entry, (ms2_file.buffer_0_bytes, ms2_file.buffer_1_bytes, ms2_file.buffer_2_bytes))

	def update(self):
		if ovl_versions.is_pz16(self.ovl):
			logging.info(f"Updating MS2 buffer 0 with padding for {self.sized_str_entry.name}")
			name_buffer, bone_infos, verts = self.get_ms2_buffer_datas()
			# make sure buffer 0 is padded to 4 bytes
			padding = get_padding(len(name_buffer), 4)
			if padding:
				self.sized_str_entry.data_entry.update_data([name_buffer + padding, bone_infos, verts])
	
	def extract(self, out_dir, show_temp_files, progress_callback):
		versions = self.get_version()
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")
		name_buffer, bone_infos, verts = self.get_ms2_buffer_datas()
		# sizedstr data has bone count
		ms2_general_info_data = self.sized_str_entry.pointers[0].data
		ms2_info = self.sized_str_entry.pointers[0].load_as(Ms2SizedStrData, context=self.context)[0]

		ms2_header = struct.pack("<2I", len(name_buffer), len(bone_infos))
	
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
		out_paths = [out_path, ]
		with open(out_path, 'wb') as outfile:
			# outfile.write(ovl_header)
			outfile.write(ms2_header)
			outfile.write(ms2_general_info_data)
			outfile.write(ms2_buffer_info_data)
			outfile.write(name_buffer)
			outfile.write(bone_infos)
			outfile.write(verts)

		bone_info_index = 0
		# export each mdl2
		for mdl2_index, mdl2_entry in enumerate(self.sized_str_entry.children):
			mdl2_path = out_dir(mdl2_entry.name)
			out_paths.append(mdl2_path)
			with open(mdl2_path, 'wb') as outfile:
				logging.info(f"Writing {mdl2_entry.name} [{mdl2_index}]")
	
				mdl2_header = struct.pack("<3I", ms2_info.version, mdl2_index, bone_info_index)
				# outfile.write(ovl_header)
				outfile.write(mdl2_header)
				outfile.write(as_bytes(self.sized_str_entry.name))
	
				if not (ovl_versions.is_pc(self.ovl) or ovl_versions.is_ztuac(self.ovl)):
					# the fixed fragments
					materials, lods, objects, models, model_info = mdl2_entry.fragments
					# write the mesh info for this mesh, buffered from the previous mesh or ms2 (model_info fragments)
					mdl2_info = model_infos[mdl2_index]
					outfile.write(as_bytes(mdl2_info, versions))
					bone_info_index += mdl2_info.increment_flag

					# avoid writing bad fragments that should be empty
					if mdl2_info.num_objects:
						for f in (materials, lods, objects, models):
							outfile.write(f.pointers[1].data)
		return out_paths
	
	def get_ms2_buffer_datas(self):
		assert self.sized_str_entry.data_entry
		all_buffer_bytes = [buffer.data for buffer in self.get_streams()]
		name_buffer = all_buffer_bytes[0]
		bone_infos = all_buffer_bytes[1]
		verts = b"".join(all_buffer_bytes[2:])
		for i, vbuff in enumerate(all_buffer_bytes[2:]):
			logging.debug(f"Vertex buffer {i}, size {len(vbuff)} bytes")
		logging.debug(f"len buffers: {len(all_buffer_bytes)}")
		logging.debug(f"name_buffer: {len(name_buffer)}, bone_infos: {len(bone_infos)}, verts: {len(verts)}")
		return name_buffer, bone_infos, verts
	
	def load(self, ms2_file_path):
		versions = get_versions(self.ovl)
	
		ms2_dir = os.path.dirname(ms2_file_path)
		mdl2s = []
		# load and check if everything is valid
		for mdl2_entry in self.sized_str_entry.children:
			mdl2_path = os.path.join(ms2_dir, mdl2_entry.name)
			mdl2 = Mdl2File()
			# todo - entry is costly, but needed for the mapping of materials - refactor to use entry just once
			mdl2.load(mdl2_path, entry=True)
			mdl2s.append(mdl2)
	
			missing_materials = []
			for material in mdl2.materials:
				fgm_name = f"{material.name.lower()}.fgm"
				if fgm_name not in self.ovl._ss_dict:
					missing_materials.append(fgm_name)
			if missing_materials:
				mats = '\n'.join(missing_materials)
				msg = f"The following materials are used by {mdl2_entry.name}, but are missing from the OVL:\n" \
					f"{mats}\n" \
					f"This will crash unless you are importing the materials from another OVL. Inject anyway?"
				if not interaction.showdialog(msg, ask=True):
					logging.info("Injection was canceled by the user")
					return
			if len(mdl2_entry.model_data_frags) != len(mdl2.models):
				raise AttributeError(f"{mdl2_entry.name} doesn't have the right amount of meshes!")
	
		logging.info(f"Injecting MDL2s")
		# actual injection starts here
		for mdl2_entry, mdl2 in zip(self.sized_str_entry.children, mdl2s):
			logging.debug(f"Injecting mdl2 {mdl2.basename} ")
	
			materials, lods, objects, models, model_info = mdl2_entry.fragments
			for frag, mdl2_list in (
					(materials, mdl2.materials,),
					(lods, mdl2.lods),
					(objects, mdl2.objects),
					(models, mdl2.models)):
				if len(mdl2_list) > 0:
					data = as_bytes(mdl2_list, version_info=versions)
					# objects.pointers[1] has padding in stock, apparently as each entry is 4 bytes
					logging.debug(f"Injecting mdl2 data {len(data)} into {len(frag.pointers[1].data)} ({len(frag.pointers[1].padding)})")
					# frag.pointers[1].update_data(data, pad_to=8)
					# the above breaks injecting minmi
					frag.pointers[1].update_data(data)
					logging.debug(f"Result {len(frag.pointers[1].data)} ({len(frag.pointers[1].padding)})")

		logging.info(f"Injecting MS2")
		ms2_file = Ms2File()
		ms2_file.load(ms2_file_path, read_bytes=True)
		# load ms2 ss data
		self.sized_str_entry.pointers[0].update_data(as_bytes(ms2_file.general_info, version_info=versions))
	
		buffer_info_frag, model_info_frag, end_frag = self.sized_str_entry.fragments
		buffer_info_frag.pointers[1].update_data(as_bytes(ms2_file.buffer_info, version_info=versions), update_copies=True)
		model_info_frag.pointers[1].update_data(self.get_model_info_bytes(mdl2s, versions))
	
		# update ms2 data
		self.sized_str_entry.data_entry.update_data([ms2_file.buffer_0_bytes, ms2_file.buffer_1_bytes, ms2_file.buffer_2_bytes])

	def get_model_info_bytes(self, mdl2s, versions):
		all_model_infos = []
		for mdl2 in mdl2s:
			data = as_bytes(mdl2.model_info, version_info=versions)
			all_model_infos.append(data)
		model_infos_bytes = b"".join(all_model_infos)
		return model_infos_bytes

	def rename_content(self, name_tuples):
		temp_dir, out_dir_func = self.get_tmp_dir()
		try:
			ms2_mdl2_files = self.extract(out_dir_func, False, None)
			# there is always just one ms2 in one entry's files
			ms2_path = [f for f in ms2_mdl2_files if f.endswith(".ms2")][0]

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
