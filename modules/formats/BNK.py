import os

from generated.formats.bnk import BnkFile
from util import texconv


def write_bnk(archive, sized_str_entry, show_dds, progress_callback, out_dir_func):
	bnk = os.path.splitext(sized_str_entry.name)[0]
	bnk_path = f"{archive.ovl.file_no_ext}_{bnk}_bnk_b.aux"
	if os.path.isfile(bnk_path):
		if "_media_" not in bnk_path:
			print("skipping events bnk", bnk_path)
			return
		print("exporting", bnk_path)

		data = BnkFile()
		data.load(bnk_path)

		# if we want to see the dds, write it to the output dir
		tmp_dir = texconv.make_tmp(archive.dir, show_dds)
		wem_files = data.extract_audio(tmp_dir, bnk)
		texconv.wem_handle(wem_files, archive.dir, show_dds, progress_callback)
	else:
		raise FileNotFoundError(f"BNK / AUX archive expected at {bnk_path}!")