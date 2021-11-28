import logging
import os
import struct
import traceback

from generated.formats.bnk import BnkFile, AuxFile
from generated.formats.ovl_base.versions import is_jwe2, is_pz16
from modules.formats.BaseFormat import BaseFile
from ovl_util import texconv


class BnkLoader(BaseFile):

	def create(self):
		pass

	def collect(self):
		self.assign_ss_entry()
			
	def extract(self, out_dir, show_temp_files, progress_callback):
		for aux_file in self.file_entry.aux_entries:
			print(aux_file)
		bnk_name = os.path.splitext(self.sized_str_entry.name)[0]
		# print(self.sized_str_entry.pointers[0].address, self.sized_str_entry.pointers[0].data)
		# print(self.sized_str_entry.data_entry.buffer_datas)
		out_path = out_dir(self.sized_str_entry.name)
		out_files = [out_path, ]
		with open(out_path, "wb") as f:
			f.write(self.sized_str_entry.data_entry.buffer_datas[0])
		# for i in range(1, len(self.sized_str_entry.data_entry.buffer_datas)):
		# 	buffer_path = out_path+str(i)
		# 	out_files.append(buffer_path)
		# 	with open(buffer_path, "wb") as f:
		# 		f.write(self.sized_str_entry.data_entry.buffer_datas[i])
		logging.debug(f"Num buffers {len(self.sized_str_entry.data_entry.buffer_datas)}")
	
		wem_files = []
		try:
			# first read the bnk file which informs of any streams
			bnk = BnkFile()
			bnk.load(out_path)
			print(bnk)
			# extract streamed files
			for ext in bnk.extensions:
				aux_path = f"{self.ovl.file_no_ext}_{bnk_name}_bnk_{ext}.aux"
				if not self.file_entry.aux_entries:
					with open(aux_path, "wb") as f:
						for b in self.sized_str_entry.data_entry.buffer_datas[1:]:
							f.write(b)
				# if ext and not os.path.isfile(aux_path):
					# raise FileNotFoundError(f"AUX file expected at {aux_path}!")
				if ext.lower() == "s":
					with open(aux_path, "rb") as f:
						for i, stream_info in enumerate(bnk.stream_infos):
							offset, size, unk = stream_info
							f.seek(offset)
							d = f.read(size)
							wem_path = out_dir(f"{bnk_name}_bnk_{i}.wem")
							with open(wem_path, "wb") as wem:
								wem.write(d)
							wem_files.append(wem_path)
				elif ext.lower() in ("b", ""):
					aux = AuxFile()
					aux.load(aux_path)
					wem_files.extend(aux.extract_audio(out_dir, bnk_name))
				if is_jwe2(self.ovl):
					break
		except BaseException as err:
			logging.error(err)
			traceback.print_exc()
		processed_files = texconv.wem_handle(wem_files, show_temp_files, progress_callback)
		if show_temp_files:
			out_files.append(aux_path)
			return out_files + wem_files + processed_files
		else:
			return out_files + processed_files
	
	def load(self, wem_file_path):
		# todo - resolve and get these
		bnk_name = None
		wem_id = None
		bnk = os.path.splitext(self.sized_str_entry.name)[0]
		aux_path = f"{self.ovl.file_no_ext}_{bnk}_bnk_b.aux"
		if os.path.isfile(aux_path):
			if "_media_" not in aux_path:
				print("skipping events bnk", aux_path)
				return
	
			data = AuxFile()
			data.load(aux_path)
			data.inject_audio(wem_file_path, wem_id)
			data.save(aux_path)
			events = AuxFile()
			ss = self.sized_str_entry.name.rsplit("_", 1)[0]
			eventspath = f"{self.ovl.file_no_ext}_{ss}_events_bnk_b.aux"
			events.load(eventspath)
			print(events)
			events.inject_hirc(wem_file_path, wem_id)
			events.save(eventspath)
	
			# first uint of the buffer is the size of the data that should be read from the aux file
			buffers = self.sized_str_entry.data_entry.buffer_datas
			buffers[0] = struct.pack("<I", data.size_for_ovl) + buffers[0][4:]
			# update the buffer
			self.sized_str_entry.data_entry.update_data(buffers)
