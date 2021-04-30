import io
import os
import struct
import logging

from generated.formats.ms2.compound.CoreModelInfo import CoreModelInfo
from generated.formats.ms2.compound.Mdl2ModelInfo import Mdl2ModelInfo
from modules.formats.shared import pack_header, get_versions
from modules.helpers import write_sized_str, as_bytes
from generated.formats.ms2 import Mdl2File, Ms2File, is_old
from generated.formats.ms2.compound.Ms2BufferInfo import Ms2BufferInfo
from generated.formats.ms2.compound.LodInfo import LodInfo
from generated.formats.ms2.compound.ModelData import ModelData
from generated.formats.ovl.versions import *


def write_ms2(ovl, ms2_sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = ms2_sized_str_entry.name
	assert ms2_sized_str_entry.data_entry
	buffers = ms2_sized_str_entry.data_entry.stream_datas
	name_buffer = buffers[0]
	bone_infos = buffers[1]
	verts = b"".join(buffers[2:])
	for i, vbuff in enumerate(buffers[2:]):
		print(f"Vertex buffer {i}, size {len(vbuff)} bytes")
	print("\nWriting", name)
	print("buffers", len(buffers))
	print(f"name_buffer: {len(name_buffer)}, bone_infos: {len(bone_infos)}, verts: {len(verts)}")
	# sizedstr data has bone count
	ms2_general_info_data = ms2_sized_str_entry.pointers[0].data[:24]
	# print("ms2 ss rest", ms2_sized_str_entry.pointers[0].data[24:])
	# ms2_general_info = ms2_sized_str_entry.pointers[0].load_as(Ms2SizedStrData, version_info=versions)
	# print("Ms2SizedStrData", ms2_sized_str_entry.pointers[0].address, ms2_general_info)

	ovl_header = pack_header(ovl, b"MS2 ")
	ms2_header = struct.pack("<2I", len(name_buffer), len(bone_infos))

	# for i, buffer in enumerate(buffers):
	# 	p = out_dir(name+str(i)+".ms2")
	# 	with open(p, 'wb') as outfile:
	# 		outfile.write(buffer)

	# Planet coaster
	if is_pc(ovl) or is_ztuac(ovl):
		# only ss entry holds any useful stuff
		ms2_buffer_info_data = b""
		next_model_info_data = b""
	# Planet Zoo, JWE
	else:
		if len(ms2_sized_str_entry.fragments) != 3:
			print("must have 3 fragments")
			return
		f_0, f_1, f_2 = ms2_sized_str_entry.fragments

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
	for mdl2_index, mdl2_entry in enumerate(ms2_sized_str_entry.children):
		mdl2_path = out_dir(mdl2_entry.name)
		out_paths.append(mdl2_path)
		with open(mdl2_path, 'wb') as outfile:
			print("Writing", mdl2_entry.name, mdl2_index)

			mdl2_header = struct.pack("<2I", mdl2_index, bone_info_index)
			outfile.write(ovl_header)
			outfile.write(mdl2_header)
			# pack ms2 name as a sized string
			write_sized_str(outfile, ms2_sized_str_entry.name)

			if not (is_pc(ovl) or is_ztuac(ovl)):
				# the fixed fragments
				materials, lods, objects, model_data_ptr, model_info = mdl2_entry.fragments
				print("num_models", mdl2_entry.num_models)
				# write the model info for this model, buffered from the previous model or ms2 (model_info fragments)
				outfile.write(next_model_info_data)
				# print("model_info",model_info.pointers[0].address,model_info.pointers[0].data_size,model_info.pointers[1].address, model_info.pointers[1].data_size)
				if model_info.pointers[0].data_size == 40:
					# 40 bytes (0,1 or 0,0,0,0)
					has_bone_info = model_info.pointers[0].data
				elif (is_jwe(ovl) and model_info.pointers[0].data_size == 144) \
					or (is_pz(ovl) and model_info.pointers[0].data_size == 160):
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


def load_ms2(ovl_data, ms2_file_path, ms2_entry):
	logging.info(f"Injecting MS2")
	ms2_file = Ms2File()
	ms2_file.load(ms2_file_path, read_bytes=True)

	versions = get_versions(ovl_data)

	# load ms2 ss data
	ms2_ss_bytes = as_bytes(ms2_file.general_info, version_info=versions) + ms2_entry.pointers[0].data[24:]
	ms2_entry.pointers[0].update_data(ms2_ss_bytes, update_copies=True)

	# overwrite ms2 buffer info frag
	buffer_info_frag = ms2_entry.fragments[0]
	buffer_info_frag.pointers[1].update_data(as_bytes(ms2_file.buffer_info, version_info=versions), update_copies=True)

	# update ms2 data
	ms2_entry.data_entry.update_data([ms2_file.buffer_0_bytes, ms2_file.buffer_1_bytes, ms2_file.buffer_2_bytes])

	logging.info(f"Injecting MDL2s")
	ms2_dir = os.path.dirname(ms2_file_path)
	mdl2s = []
	for mdl2_entry in ms2_entry.children:
		mdl2_path = os.path.join(ms2_dir, mdl2_entry.name)
		mdl2 = Mdl2File()
		mdl2.load(mdl2_path)
		mdl2s.append(mdl2)

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
			f_0, f_1, f_2 = ms2_entry.fragments
			f_1.pointers[1].update_data(data, update_copies=True)
		else:
			# grab the preceding mdl2 entry since it points ahead
			mdl2_entry = ms2_entry.children[mdl2.index - 1]
			# get its model info fragment
			materials, lods, objects, model_data_ptr, model_info = mdl2_entry.fragments
			if (is_jwe(ovl_data) and model_info.pointers[0].data_size == 144) \
				or (is_pz(ovl_data) and model_info.pointers[0].data_size == 160):
				data = model_info.pointers[0].data[:40] + data
				model_info.pointers[0].update_data(data, update_copies=True)


class Ms2Loader(Ms2File):

	def collect(self, ovl, file_entry):
		self.ovl = ovl
		ms2_entry = self.ovl.ss_dict[file_entry.name]
		ss_pointer = ms2_entry.pointers[0]
		self.ovs = ovl.static_archive.content
		frags = self.ovs.header_entries[ss_pointer.header_index].fragments
		if not is_old(self.ovl):
			ms2_entry.fragments = self.ovs.get_frags_after_count(frags, ss_pointer.address, 3)
			# print(ms2_entry.fragments)
			# second pass: collect model fragments
			versions = get_versions(self.ovl)
			# assign the mdl2 frags to their sized str entry

			# 3 fixed fragments laid out like
			# sse p0: ms2_general_info_data (24 bytes)
			# 0 - p0: 8*00 				p1: buffer_info
			# 1 - p0: 8*00 				p1: core_model_info for first mdl2 file
			# 2 - p0: 8*00 				p1: 2 unk uints: -1, 0
			f_1 = ms2_entry.fragments[1]
			core_model_info = f_1.pointers[1].load_as(CoreModelInfo, version_info=versions)[0]
			# print("next model info:", core_model_info)
			for mdl2_entry in ms2_entry.children:
				assert mdl2_entry.ext == ".mdl2"
				self.collect_mdl2(mdl2_entry, core_model_info, f_1.pointers[1])
				pink = mdl2_entry.fragments[4]
				if (is_jwe(self.ovl) and pink.pointers[0].data_size == 144) \
					or (is_pz(self.ovl) and pink.pointers[0].data_size == 160):
					core_model_info = pink.pointers[0].load_as(Mdl2ModelInfo, version_info=versions)[0].info

		else:
			ms2_entry.fragments = self.ovs.get_frags_after_count(frags, ss_pointer.address, 1)

	def collect_mdl2(self, mdl2_entry, core_model_info, mdl2_pointer):
		logging.info(f"MDL2: {mdl2_entry.name}")
		mdl2_entry.fragments = self.ovs.frags_from_pointer(mdl2_pointer, 5)
		# these 5 fixed fragments are laid out like
		# 0 - p0: 8*00 				p1: materials
		# 1 - p0: 8*00 				p1: lods
		# 2 - p0: 8*00 				p1: objects
		# 3 - p0: 8*00 				p1: -> first ModelData, start of ModelData fragments block
		# 4 - p0: next_model_info	p1: -> materials
		materials, lods, objects, model_data_ptr, model_info = mdl2_entry.fragments
		# remove padding
		objects.pointers[1].split_data_padding(4 * core_model_info.num_objects)

		# get and set fragments
		logging.debug(f"Num model data frags = {core_model_info.num_models}")
		mdl2_entry.model_data_frags = self.ovs.frags_from_pointer(model_data_ptr.pointers[1], core_model_info.num_models)
