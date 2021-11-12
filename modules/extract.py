import struct
import os
import traceback
import sys

import ovl_util.interaction
import modules.formats.shared
from modules.formats.BANI import write_banis, write_bani
from modules.formats.BNK import write_bnk
from modules.formats.FCT import write_fct
from modules.formats.MANI import write_manis
from modules.formats.MOTIONGRAPHVARS import write_motiongraphvars
from modules.formats.SCALEFORMLANGUAGEDATA import write_scaleformlanguagedata
from ovl_util import widgets

IGNORE_TYPES = (".mani", ".mdl2", ".texturestream", ".datastreams", ".model2stream")


def extract_kernel(ovl, entry, out_dir_func, show_temp_files, progress_callback):
	# automatically call the extract function, if it has been defined
	namespace = sys.modules[__name__]
	func_name = f"write_{entry.ext[1:]}"
	func = getattr(namespace, func_name, None)
	if func:
		return func(ovl, entry, out_dir_func, show_temp_files, progress_callback)
	else:
		raise AttributeError(f"No function to export {entry.name}")


def get_files(ovl, only_names, only_types, skip_files):
	extract_files = []
	for file in ovl.files:
		# for batch operations, only export those that we need
		if only_types and file.ext not in only_types:
			skip_files.append(file.name)
			continue
		if only_names and file.name not in only_names:
			skip_files.append(file.name)
			continue
		# ignore types in the count that we export from inside other type exporters
		if file.ext in IGNORE_TYPES:
			continue
		extract_files.append(file)
	return extract_files


def write_gfx(ovl, sized_str_entry, out_dir, show_temp_files, progress_callback):
	name = sized_str_entry.name
	print(f"\nWriting {name}")

	out_path = out_dir(name)
	buffers = sized_str_entry.data_entry.buffer_datas
	with open(out_path, 'wb') as outfile:
		outfile.write(sized_str_entry.pointers[0].data)
		for buff in buffers:
			outfile.write(buff)
	return out_path,


