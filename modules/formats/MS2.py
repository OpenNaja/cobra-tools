import io
import os
import struct

from modules.util import write_sized_str, to_bytes
from pyffi_ext.formats.ms2 import Ms2Format


def write_ms2(archive, ms2_sized_str_entry):
	name = ms2_sized_str_entry.name
	if not ms2_sized_str_entry.data_entry:
		print("No data entry for ",name)
		return
	buffers = ms2_sized_str_entry.data_entry.buffer_datas
	if len(buffers) == 3:
		bone_names, bone_matrices, verts = buffers
	elif len(buffers) == 2:
		bone_names, verts = buffers
		bone_matrices = b""
	else:
		raise BufferError(f"Wrong amount of buffers for {name}\nWanted 2 or 3 buffers, got {len(buffers)}")

	# sizedstr data has bone count
	ms2_general_info_data = ms2_sized_str_entry.pointers[0].data[:24]
	# ms2_general_info = ms2_sized_str_entry.pointers[0].read_as(Ms2Format.Ms2SizedStrData, archive)
	# print("Ms2SizedStrData", ms2_sized_str_entry.pointers[0].address, ms2_general_info)

	ms2_header = struct.pack("<4s4I", b"MS2 ", archive.ovl.version, archive.ovl.flag_2, len(bone_names),
							 len(bone_matrices))

	print("\nWriting",name)
	print("\nbuffers",len(buffers))
	for i, buffer in enumerate(buffers):
		with open(archive.indir(name+str(i)+".ms2"), 'wb') as outfile:
			outfile.write(buffer)

	# Planet coaster
	if archive.is_pc():
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
		# next_model_info = f_1.pointers[1].read_as(Ms2Format.CoreModelInfo, archive)
		# print("next_model_info", f_1.pointers[1].address, next_model_info)

	# write the ms2 file
	with open(archive.indir(name), 'wb') as outfile:
		outfile.write(ms2_header)
		outfile.write(ms2_general_info_data)
		outfile.write(ms2_buffer_info_data)
		outfile.write(bone_names)
		outfile.write(bone_matrices)
		outfile.write(verts)

	# export each mdl2
	for mdl2_index, mdl2_entry in enumerate(ms2_sized_str_entry.children):
		with open(archive.indir(mdl2_entry.name), 'wb') as outfile:
			print("Writing", mdl2_entry.name, mdl2_index)

			mdl2_header = struct.pack("<4s3I", b"MDL2", archive.ovl.version, archive.ovl.flag_2, mdl2_index )
			outfile.write(mdl2_header)
			# pack ms2 name as a sized string
			write_sized_str(outfile, ms2_sized_str_entry.name)

			if not archive.is_pc():
				# the fixed fragments
				green_mats_0, blue_lod, orange_mats_1, yellow_lod0, pink = mdl2_entry.fragments
				print("model_count",mdl2_entry.model_count)
				# write the model info for this model, buffered from the previous model or ms2 (pink fragments)
				outfile.write(next_model_info_data)
				# print("PINK",pink.pointers[0].address,pink.pointers[0].data_size,pink.pointers[1].address, pink.pointers[1].data_size)
				if pink.pointers[0].data_size == 40:
					pass
					# 40 bytes of 'padding' (0,1 or 0,0,0,0)
					# core_model_data = pink.pointers[0].read_as(Ms2Format.Mdl2FourtyInfo, archive)
					# print(core_model_data)
				elif (archive.ovl.flag_2 == 24724 and pink.pointers[0].data_size == 144) \
				or   (archive.ovl.flag_2 == 8340  and pink.pointers[0].data_size == 160):
					# read model info for next model, but just the core part without the 40 bytes of 'padding' (0,1,0,0,0)
					next_model_info_data = pink.pointers[0].data[40:]
					# core_model_data = pink.pointers[0].read_as(Ms2Format.Mdl2ModelInfo, archive)
					# print(core_model_data)
				else:
					print("unexpected size for pink")

				# avoid writing bad fragments that should be empty
				if mdl2_entry.model_count:
					# print("fixed fragments")
					# need not write lod0
					for f in (green_mats_0, blue_lod, orange_mats_1):
						# print(f.pointers[0].address,f.pointers[0].data_size,f.pointers[1].address, f.pointers[1].data_size)
						other_data = f.pointers[1].data
						outfile.write(other_data)

				# print("modeldata frags")
				for f in mdl2_entry.model_data_frags:
					# each address_0 points to ms2's f_0 address_1 (size of vert & tri buffer)
					# print(f.pointers[0].address,f.pointers[0].data_size,f.pointers[1].address, f.pointers[1].data_size)
					# model_data = f.pointers[0].read_as(Ms2Format.ModelData, archive)
					# print(model_data)

					model_data = f.pointers[0].data
					outfile.write(model_data)


class Mdl2Holder:
	"""Used to handle injection of mdl2 files"""
	def __init__(self, archive):
		self.name = "NONE"
		self.lodinfo = b""
		self.mdl2_data = Ms2Format.Data()
		self.model_data_frags = []
		self.archive = archive
		self.source = "NONE"
		self.mdl2_entry = None

		self.bone_info_buffer = []# list or array of pyffi modeldata structs
		self.models = []
		# one per model
		self.verts_bytes = []
		self.tris_bytes = []

		self.lods = []

	def from_file(self, mdl2_file_path):
		"""Read a mdl2 + ms2 file"""
		print(f"Reading {mdl2_file_path} from file")
		self.name = os.path.basename(mdl2_file_path)
		self.source = "EXT"
		with open(mdl2_file_path, "rb") as mdl2_stream:
			self.mdl2_data.inspect(mdl2_stream)
			ms2_name = self.mdl2_data.mdl2_header.name.decode()
			self.models = self.mdl2_data.mdl2_header.models
			self.lods = self.mdl2_data.mdl2_header.lods

		# get ms2 buffers
		ms2_dir = os.path.dirname(mdl2_file_path)
		ms2_path = os.path.join(ms2_dir, ms2_name)
		with open(ms2_path, "rb") as ms2_stream:
			ms2_header = Ms2Format.Ms2InfoHeader()
			ms2_header.read(ms2_stream, data=self.mdl2_data)
			self.bone_info_buffer = ms2_stream.read(ms2_header.bone_info_size)
			eoh = ms2_stream.tell()

			self.read_verts_tris(ms2_stream, ms2_header.buffer_info, eoh)

	def read_verts_tris(self, ms2_stream, buffer_info, eoh=0, ):
		"""Reads vertices and triangles into list of bytes for all models of this file"""
		print("reading verts and tris")
		self.verts_bytes = []
		self.tris_bytes = []
		for model in self.models:
			# first, get the buffers for this model from the input
			ms2_stream.seek(eoh + model.vertex_offset)
			verts = ms2_stream.read(model.size_of_vertex * model.vertex_count)

			ms2_stream.seek(eoh + buffer_info.vertexdatasize + model.tri_offset)
			tris = ms2_stream.read(2 * model.tri_index_count)
			self.verts_bytes.append(verts)
			self.tris_bytes.append(tris)
		# print(len(self.tris_bytes))

	def from_entry(self, mdl2_entry):
		"""Reads the required data to represent this model from the archive"""
		print(f"Reading {mdl2_entry.name} from archive")
		self.name = mdl2_entry.name
		self.source = "OVL"
		self.mdl2_entry = mdl2_entry
		ms2_entry = mdl2_entry.parent

		# read the vertex data for this from the archive's ms2
		buffer_info_frag = ms2_entry.fragments[0]
		buffer_info = buffer_info_frag.pointers[1].read_as(Ms2Format.Ms2BufferInfo, self.archive)[0]
		print(buffer_info)

		verts_tris_buffer = ms2_entry.data_entry.buffer_datas[-1]
		if len(mdl2_entry.fragments[1].pointers[1].data) < 104:
			if len(mdl2_entry.fragments[1].pointers[1].data) % 20 == 0:
				lod_pointer = mdl2_entry.fragments[1].pointers[1]
				lod_count = len(lod_pointer.data) // 20
				# todo get count from CoreModelInfo
				self.lods = lod_pointer.read_as(Ms2Format.LodInfo, self.archive, num=lod_count)
		print("lod list",self.lods)
		self.models = []
		for f in mdl2_entry.model_data_frags:
			model = f.pointers[0].read_as(Ms2Format.ModelData, self.archive)[0]
			self.models.append(model)
		print("num models:",len(self.models))
		if len(self.models) > 0:
			with io.BytesIO(verts_tris_buffer) as ms2_stream:
				self.read_verts_tris(ms2_stream, buffer_info)

	def update_entry(self):
		# overwrite mdl2 modeldata frags
		for frag, modeldata in zip(self.mdl2_entry.model_data_frags, self.models):
			frag_data = to_bytes(modeldata, self.mdl2_data)
			frag.pointers[0].update_data(frag_data, update_copies=True)
		if len(self.lods) > 0:
			self.lodinfo = to_bytes(self.lods, self.mdl2_data)
			# overwrite mdl2 lodinfo frag
			self.mdl2_entry.fragments[1].pointers[1].update_data(self.lodinfo, update_copies=True)

	def __repr__(self):
		return f"<Mdl2Holder: {self.name} [{self.source}], V{len(self.verts_bytes)}, T{len(self.tris_bytes)}, M{len(self.models)}, L{len(self.lods)}>"


class Ms2Holder:
	"""Used to handle injection of ms2 files"""
	def __init__(self, archive):
		self.name = "NONE"
		self.buffer_info = None
		self.buff_datas = []
		self.mdl2s = []
		self.archive = archive
		self.ms2_entry = None
		self.bone_info = []

	def __repr__(self):
		return f"<Ms2Holder: {self.name}, Models: {len(self.mdl2s)}>"

	def from_mdl2_file(self, mdl2_file_path):
		new_name = os.path.basename(mdl2_file_path)

		for i, mdl2 in enumerate(self.mdl2s):
			if mdl2.name == new_name:
				print(f"Match, slot {i}")
				mdl2.from_file(mdl2_file_path)
				self.bone_info = mdl2.bone_info_buffer
				print(len(self.bone_info))
				break
		else:
			raise AttributeError(f"No match for {mdl2}")
		return mdl2

	def from_entry(self, ms2_entry):
		"""Read from the archive"""
		print(f"Reading {ms2_entry.name} from archive")
		self.name = ms2_entry.name
		self.mdl2s = []
		self.ms2_entry = ms2_entry

		buffer_info_frag = self.ms2_entry.fragments[0]
		# print(buffer_info_frag.pointers[1].data)
		if not buffer_info_frag.pointers[1].data:
			raise AttributeError("No buffer info, aborting merge")
		self.buffer_info = buffer_info_frag.pointers[1].read_as(Ms2Format.Ms2BufferInfo, self.archive)[0]
		print(self.buffer_info)

		for mdl2_entry in self.ms2_entry.children:
			mdl2 = Mdl2Holder(self.archive)
			mdl2.from_entry(mdl2_entry)
			self.mdl2s.append(mdl2)
		print(self.mdl2s)

	def update_entry(self):
		print(f"Updating {self}")

		# write each model's vert & tri block to a temporary buffer
		temp_vert_writer = io.BytesIO()
		temp_tris_writer = io.BytesIO()

		# set initial offset for the first modeldata
		vert_offset = 0
		tris_offset = 0

		# go over all input mdl2 files
		for mdl2 in self.mdl2s:
			print(f"Flushing {mdl2}")
			# read the mdl2
			for model, verts, tris in zip(mdl2.models, mdl2.verts_bytes, mdl2.tris_bytes):
				print(vert_offset)
				print(tris_offset)
				# write buffer to each output
				temp_vert_writer.write(verts)
				temp_tris_writer.write(tris)

				# update mdl2 offset values
				model.vertex_offset = vert_offset
				model.tri_offset = tris_offset

				# get offsets for the next model
				vert_offset = temp_vert_writer.tell()
				tris_offset = temp_tris_writer.tell()

		# get bytes from IO object
		vert_bytes = temp_vert_writer.getvalue()
		tris_bytes = temp_tris_writer.getvalue()

		buffers = self.ms2_entry.data_entry.buffer_datas[:-2]
		buffers.append(self.bone_info)
		buffers.append(vert_bytes+tris_bytes)

		# modify buffer size
		self.buffer_info.vertexdatasize = len(vert_bytes)
		self.buffer_info.facesdatasize = len(tris_bytes)
		# overwrite ms2 buffer info frag
		buffer_info_frag = self.ms2_entry.fragments[0]
		buffer_info_frag.pointers[1].update_data(to_bytes(self.buffer_info, self.archive), update_copies=True)

		# update data
		self.ms2_entry.data_entry.update_data(buffers)

		# also flush the mdl2s
		for mdl2 in self.mdl2s:
			mdl2.update_entry()


def load_mdl2(ovl_data, mdl2_tups):

	# first resolve tuples to associated ms2 entry
	ms2_mdl2_dic = {}
	for mdl2_file_path, mdl2_entry in mdl2_tups:
		ms2_entry = mdl2_entry.parent
		if ms2_entry not in ms2_mdl2_dic:
			ms2_mdl2_dic[ms2_entry] = []
		ms2_mdl2_dic[ms2_entry].append(mdl2_file_path)

	# then read the ms2 and all associated new mdl2 files for it
	for ms2_entry, mdl2_file_paths in ms2_mdl2_dic.items():

		# first read the ms2 and all of its mdl2s from the archive
		ms2 = Ms2Holder(ovl_data)
		ms2.from_entry(ms2_entry)

		# load new input
		for mdl2_file_path in mdl2_file_paths:
			ms2.from_mdl2_file(mdl2_file_path)

		# the actual injection
		ms2.update_entry()
