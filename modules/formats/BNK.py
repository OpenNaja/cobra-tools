import os

from generated.formats.bnk import BnkFile
from util import texconv


def write_bnk(archive, sized_str_entry, show_temp_files, progress_callback, out_dir_func):
	bnk = os.path.splitext(sized_str_entry.name)[0]
	bnk_path = f"{archive.ovl.file_no_ext}_{bnk}_bnk_b.aux"
	if os.path.isfile(bnk_path):
		if "_media_" not in bnk_path:
			print("skipping events bnk", bnk_path)
			return ()
		print("exporting", bnk_path)

		data = BnkFile()
		data.load(bnk_path)

		# if we want to see the dds, write it to the output dir
		# tmp_dir = texconv.make_tmp(archive.dir, show_temp_files)
		wem_files = data.extract_audio(out_dir_func, bnk)
		processed_files = texconv.wem_handle(wem_files, show_temp_files, progress_callback)
		if show_temp_files:
			return wem_files + processed_files
		else:
			return processed_files
	else:
		raise FileNotFoundError(f"BNK / AUX archive expected at {bnk_path}!")
