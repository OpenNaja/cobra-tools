import logging
import os
import shutil
from io import BytesIO

from generated.formats.bnk import BnkFile
from generated.formats.bnk.compounds.BnkBufferData import BnkBufferData
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
		pass

	def get_aux_size(self, aux_basename):
		bnkpath = f"{self.ovl.path_no_ext}_{self.basename}_bnk_{aux_basename.lower()}.aux"
		if os.path.isfile(bnkpath):
			return os.path.getsize(bnkpath)
		else:
			logging.warning(f"Could not find {bnkpath} to update .aux file size")
			return 0

	def extract(self, out_dir):
		bnk_name = os.path.splitext(self.name)[0]
		out_path = out_dir(self.name)
		out_files = [out_path, ]
		buffer_datas = self.data_entry.buffer_datas
		main_buffer = buffer_datas[0]
		with open(out_path, "wb") as f:
			f.write(self.pack_header(b"BNK"))
			f.write(main_buffer)

		# only needed to assert validity of aux stream mapping
		# with BytesIO(main_buffer) as stream:
		# 	bnk_header = BnkBufferData.from_stream(stream, self.context)

		# ensure that aux files are where they should be
		for aux_suffix in self.aux_entries:
			aux_suffix = aux_suffix.lower()
			# if aux_suffix == "b":
			# 	assert bnk_header.external_b_suffix.lower() == "b"
			# elif aux_suffix == "s":
			# 	assert bnk_header.external_s_suffix.lower() == "s"
			# else:
			# 	logging.warning(f"Unknown .aux suffix '{aux_suffix}'")
			# 	continue
			aux_name = f"{self.ovl.basename}_{bnk_name}_bnk_{aux_suffix}.aux"
			aux_path = os.path.join(self.ovl.dir, aux_name)
			if not os.path.isfile(aux_path):
				logging.error(f"External .aux file '{aux_suffix}' was not found at {aux_path}")
			# copy to tmp path so we leave the original file intact
			copy_aux_path = out_dir(aux_name)
			shutil.copy(aux_path, copy_aux_path)
			out_files.append(copy_aux_path)

		# check if an aux 'file' is stored as second buffer in ovl
		if len(buffer_datas) > 1:
			# always type b
			aux_name = f"{self.ovl.basename}_{bnk_name}_bnk_b.aux"
			# extract to tmp path
			aux_path = out_dir(aux_name)
			logging.debug(f"Extracted internal .aux to {aux_path}")
			out_files.append(aux_path)
			with open(aux_path, "wb") as f:
				for b in buffer_datas[1:]:
					f.write(b)
		return out_files

