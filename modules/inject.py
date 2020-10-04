import struct
import os
import io
import tempfile
import shutil
import pyffi

from modules.formats.DDS import load_png, load_dds
from pyffi_ext.formats.ms2 import Ms2Format
from pyffi_ext.formats.fgm import FgmFormat
from pyffi_ext.formats.materialcollection import MaterialcollectionFormat
from generated.formats.bnk import BnkFile

from util import imarray


def split_path(fp):
	in_dir, name_ext = os.path.split(fp)
	name, ext = os.path.splitext(name_ext)
	ext = ext.lower()
	return name_ext, name, ext


def inject(ovl_data, file_paths, show_dds, is_2K):

	# write modified version to tmp dir
	tmp_dir = tempfile.mkdtemp("-cobra-png")

	dupecheck = []
	mdl2_tups = []
	for file_path in file_paths:
		name_ext, name, ext = split_path(file_path)
		print("Injecting", name_ext)
		# check for separated array tiles & flipped channels
		if ext == ".png":
			out_path = imarray.inject_wrapper(file_path, dupecheck, tmp_dir)
			# skip dupes
			if not out_path:
				print("Skipping injection of", file_path)
				continue
			# update the file path to the temp file with flipped channels or rebuilt array
			file_path = out_path
			name_ext, name, ext = split_path(file_path)
		# image files are stored as tex files in the archive
		if ext in (".dds", ".png"):
			name_ext = name+".tex"
		elif ext == ".matcol":
			name_ext = name+".materialcollection"
		elif ext == ".otf" or ext == ".ttf":
			name_ext = name[:-1]
			ext = ".fct"
		if ext == ".wem":
			bnk_name, wem_name = name.rsplit("_", 1)
			name_ext = bnk_name + ".bnk"
		# find the sizedstr entry that refers to this file
		sized_str_entry = ovl_data.get_sized_str_entry(name_ext)
		if is_2K:
		# Grab OVS sized string for Textures
			if sized_str_entry.ext == "tex":
				for lod_i in range(1):
					for archive in ovl_data.ovs_files[1:]:
						for other_sizedstr in archive.sized_str_entries:
							if sized_str_entry.basename in other_sizedstr.name and "_lod"+str(lod_i) in other_sizedstr.name:
								ovs_sized_str_entry = other_sizedstr
		else:
			ovs_sized_str_entry = sized_str_entry
		# do the actual injection, varies per file type
		if ext == ".mdl2":
			mdl2_tups.append((file_path, sized_str_entry))
		if ext == ".fgm":
			load_fgm(ovl_data, file_path, sized_str_entry)
		elif ext == ".png":
			load_png(ovl_data, file_path, sized_str_entry, show_dds, is_2K, ovs_sized_str_entry)
		elif ext == ".dds":
			load_dds(ovl_data, file_path, sized_str_entry, is_2K, ovs_sized_str_entry)
		elif ext == ".txt":
			load_txt(ovl_data, file_path, sized_str_entry)
		elif ext == ".wem":
			load_wem(ovl_data, file_path, sized_str_entry, bnk_name, wem_name)
		elif ext == ".xmlconfig":
			load_xmlconfig(ovl_data, file_path, sized_str_entry)
		elif ext == ".fdb":
			load_fdb(ovl_data, file_path, sized_str_entry, name)
		elif ext == ".matcol":
			load_materialcollection(ovl_data, file_path, sized_str_entry)
		elif ext == ".lua":
			load_lua(ovl_data, file_path, sized_str_entry)
		elif ext == ".fct":
			load_fct(ovl_data, file_path, sized_str_entry, name[-1])
		elif ext == ".assetpkg":
			load_assetpkg(ovl_data, file_path, sized_str_entry)

	load_mdl2(ovl_data, mdl2_tups)
	shutil.rmtree(tmp_dir)


def to_bytes(inst, data):
	"""helper that returns the bytes representation of a pyffi struct"""
	# we must make sure that pyffi arrays are not treated as a list although they are an instance of 'list'
	if isinstance(inst, list) and not isinstance(inst, pyffi.object_models.xml.array.Array):
		return b"".join(to_bytes(c, data) for c in inst)
	if isinstance(inst, bytes):
		return inst
	# zero terminated strings show up as strings
	if isinstance(inst, str):
		return inst.encode() + b"\x00"
	with io.BytesIO() as frag_writer:
		inst.write(frag_writer, data=data)
		return frag_writer.getvalue()


def load_txt(ovl_data, txt_file_path, txt_sized_str_entry):
	txt_pointer = txt_sized_str_entry.pointers[0]
	# first make sure that the padding has been separated from the data
	size = struct.unpack("<I", txt_pointer.data[:4])[0]
	txt_pointer.split_data_padding(4+size)
	with open(txt_file_path, 'rb') as stream:
		raw_txt_bytes = stream.read()
		data = struct.pack("<I", len(raw_txt_bytes)) + raw_txt_bytes
	# make sure all are updated, and pad to 8 bytes, using old padding
	txt_pointer.update_data(data, update_copies=True, pad_to=8, include_old_pad=True)
	
def load_fct(ovl_data, file_path, sized_str_entry, index):
	# read fct
	# inject fct buffers
	# update sized string
	ss_len = len(sized_str_entry.pointers[0].data)/4
	ss_data = list(struct.unpack("<4f{}I".format(int(ss_len - 4)),sized_str_entry.pointers[0].data))
	pad_size = ss_data[8]
	data_sizes = (ss_data[10],ss_data[12],ss_data[14],ss_data[16])
	old_buffer_bytes = sized_str_entry.data_entry.buffer_datas[0]
	print("old",len(old_buffer_bytes))
	pad_bytes = old_buffer_bytes[0:pad_size]
	d0 = old_buffer_bytes[pad_size:data_sizes[0]+pad_size]
	d1 = old_buffer_bytes[data_sizes[0]+pad_size:data_sizes[0]+pad_size+data_sizes[1]]
	d2 = old_buffer_bytes[data_sizes[0]+pad_size+data_sizes[1]:data_sizes[0]+pad_size+data_sizes[1]+data_sizes[2]]
	d3 = old_buffer_bytes[data_sizes[0]+pad_size+data_sizes[1]+data_sizes[2]:]
	print("old2",len(pad_bytes+d0+d1+d2+d3))

	#data_size = ss_data[10]
	print("updating index: ",index)

	with open(file_path, "rb") as stream:
		# load the new buffer
		new_buffer_bytes = stream.read()


		buffer_bytes=pad_bytes# update the correct ss entry size
		if int(index) == 0:
			ss_data[10] = len(new_buffer_bytes)
			buffer_bytes+=new_buffer_bytes
			buffer_bytes+= d1
			buffer_bytes+= d2
			buffer_bytes+=d3
		elif int(index) == 1:
			ss_data[12] = len(new_buffer_bytes)
			buffer_bytes+=d0
			buffer_bytes+=new_buffer_bytes
			buffer_bytes+= d2
			buffer_bytes+=d3
		elif int(index) == 2:
			ss_data[14] = len(new_buffer_bytes)
			buffer_bytes+=d0
			buffer_bytes+= d1
			buffer_bytes+=new_buffer_bytes
			buffer_bytes+=d3
		elif int(index) == 3:
			ss_data[16] = len(new_buffer_bytes)
			buffer_bytes+=d0
			buffer_bytes+= d1
			buffer_bytes+= d2
			buffer_bytes+=new_buffer_bytes
            
    
		print(len(buffer_bytes))
            
		# update the buffers
		sized_str_entry.data_entry.update_data( (buffer_bytes,) )
            
		data = struct.pack("<4f{}I".format(int(ss_len - 4)), *ss_data)
		sized_str_entry.pointers[0].update_data(data, update_copies=True)


def load_wem(ovl_data, wem_file_path, sized_str_entry, bnk_name, wem_id):
	bnk = os.path.splitext(sized_str_entry.name)[0]
	archive = ovl_data.ovs_files[0]
	bnk_path = f"{archive.ovl.file_no_ext}_{bnk}_bnk_b.aux"
	if os.path.isfile(bnk_path):
		if "_media_" not in bnk_path:
			print("skipping events bnk", bnk_path)
			return

		data = BnkFile()
		data.load(bnk_path)
		data.inject_audio(wem_file_path, wem_id)
		data.save(bnk_path)
		events = BnkFile()
		ss = sized_str_entry.name.rsplit("_", 1)[0]
		eventspath = f"{archive.ovl.file_no_ext}_{ss}_events_bnk_b.aux"
		events.load(eventspath)
		print(events)
		events.inject_hirc(wem_file_path, wem_id)
		events.save(eventspath)
        
        
		# first uint of the buffer is the size of the data that should be read from the aux file
		buffers = sized_str_entry.data_entry.buffer_datas
		buffers[0] = struct.pack("<I", data.size_for_ovl) + buffers[0][4:]
		# update the buffer
		sized_str_entry.data_entry.update_data(buffers)


def load_xmlconfig(ovl_data, xml_file_path, xml_sized_str_entry):
	with open(xml_file_path, 'rb') as stream:
		# add zero terminator
		data = stream.read() + b"\x00"
		# make sure all are updated, and pad to 8 bytes
		xml_sized_str_entry.fragments[0].pointers[1].update_data(data, update_copies=True, pad_to=8)


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
		# adapted from old merger code

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


def load_fgm(ovl_data, fgm_file_path, fgm_sized_str_entry):

	fgm_data = FgmFormat.Data()
	# open file for binary reading
	with open(fgm_file_path, "rb") as stream:
		fgm_data.read(stream, fgm_data, file=fgm_file_path)

		sizedstr_bytes = to_bytes(fgm_data.fgm_header.fgm_info, fgm_data) + to_bytes(fgm_data.fgm_header.two_frags_pad, fgm_data)

		# todo - move texpad into fragment padding?
		textures_bytes = to_bytes(fgm_data.fgm_header.textures, fgm_data) + to_bytes(fgm_data.fgm_header.texpad, fgm_data)
		attributes_bytes = to_bytes(fgm_data.fgm_header.attributes, fgm_data)

		# read the other datas
		stream.seek(fgm_data.eoh)
		zeros_bytes = stream.read(fgm_data.fgm_header.zeros_size)
		data_bytes = stream.read(fgm_data.fgm_header.data_lib_size)
		buffer_bytes = stream.read()

	# the actual injection
	fgm_sized_str_entry.data_entry.update_data( (buffer_bytes,) )
	fgm_sized_str_entry.pointers[0].update_data(sizedstr_bytes, update_copies=True)

	if len(fgm_sized_str_entry.fragments) == 4:
		datas = (textures_bytes, attributes_bytes, zeros_bytes, data_bytes)
	# fgms without zeros
	elif len(fgm_sized_str_entry.fragments) == 3:
		datas = (textures_bytes, attributes_bytes, data_bytes)
	# fgms for variants
	elif len(fgm_sized_str_entry.fragments) == 2:
		datas = (attributes_bytes, data_bytes)
	else:
		raise AttributeError("Unexpected fgm frag count")

	# inject fragment datas
	for frag, data in zip(fgm_sized_str_entry.fragments, datas):
		frag.pointers[1].update_data(data, update_copies=True)


def update_matcol_pointers(pointers, new_names):
	# it looks like fragments are not reused here, and not even pointers are
	# but as they point to the same address the writer treats them as same
	# so the pointer map has to be updated for the involved header entries
	# also the copies list has to be adjusted

	# so this is a hack that only considers one entry for each union of pointers
	# map doffset to tuple of pointer and new data
	dic = {}
	for p, n in zip(pointers, new_names):
		dic[p.data_offset] = (p, n.encode() + b"\x00")
	sorted_keys = list(sorted(dic))
	# print(sorted_keys)
	print("Names in ovl order:", list(dic[k][1] for k in sorted_keys))
	sum = 0
	for k in sorted_keys:
		p, d = dic[k]
		sum += len(d)
		for pc in p.copies:
			pc.data = d
			pc.padding = b""
	pad_to = 64
	mod = sum % pad_to
	if mod:
		padding = b"\x00" * (pad_to-mod)
	else:
		padding = b""
	for pc in p.copies:
		pc.padding = padding


def load_materialcollection(ovl_data, matcol_file_path, sized_str_entry):
	matcol_data = MaterialcollectionFormat.Data()
	# open file for binary reading
	with open(matcol_file_path, "rb") as stream:
		matcol_data.read(stream)
		# print(matcol_data.header)

		if sized_str_entry.has_texture_list_frag:
			pointers = [tex_frag.pointers[1] for tex_frag in sized_str_entry.tex_frags]
			new_names = [n for t in matcol_data.header.texture_wrapper.textures for n in (t.fgm_name, t.texture_suffix, t.texture_type)]
		else:
			pointers = []
			new_names = []

		if sized_str_entry.is_variant:
			for (m0,), variant in zip(sized_str_entry.mat_frags, matcol_data.header.variant_wrapper.materials):
				# print(layer.name)
				pointers.append(m0.pointers[1])
				new_names.append(variant)
		elif sized_str_entry.is_layered:
			for (m0, info, attrib), layer in zip(sized_str_entry.mat_frags, matcol_data.header.layered_wrapper.layers):
				# print(layer.name)
				pointers.append(m0.pointers[1])
				new_names.append(layer.name)
				for frag, wrapper in zip(info.children, layer.infos):
					frag.pointers[0].update_data( to_bytes(wrapper.info, matcol_data), update_copies=True )
					frag.pointers[1].update_data( to_bytes(wrapper.name, matcol_data), update_copies=True )
					pointers.append(frag.pointers[1])
					new_names.append(wrapper.name)
				for frag, wrapper in zip(attrib.children, layer.attribs):
					frag.pointers[0].update_data( to_bytes(wrapper.attrib, matcol_data), update_copies=True )
					frag.pointers[1].update_data( to_bytes(wrapper.name, matcol_data), update_copies=True )
					pointers.append(frag.pointers[1])
					new_names.append(wrapper.name)

		update_matcol_pointers(pointers, new_names)


def load_fdb(ovl_data, fdb_file_path, fdb_sized_str_entry, fdb_name):
	# read fdb
	# inject fdb buffers
	# update sized string

	with open(fdb_file_path, "rb") as fdb_stream:
		# load the new buffers
		buffer1_bytes = fdb_stream.read()
		buffer0_bytes = fdb_name.encode()
		# update the buffers
		fdb_sized_str_entry.data_entry.update_data( (buffer0_bytes, buffer1_bytes) )
		# update the sizedstring entry
		data = struct.pack("<8I", len(buffer1_bytes), 0, 0, 0, 0, 0, 0, 0)
		fdb_sized_str_entry.pointers[0].update_data(data, update_copies=True)

def load_assetpkg(ovl_data, assetpkg_file_path, sized_str_entry):
	with open(assetpkg_file_path, "rb") as stream:
		b = stream.read()
		sized_str_entry.fragments[0].pointers[1].update_data( b + b"\x00", update_copies=True, pad_to=64)
        
def load_lua(ovl_data, lua_file_path, lua_sized_str_entry):
	# read lua
	# inject lua buffer
	# update sized string
	#IMPORTANT: all meta data of the lua except the sized str entries lua size value seems to just be meta data, can be zeroed
	with open(lua_file_path, "rb") as lua_stream:
		# load the new buffer
		buffer_bytes = lua_stream.read()
		# update the buffer
		lua_sized_str_entry.data_entry.update_data( (buffer_bytes,))
		# update the sizedstring entry
	with open(lua_file_path+"meta","rb") as luameta_stream:
		string_data = luameta_stream.read(16)
		print(string_data) #4 uints: size,unknown,hash,zero. only size is used by game.
		frag0_data0 = luameta_stream.read(8)
		print(frag0_data0)
		frag0_data1 = luameta_stream.read(lua_sized_str_entry.fragments[0].pointers[1].data_size)
		print(frag0_data1)
		frag1_data0 = luameta_stream.read(24)
		print(frag1_data0)
		frag1_data1 = luameta_stream.read(lua_sized_str_entry.fragments[1].pointers[1].data_size)
		print(frag1_data1)
		lua_sized_str_entry.pointers[0].update_data(string_data, update_copies=True)
		lua_sized_str_entry.fragments[0].pointers[1].update_data(frag0_data1, update_copies=True)
		lua_sized_str_entry.fragments[1].pointers[1].update_data(frag1_data1, update_copies=True)  
