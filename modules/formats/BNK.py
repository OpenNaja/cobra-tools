import logging
import os
import shutil

from generated.formats.bnk import BnkFile
from modules.formats.BaseFormat import BaseFile


class BnkLoader(BaseFile):
	extension = ".bnk"

	def create(self, file_path):
		# todo - fixme
		# # first uint of the buffer is the size of the data that should be read from the aux file
		# media_buffers = self.data_entry.buffer_datas
		# media_buffers[0] = struct.pack("<I", media.size_for_ovl) + media_buffers[0][4:]
		#
		# if len(media_buffers) > 1:
		# 	logging.info(f"Loaded bnk {media_path} into OVL buffers")
		# 	with open(media_path, "rb") as f:
		# 		media_buffers[1] = f.read()
		# # update the buffer
		# self.data_entry.update_data(media_buffers)
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
		# for aux in self.aux_entries:
		# 	bnkpath = f"{self.ovl.path_no_ext}_{self.file_entry.basename}_bnk_{aux.name.lower()}.aux"
		# 	# grab and update size
		# 	if os.path.isfile(bnkpath):
		# 		aux.size = os.path.getsize(bnkpath)
		# 	else:
		# 		logging.warning(f"Could find {bnkpath} to update .aux file size")
		pass

	def extract(self, out_dir):
		bnk_name = os.path.splitext(self.name)[0]
		# print(self.root_entry.struct_ptr.data)
		out_path = out_dir(self.name)
		out_files = [out_path, ]
		buffer_datas = self.data_entry.buffer_datas
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
		for aux_file in self.aux_entries:
			aux_suffix = aux_file.name.lower()
			if aux_suffix == "b":
				assert bnk.bnk_header.external_b_suffix.lower() == "b"
			elif aux_suffix == "s":
				assert bnk.bnk_header.external_s_suffix.lower() == "s"
			else:
				logging.warning(f"Unknown .aux suffix '{aux_file.name}'")
				continue
			aux_name = f"{self.ovl.basename}_{bnk_name}_bnk_{aux_suffix}.aux"
			aux_path = os.path.join(self.ovl.dir, aux_name)
			if not os.path.isfile(aux_path):
				logging.error(f"External .aux file '{aux_file.name}' was not found at {aux_path}")
			# copy to tmp path so we leave the original file intact
			copy_aux_path = out_dir(aux_name)
			shutil.copy(aux_path, copy_aux_path)
			out_files.append(copy_aux_path)

		# check if an aux 'file' is stored as second buffer
		if len(buffer_datas) > 1:
			# always type b
			aux_name = f"{self.ovl.basename}_{bnk_name}_bnk_b.aux"
			# extract to tmp path
			aux_path = out_dir(aux_name)
			# only internal aux will be in extracted output
			logging.debug(f"Extracted internal .aux to {aux_path}")
			out_files.append(aux_path)
			with open(aux_path, "wb") as f:
				for b in buffer_datas[1:]:
					f.write(b)
		return out_files

