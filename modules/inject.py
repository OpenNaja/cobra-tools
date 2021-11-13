import tempfile
import shutil
import logging

from modules.formats.BNK import load_wem
from modules.helpers import split_path

from ovl_util import imarray, interaction


def inject(ovl, file_paths, show_temp_files, hack_2k, progress_callback=None):
	logging.info(f"Injecting {len(file_paths)}")
	# write modified version to tmp dir
	tmp_dir = tempfile.mkdtemp("-cobra-png")

	dupecheck = []
	for file_i, file_path in enumerate(file_paths):
		name_ext, name, ext = split_path(file_path)
		logging.info(f"Injecting {name_ext}")
		# check for separated array tiles & flipped channels
		if ext == ".png":
			out_path = imarray.inject_wrapper(file_path, dupecheck, tmp_dir)
			# skip dupes
			if not out_path:
				logging.warning(f"Skipping injection of {file_path}")
			# update the file path to the temp file with flipped channels or rebuilt array
			file_path = out_path
			name_ext, name, ext = split_path(file_path)
		if ext == ".wem":
			bnk_name, wem_name = name.rsplit("_", 1)
			name_ext = bnk_name + ".bnk"
			# load_wem(ovl, file_path, sized_str_entry, bnk_name, wem_name)
	shutil.rmtree(tmp_dir)

	if progress_callback:
		progress_callback("Injection completed!", value=1, vmax=1)


