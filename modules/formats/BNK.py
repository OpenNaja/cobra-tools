import logging
import os

from generated.formats.bnk import BnkFile
from modules.formats.BaseFormat import BaseFile


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
		# todo - fixme
		# # first uint of the buffer is the size of the data that should be read from the aux file
		# media_buffers = self.root_entry.data_entry.buffer_datas
		# media_buffers[0] = struct.pack("<I", media.size_for_ovl) + media_buffers[0][4:]
		#
		# if len(media_buffers) > 1:
		# 	logging.info(f"Loaded bnk {media_path} into OVL buffers")
		# 	with open(media_path, "rb") as f:
		# 		media_buffers[1] = f.read()
		# # update the buffer
		# self.root_entry.data_entry.update_data(media_buffers)
		#
		# # get events bnk for internal files
		# if not self.file_entry.aux_entries:
		# 	events_ss, archive = self.ovl.get_root_entry(f"{events_bnk}.bnk")
		# 	if events_ss:
		# 		events_buffers = events_ss.data_entry.buffer_datas
		# 		events_buffers[0] = struct.pack("<I", events.size_for_ovl) + events_buffers[0][4:]
		#
		# 		logging.info(f"Loaded bnk {events_path} into OVL buffers")
		# 		with open(events_path, "rb") as f:
		# 			events_buffers[1] = f.read()
		# 		events_ss.data_entry.update_data(events_buffers)
		# 	else:
		# 		logging.warning(f"Could not find {events_bnk}.bnk in OVL")
		pass

	def collect(self):
		self.assign_root_entry()
			
	def extract(self, out_dir, show_temp_files, progress_callback):
		bnk_name = os.path.splitext(self.root_entry.name)[0]
		# print(self.root_entry.struct_ptr.data)
		out_path = out_dir(self.root_entry.name)
		out_files = [out_path, ]
		buffer_datas = self.root_entry.data_entry.buffer_datas
		with open(out_path, "wb") as f:
			f.write(self.pack_header(b"BNK"))
			f.write(buffer_datas[0])
		# logging.debug(f"Num buffers {len(buffer_datas)}")
		# for i, buffer_data in enumerate(buffer_datas):
		# 	logging.debug(f"buffer {i}, size {len(buffer_data)}")

		# first read the bnk file which informs of any streams
		bnk = BnkFile()
		bnk.load(out_path)
		# print(bnk)
		# ensure that aux files are where they should be
		for aux_file in self.file_entry.aux_entries:
			# print(aux_file)
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

