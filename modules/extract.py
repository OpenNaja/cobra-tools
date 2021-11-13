import struct
import os
import traceback
import sys

import ovl_util.interaction
import modules.formats.shared
from modules.formats.BNK import write_bnk
from modules.formats.MANI import write_manis
from modules.formats.MOTIONGRAPHVARS import write_motiongraphvars
from modules.formats.SCALEFORMLANGUAGEDATA import write_scaleformlanguagedata
from ovl_util import widgets


def extract_kernel(ovl, entry, out_dir_func, show_temp_files, progress_callback):
	# automatically call the extract function, if it has been defined
	namespace = sys.modules[__name__]
	func_name = f"write_{entry.ext[1:]}"
	func = getattr(namespace, func_name, None)
	if func:
		return func(ovl, entry, out_dir_func, show_temp_files, progress_callback)
	else:
		raise AttributeError(f"No function to export {entry.name}")


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


