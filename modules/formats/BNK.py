import logging
import os
import struct
import traceback

from generated.formats.bnk import BnkFile, AuxFile
from modules.formats.BaseFormat import BaseFile
from ovl_util.texconv import write_riff_file


class BnkLoader(BaseFile):
	extension = ".bnk"
	# child_extensions = (".aux",)

	def validate_child(self, file_path):
		return True
		# # only accept audio files on media bnks
		# if "media" in self.file_entry.name:
		# 	return True
		# return False

	def create(self):
		pass

	def collect(self):
		self.assign_ss_entry()
			
	def extract(self, out_dir, show_temp_files, progress_callback):
		bnk_name = os.path.splitext(self.sized_str_entry.name)[0]
		# print(self.sized_str_entry.pointers[0].data)
		out_path = out_dir(self.sized_str_entry.name)
		out_files = [out_path, ]
		buffer_datas = self.sized_str_entry.data_entry.buffer_datas
		with open(out_path, "wb") as f:
			f.write(self.pack_header(b"BNK"))
			f.write(buffer_datas[0])
		# logging.debug(f"Num buffers {len(buffer_datas)}")
		# for i, buffer_data in enumerate(buffer_datas):
		# 	logging.debug(f"buffer {i}, size {len(buffer_data)}")

		# first read the bnk file which informs of any streams
		bnk = BnkFile()
		bnk.load(out_path)
		print(bnk)
		# ensure that aux files are where they should be
		for aux_file in self.file_entry.aux_entries:
			print(aux_file)
			if aux_file.name.lower() == "b":
				assert bnk.bnk_header.external_b_suffix.lower() == "b"
			elif aux_file.name.lower() == "s":
				assert bnk.bnk_header.external_s_suffix.lower() == "s"
			else:
				logging.warning(f"Unknown .aux suffix '{aux_file.name}'")
				continue
			bnk_path = os.path.join(self.ovl.dir, f"{self.ovl.basename}_{bnk_name}_bnk_b.aux")
			if not os.path.isfile(bnk_path):
				logging.warning(f"External .aux file '{aux_file.name}' is missing")

		# check if an aux 'file' is stored as second buffer
		if len(buffer_datas) > 1:
			# always type b
			aux_path = f"{self.ovl.path_no_ext}_{bnk_name}_bnk_b.aux"
			# only internal aux will be in extracted output
			logging.debug(f"Extracted internal .aux to {aux_path}")
			out_files.append(aux_path)
			with open(aux_path, "wb") as f:
				for b in buffer_datas[1:]:
					f.write(b)
		return out_files
	
	def load(self, bnk_file_path):
		pass

