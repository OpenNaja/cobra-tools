import logging
import os
import struct
import traceback

from generated.formats.bnk import BnkFile, AuxFile
from modules.formats.BaseFormat import BaseFile
from ovl_util.texconv import write_riff_file


class BnkLoader(BaseFile):
	extension = ".bnk"
	child_extensions = (".wav", ".wem", ".ogg")

	def validate_child(self, file_path):
		if "media" in self.file_entry.name:
			return True
		return False

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
			f.write(self.pack_header(b"BNK"))
			f.write(self.sized_str_entry.data_entry.buffer_datas[0])
		logging.debug(f"Num buffers {len(self.sized_str_entry.data_entry.buffer_datas)}")

		try:
			# first read the bnk file which informs of any streams
			bnk = BnkFile()
			bnk.load(out_path)
			print(bnk)
			# extract streamed files
			if bnk.bnk_header.suffixes and self.file_entry.aux_entries:
				# usually both are present
				ext_aux_paths = [(suffix, f"{self.ovl.path_no_ext}_{bnk_name}_bnk_{suffix}.aux") for suffix in bnk.bnk_header.suffixes]
			elif self.file_entry.aux_entries:
				# JWE2 Music_Tour_media has no bnk_header.suffixes but does have aux files
				ext_aux_paths = [(aux.name.lower(), f"{self.ovl.path_no_ext}_{bnk_name}_bnk_{aux.name.lower()}.aux") for aux in self.file_entry.aux_entries]
			else:
				# JWE2 dinos, no aux_entries nor suffixes, aux file is stored as second buffer
				# check for dtype
				suffix = "s" if bnk.bnk_header.stream_infos else "b"
				ext_aux_paths = [(suffix, f"{self.ovl.path_no_ext}_{bnk_name}_bnk_{suffix}.aux") for suffix in (suffix,)]
				for suffix, aux_path in ext_aux_paths:
					# only internal aux will be in extracted output
					logging.debug(f"Extracted internal .aux to {aux_path}")
					out_files.append(aux_path)
					with open(aux_path, "wb") as f:
						for b in self.sized_str_entry.data_entry.buffer_datas[1:]:
							f.write(b)
			for suffix, aux_path in ext_aux_paths:
				if suffix and not os.path.isfile(aux_path):
					logging.warning(f"AUX file expected at {aux_path}!")
				if suffix.lower() == "s":
					with open(aux_path, "rb") as f:
						for i, stream_info in enumerate(bnk.bnk_header.stream_infos):
							if progress_callback:
								progress_callback("Extracting stream", value=i, vmax=len(bnk.bnk_header.stream_infos))
							f.seek(stream_info.offset)
							d = f.read(stream_info.size)
							out_file = write_riff_file(d, out_dir(f"{bnk_name}_bnk_{i}"))
							if out_file:
								out_files.append(out_file)
				elif suffix.lower() in ("b", ""):
					aux = AuxFile()
					aux.load(aux_path)
					out_files.extend(aux.extract_audio(out_dir, bnk_name, progress_callback))
		except BaseException as err:
			logging.error(err)
			traceback.print_exc()
		return out_files
	
	def load(self, wem_file_path):
		logging.info(f"Trying to inject {wem_file_path}")
		# bnk_name = None
		wem_id = None
		bnk = os.path.splitext(self.sized_str_entry.name)[0]
		aux_path = f"{self.ovl.path_no_ext}_{bnk}_bnk_b.aux"
		if os.path.isfile(aux_path):
			# if "_media_" not in aux_path:
			# 	print("skipping events bnk", aux_path)
			# 	return
	
			data = AuxFile()
			data.load(aux_path)
			data.inject_audio(wem_file_path, wem_id)
			data.save(aux_path)
			events = AuxFile()
			ss = self.sized_str_entry.name.rsplit("_", 1)[0]
			eventspath = f"{self.ovl.path_no_ext}_{ss}_events_bnk_b.aux"
			events.load(eventspath)
			# print(events)
			events.inject_hirc(wem_file_path, wem_id)
			events.save(eventspath)
	
			# first uint of the buffer is the size of the data that should be read from the aux file
			buffers = self.sized_str_entry.data_entry.buffer_datas
			buffers[0] = struct.pack("<I", data.size_for_ovl) + buffers[0][4:]
			# update the buffer
			self.sized_str_entry.data_entry.update_data(buffers)
			logging.info(f"Injected {wem_file_path} {wem_id}")
