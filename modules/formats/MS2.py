import os
import struct
import logging

from generated.formats.ms2.compound.CoreModelInfo import CoreModelInfo
from generated.formats.ms2.compound.Mdl2ModelInfo import Mdl2ModelInfo
from generated.formats.ms2 import Mdl2File, Ms2File, is_old

from generated.formats.ovl.versions import *

from modules.formats.shared import get_versions, get_padding
from modules.formats.BaseFormat import BaseFile
from modules.helpers import write_sized_str, as_bytes
from ovl_util import interaction


class Ms2Loader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		ss_pointer = self.sized_str_entry.pointers[0]
		if not is_old(self.ovl):
			self.sized_str_entry.fragments = self.ovs.frags_from_pointer(ss_pointer, 3)
			# print(self.sized_str_entry.fragments)
			# second pass: collect model fragments
			versions = get_versions(self.ovl)
			if ss_pointer.data_size != 24:
				logging.warning(f"Unexpected SS ptr size ({ss_pointer.data_size}) for {self.file_entry.name}")
			if self.sized_str_entry.fragments[2].pointers[1].data not in (struct.pack("<ii", -1, 0), b""):
				logging.warning(
					f"Unexpected frag 2 ptr data ({self.sized_str_entry.fragments[2].pointers[1].data}) for {self.file_entry.name}")
			# print(self.sized_str_entry.fragments[2].pointers[1].address, self.sized_str_entry.fragments[2].pointers[1].data)

			# assign the mdl2 frags to their sized str entry

			# 3 fixed fragments laid out like
			# sse p0: ms2_general_info_data (24 bytes)
			# 0 - p0: 8*00 				p1: buffer_info or empty (if no buffers)
			# 1 - p0: 8*00 				p1: core_model_info for first mdl2 file
			# 2 - p0: 8*00 				p1: 2 unk uints: -1, 0 or empty (if no buffers)
			f_1 = self.sized_str_entry.fragments[1]
			core_model_info = f_1.pointers[1].load_as(CoreModelInfo, version_info=versions)[0]
			# print("next model info:", core_model_info)
			for mdl2_entry in self.sized_str_entry.children:
				assert mdl2_entry.ext == ".mdl2"
				self.collect_mdl2(mdl2_entry, core_model_info, f_1.pointers[1])
				pink = mdl2_entry.fragments[4]
				if self.size_check(pink):
					core_model_info = pink.pointers[0].load_as(Mdl2ModelInfo, version_info=versions)[0].info

		else:
			self.sized_str_entry.fragments = self.ovs.frags_from_pointer(ss_pointer, 1)

	def collect_mdl2(self, mdl2_entry, core_model_info, mdl2_pointer):
		logging.info(f"MDL2: {mdl2_entry.name}")
		mdl2_entry.fragments = self.ovs.frags_from_pointer(mdl2_pointer, 5)
		# these 5 fixed fragments are laid out like
		# 0 - p0: 8*00 				p1: materials
		# 1 - p0: 8*00 				p1: lods
		# 2 - p0: 8*00 				p1: objects
		# 3 - p0: 8*00 				p1: -> first ModelData, start of ModelData fragments block
		# 4 - p0: next_model_info	p1: -> materials of the first mdl2
		#         or just 40 bytes
		# plus fragments counted by num_models
		# i - p0: ModelData (64b)	p1: -> buffer_info
		materials, lods, objects, model_data_ptr, model_info = mdl2_entry.fragments
		# remove padding
		objects.pointers[1].split_data_padding(4 * core_model_info.num_objects)
		# store for export
		mdl2_entry.num_models = core_model_info.num_objects
		# get and set fragments
		logging.debug(f"Num model data frags = {core_model_info.num_models}")
		mdl2_entry.model_data_frags = self.ovs.frags_from_pointer(
			model_data_ptr.pointers[1], core_model_info.num_models)
		# just assign name for those here
		for f in mdl2_entry.model_data_frags:
			f.name = mdl2_entry.name

	def create(self):
		ms2_file = Ms2File()
		ms2_file.load(self.file_entry.path, read_bytes=True)

		ms2_entry = self.create_ss_entry(self.file_entry)
		ms2_entry.children = []

		versions = get_versions(self.ovl)

		pool_index, pool = self.get_pool(2)
		offset = pool.data.tell()

		ms2_dir, ms2_basename = os.path.split(self.file_entry.path)
		mdl2_names = [f for f in os.listdir(ms2_dir) if f.lower().endswith(".mdl2")]
		mdl2s = []
		for mdl2_name in mdl2_names:
			mdl2_path = os.path.join(ms2_dir, mdl2_name)
			mdl2 = Mdl2File()
			mdl2.load(mdl2_path)
			if mdl2.ms_2_name == ms2_basename:
				mdl2s.append((mdl2_name, mdl2))
		# sort them by model index
		mdl2s.sort(key=lambda tup: tup[1].index)

		# 1 for the ms2, 2 for each mdl2
		pool.num_files += 1
		# create sized str entries and model data fragments
		for mdl2_name, mdl2 in mdl2s:
			pool.num_files += 2
			mdl2_file_entry = self.get_file_entry(mdl2_name)
			mdl2_entry = self.create_ss_entry(mdl2_file_entry)
			mdl2_entry.pointers[0].pool_index = -1
			mdl2_entry.pointers[0].data_offset = 0
			ms2_entry.children.append(mdl2_entry)

			# first, create all ModelData structs as fragments
			mdl2_entry.model_data_frags = [self.create_fragment() for _ in range(mdl2.model_info.num_models)]

		first_materials_offset = None
		# create the 5 fixed frags per MDL2 and write their data
		for (mdl2_name, mdl2), mdl2_entry in zip(mdl2s, ms2_entry.children):
			mdl2_entry.fragments = [self.create_fragment() for _ in range(5)]
			materials, lods, objects, model_data_ptr, model_info = mdl2_entry.fragments

			materials_offset = pool.data.tell()
			if first_materials_offset is None:
				first_materials_offset = materials_offset
			materials.pointers[1].pool_index = pool_index
			materials.pointers[1].data_offset = materials_offset
			pool.data.write(as_bytes(mdl2.materials, version_info=versions))

			lods.pointers[1].pool_index = pool_index
			lods.pointers[1].data_offset = pool.data.tell()
			pool.data.write(as_bytes(mdl2.lods, version_info=versions))

			objects.pointers[1].pool_index = pool_index
			objects.pointers[1].data_offset = pool.data.tell()
			objects_bytes = as_bytes(mdl2.objects, version_info=versions)
			pool.data.write(objects_bytes + get_padding(len(objects_bytes), alignment=8))

			# modeldatas start here

			model_info.pointers[1].pool_index = pool_index
			model_info.pointers[1].data_offset = first_materials_offset

			model_data_ptr.pointers[1].pool_index = pool_index
			model_data_ptr.pointers[1].data_offset = pool.data.tell()
			# write mdl2 modeldata frags
			for frag, modeldata in zip(mdl2_entry.model_data_frags, mdl2.models):
				frag.pointers[0].pool_index = pool_index
				frag.pointers[0].data_offset = pool.data.tell()
				pool.data.write(as_bytes(modeldata, version_info=versions))

		# create fragments for ms2
		ms2_entry.fragments = [self.create_fragment() for _ in range(3)]

		# write model info
		for mdl2_name, mdl2 in mdl2s:
			model_info_bytes = as_bytes(mdl2.model_info, version_info=versions)
			if mdl2.index == 0:
				f_0, f_1, f_2 = ms2_entry.fragments
				f_1.pointers[1].pool_index = pool_index
				f_1.pointers[1].data_offset = pool.data.tell()
				# only write core model info
				pool.data.write(model_info_bytes)

			else:
				# grab the preceding mdl2 entry since it points ahead
				prev_mdl2_entry = ms2_entry.children[mdl2.index - 1]
				# get its model info fragment
				materials, lods, objects, model_data_ptr, model_info = prev_mdl2_entry.fragments
				model_info.pointers[0].pool_index = pool_index
				model_info.pointers[0].data_offset = pool.data.tell()
				# we write this anyway
				# todo - get the actual data
				core_model_data = struct.pack("<5Q", 0, 1, 0, 0, 0)
				pool.data.write(core_model_data)
				# we should only
				pool.data.write(model_info_bytes)

			this_mdl2_entry = ms2_entry.children[mdl2.index]
			materials, lods, objects, model_data_ptr, model_info = this_mdl2_entry.fragments
			for frag in (materials, lods, objects, model_data_ptr):
				frag.pointers[0].pool_index = pool_index
				frag.pointers[0].data_offset = pool.data.tell()
				pool.data.write(b"\x00" * 8)
		# write last 40 bytes to model_info
		if mdl2s:
			model_info.pointers[0].pool_index = pool_index
			model_info.pointers[0].data_offset = pool.data.tell()
			# todo - get the actual data
			core_model_data = struct.pack("<5Q", 0, 1, 0, 0, 0)
			pool.data.write(core_model_data)

		# write the ms2 itself
		# buffer info data
		buffer_info_frag, model_info_frag, end_frag = ms2_entry.fragments
		buffer_info_offset = pool.data.tell()
		# set ptr to buffer info for each ModelData frag
		for mdl2_entry in ms2_entry.children:
			for frag in mdl2_entry.model_data_frags:
				frag.pointers[1].pool_index = pool_index
				frag.pointers[1].data_offset = buffer_info_offset
		# todo - from the frag log, buffer_info_bytes should be 48 bytes but is 32
		buffer_info_frag.pointers[1].data_offset = buffer_info_offset
		buffer_info_bytes = as_bytes(ms2_file.buffer_info, version_info=versions)
		logging.debug(f"len(buffer_info_bytes) {len(buffer_info_bytes)}")
		pool.data.write(buffer_info_bytes)

		# ss data
		ms2_entry.pointers[0].pool_index = pool_index
		ms2_entry.pointers[0].data_offset = pool.data.tell()
		# load ms2 ss data
		ms2_ss_bytes = as_bytes(ms2_file.general_info, version_info=versions)  # + ms2_entry.pointers[0].data[24:]
		pool.data.write(ms2_ss_bytes)

		# first, 3 * 8 bytes of 00
		for frag in ms2_entry.fragments:
			frag.pointers[0].pool_index = pool_index
			frag.pointers[1].pool_index = pool_index
			frag.pointers[0].data_offset = pool.data.tell()
			pool.data.write(b"\x00" * 8)

		# the last ms2 fragment
		end_frag.pointers[1].data_offset = pool.data.tell()
		pool.data.write(struct.pack("<ii", -1, 0))
		# create ms2 data
		self.create_data_entry(ms2_entry, (ms2_file.buffer_0_bytes, ms2_file.buffer_1_bytes, ms2_file.buffer_2_bytes))

	def update(self):
		if is_pz16(self.ovl):
			logging.info(f"Updating MS2 buffer 0 with padding for {self.sized_str_entry.name}")
			name_buffer, bone_infos, verts = self.get_ms2_buffer_datas()
			# make sure buffer 0 is padded to 4 bytes
			padding = get_padding(len(name_buffer), 4)
			if padding:
				self.sized_str_entry.data_entry.update_data([name_buffer + padding, bone_infos, verts])

	def size_check(self, model_info):
		if (is_jwe(self.ovl) and model_info.pointers[0].data_size == 144) \
				or ((is_pz(self.ovl) or is_pz16(self.ovl) or is_jwe2(self.ovl)) and model_info.pointers[0].data_size == 160):
			return True
	
	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		print("\nWriting", name)
		name_buffer, bone_infos, verts = self.get_ms2_buffer_datas()
		# sizedstr data has bone count
		ms2_general_info_data = self.sized_str_entry.pointers[0].data[:24]
		# print("ms2 ss rest", self.sized_str_entry.pointers[0].data[24:])
		# ms2_general_info = self.sized_str_entry.pointers[0].load_as(Ms2SizedStrData, version_info=versions)
		# print("Ms2SizedStrData", self.sized_str_entry.pointers[0].address, ms2_general_info)
	
		ovl_header = self.pack_header(b"MS2 ")
		ms2_header = struct.pack("<2I", len(name_buffer), len(bone_infos))
	
		# for i, buffer in enumerate(buffers):
		# 	p = out_dir(name+str(i)+".ms2")
		# 	with open(p, 'wb') as outfile:
		# 		outfile.write(buffer)
	
		# Planet coaster
		if is_pc(self.ovl) or is_ztuac(self.ovl):
			# only ss entry holds any useful stuff
			ms2_buffer_info_data = b""
			next_model_info_data = b""
		# Planet Zoo, JWE
		else:
			if len(self.sized_str_entry.fragments) != 3:
				print("must have 3 fragments")
				return
			f_0, f_1, f_2 = self.sized_str_entry.fragments
	
			# f0 has information on vert & tri buffer sizes
			ms2_buffer_info_data = f_0.pointers[1].data
			# this fragment informs us about the model count of the next mdl2 that is read
			# so we can use it to collect the variable mdl2 fragments describing a model each
			next_model_info_data = f_1.pointers[1].data
		# next_model_info = f_1.pointers[1].load_as(CoreModelInfo, version_info=versions)
		# print("next_model_info", f_1.pointers[1].address, next_model_info)
	
		# write the ms2 file
		out_path = out_dir(name)
		out_paths = [out_path, ]
		with open(out_path, 'wb') as outfile:
			outfile.write(ovl_header)
			outfile.write(ms2_header)
			outfile.write(ms2_general_info_data)
			outfile.write(ms2_buffer_info_data)
			outfile.write(name_buffer)
			outfile.write(bone_infos)
			outfile.write(verts)
	
		# zeros = []
		# ones = []
		bone_info_index = 0
		# export each mdl2
		for mdl2_index, mdl2_entry in enumerate(self.sized_str_entry.children):
			mdl2_path = out_dir(mdl2_entry.name)
			out_paths.append(mdl2_path)
			with open(mdl2_path, 'wb') as outfile:
				print("Writing", mdl2_entry.name, mdl2_index)
	
				mdl2_header = struct.pack("<2I", mdl2_index, bone_info_index)
				outfile.write(ovl_header)
				outfile.write(mdl2_header)
				# pack ms2 name as a sized string
				write_sized_str(outfile, self.sized_str_entry.name)
	
				if not (is_pc(self.ovl) or is_ztuac(self.ovl)):
					# the fixed fragments
					materials, lods, objects, model_data_ptr, model_info = mdl2_entry.fragments
					print("num_models", mdl2_entry.num_models)
					# write the model info for this model, buffered from the previous model or ms2 (model_info fragments)
					outfile.write(next_model_info_data)
					# print("model_info",model_info.pointers[0].address,model_info.pointers[0].data_size,model_info.pointers[1].address, model_info.pointers[1].data_size)
					if model_info.pointers[0].data_size == 40:
						# 40 bytes (0,1 or 0,0,0,0)
						has_bone_info = model_info.pointers[0].data
					elif self.size_check(model_info):
						# read model info for next model, but just the core part without the 40 bytes of 'padding' (0,1,0,0,0)
						next_model_info_data = model_info.pointers[0].data[40:]
						has_bone_info = model_info.pointers[0].data[:40]
					# core_model_data = model_info.pointers[0].load_as(Mdl2ModelInfo, version_info=versions)
					# print(core_model_data)
					else:
						raise ValueError(
							f"Unexpected size {len(model_info.pointers[0].data)} for model_info fragment for {mdl2_entry.name}")
	
					core_model_data = struct.unpack("<5Q", has_bone_info)
					# print(core_model_data)
					var = core_model_data[1]
					bone_info_index += var
					# if var == 1:
					# 	ones.append((mdl2_index, mdl2_entry.name))
					# elif var == 0:
					# 	zeros.append((mdl2_index, mdl2_entry.name))
	
					# avoid writing bad fragments that should be empty
					if mdl2_entry.num_models:
						# need not write model_data_ptr
						for f in (materials, lods, objects):
							# print(f.pointers[0].address,f.pointers[0].data_size,f.pointers[1].address, f.pointers[1].data_size)
							outfile.write(f.pointers[1].data)
							# data 0 must be empty
							assert f.pointers[0].data == b'\x00\x00\x00\x00\x00\x00\x00\x00'
	
					# print("modeldata frags")
					for f in mdl2_entry.model_data_frags:
						# each address_0 points to ms2's f_0 address_1 (size of vert & tri buffer)
						# print(f.pointers[0].address,f.pointers[0].data_size,f.pointers[1].address, f.pointers[1].data_size)
						# model_data = f.pointers[0].load_as(ModelData, version_info=versions)
						# print(model_data)
						outfile.write(f.pointers[0].data)
		# print("ones", len(ones), ones)
		# print("zeros", len(zeros), zeros)
		return out_paths
	
	def get_ms2_buffer_datas(self):
		assert self.sized_str_entry.data_entry
		buffers = self.sized_str_entry.data_entry.stream_datas
		name_buffer = buffers[0]
		bone_infos = buffers[1]
		verts = b"".join(buffers[2:])
		for i, vbuff in enumerate(buffers[2:]):
			print(f"Vertex buffer {i}, size {len(vbuff)} bytes")
		print("buffers", len(buffers))
		print(f"name_buffer: {len(name_buffer)}, bone_infos: {len(bone_infos)}, verts: {len(verts)}")
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
				if fgm_name not in self.ovl.ss_dict:
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
			# overwrite mdl2 modeldata frags
			for frag, modeldata in zip(mdl2_entry.model_data_frags, mdl2.models):
				frag_data = as_bytes(modeldata, version_info=versions)
				frag.pointers[0].update_data(frag_data, update_copies=True)
	
			materials, lods, objects, model_data_ptr, model_info = mdl2_entry.fragments
			for frag, mdl2_list in (
					(materials, mdl2.materials,),
					(lods, mdl2.lods),
					(objects, mdl2.objects)):
				if len(mdl2_list) > 0:
					data = as_bytes(mdl2_list, version_info=versions)
					frag.pointers[1].update_data(data, update_copies=True, pad_to=8)
	
		for mdl2 in mdl2s:
			data = as_bytes(mdl2.model_info, version_info=versions)
			if mdl2.index == 0:
				f_0, f_1, f_2 = self.sized_str_entry.fragments
				f_1.pointers[1].update_data(data, update_copies=True)
			else:
				# grab the preceding mdl2 entry since it points ahead
				mdl2_entry = self.sized_str_entry.children[mdl2.index - 1]
				# get its model info fragment
				materials, lods, objects, model_data_ptr, model_info = mdl2_entry.fragments
				if self.size_check(model_info):
					data = model_info.pointers[0].data[:40] + data
					model_info.pointers[0].update_data(data, update_copies=True)
	
		logging.info(f"Injecting MS2")
		ms2_file = Ms2File()
		ms2_file.load(ms2_file_path, read_bytes=True)
		# load ms2 ss data
		ms2_ss_bytes = as_bytes(ms2_file.general_info, version_info=versions) + self.sized_str_entry.pointers[0].data[24:]
		self.sized_str_entry.pointers[0].update_data(ms2_ss_bytes, update_copies=True)
	
		# overwrite ms2 buffer info frag
		buffer_info_frag = self.sized_str_entry.fragments[0]
		buffer_info_frag.pointers[1].update_data(as_bytes(ms2_file.buffer_info, version_info=versions), update_copies=True)
	
		# update ms2 data
		self.sized_str_entry.data_entry.update_data([ms2_file.buffer_0_bytes, ms2_file.buffer_1_bytes, ms2_file.buffer_2_bytes])
