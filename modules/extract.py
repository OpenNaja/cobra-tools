from modules.formats.BNK import write_bnk
from modules.formats.MOTIONGRAPHVARS import write_motiongraphvars
from modules.formats.SCALEFORMLANGUAGEDATA import write_scaleformlanguagedata

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


