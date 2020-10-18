import struct
import os
import tempfile
import shutil

from modules.formats.DDS import load_png, load_dds
from modules.formats.FDB import load_fdb
from modules.formats.FGM import load_fgm
from modules.formats.LUA import load_lua
from modules.formats.MATCOL import load_materialcollection
from modules.formats.MS2 import load_mdl2
from modules.util import split_path
from generated.formats.bnk import BnkFile

from util import imarray


def inject(ovl_data, file_paths, show_temp_files, is_2K):

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
			load_png(ovl_data, file_path, sized_str_entry, show_temp_files, is_2K, ovs_sized_str_entry)
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


def load_assetpkg(ovl_data, assetpkg_file_path, sized_str_entry):
	with open(assetpkg_file_path, "rb") as stream:
		b = stream.read()
		sized_str_entry.fragments[0].pointers[1].update_data( b + b"\x00", update_copies=True, pad_to=64)
        
