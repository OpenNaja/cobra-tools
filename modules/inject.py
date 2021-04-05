import tempfile
import shutil

from modules.formats.BNK import load_wem
from modules.formats.DDS import load_png, load_dds
from modules.formats.FCT import load_fct
from modules.formats.FDB import load_fdb
from modules.formats.FGM import load_fgm
from modules.formats.LUA import load_lua
from modules.formats.MATCOL import load_materialcollection
from modules.formats.MS2 import load_mdl2
from modules.formats.TXT import load_txt
from modules.formats.VOXELSKIRT import load_voxelskirt
from modules.formats.XMLCONFIG import load_xmlconfig
from modules.helpers import split_path

from ovl_util import imarray


def inject(ovl_data, file_paths, show_temp_files, hack_2k):

	print("\nInjecting...")
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
		sized_str_entry = ovl_data.archives[0].content.get_sized_str_entry(name_ext)
		# do the actual injection, varies per file type
		if ext == ".mdl2":
			mdl2_tups.append((file_path, sized_str_entry))
		if ext == ".fgm":
			load_fgm(ovl_data, file_path, sized_str_entry)
		elif ext == ".png":
			load_png(ovl_data, file_path, sized_str_entry, show_temp_files, hack_2k)
		elif ext == ".dds":
			load_dds(ovl_data, file_path, sized_str_entry, hack_2k)
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
		elif ext == ".userinterfaceicondata":
			load_userinterfaceicondata(ovl_data, file_path, sized_str_entry)
		elif ext == ".voxelskirt":
			load_voxelskirt(ovl_data, file_path, sized_str_entry)

	load_mdl2(ovl_data, mdl2_tups)
	shutil.rmtree(tmp_dir)


def load_assetpkg(ovl_data, assetpkg_file_path, sized_str_entry):
	with open(assetpkg_file_path, "rb") as stream:
		b = stream.read()
		sized_str_entry.fragments[0].pointers[1].update_data( b + b"\x00", update_copies=True, pad_to=64)


def load_userinterfaceicondata(ovl_data, userinterfaceicondata_file_path, sized_str_entry):
	with open(userinterfaceicondata_file_path, "rb") as stream:
		b = stream.read()
		sized_str_entry.fragments[0].pointers[1].update_data( b + b"\x00", update_copies=True)
		len_a = len(b + b"\x00")
	with open(userinterfaceicondata_file_path+"_b", "rb") as stream2:
		bb = stream2.read()      
		sized_str_entry.fragments[1].pointers[1].update_data( bb + b"\x00", update_copies=True, pad_to=64-len_a)

