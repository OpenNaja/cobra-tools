import os
import struct

from generated.formats.bnk import BnkFile, AuxFile
from util import texconv


def write_bnk(archive, entry, out_dir_func, show_temp_files, progress_callback):
	bnk_name = os.path.splitext(entry.name)[0]
	# print(entry.pointers[0].address, entry.pointers[0].data)
	# print(entry.data_entry.buffer_datas)
	out_path = out_dir_func(entry.name)
	with open(out_path, "wb") as f:
		f.write(entry.data_entry.buffer_datas[0])
	# first read the bnk file which informs of any streams
	bnk = BnkFile()
	bnk.load(out_path)
	# print(bnk)
	wem_files = []
	# extract streamed files
	for ext in bnk.extensions:
		aux_path = f"{archive.ovl.file_no_ext}_{bnk_name}_bnk_{ext}.aux"
		if ext and not os.path.isfile(aux_path):
			raise FileNotFoundError(f"AUX file expected at {aux_path}!")
		if ext.lower() == "s":
			with open(aux_path, "rb") as f:
				for i, stream_info in enumerate(bnk.stream_infos):
					offset, size, unk = stream_info
					f.seek(offset)
					d = f.read(size)
					wem_path = out_dir_func(f"{bnk_name}_bnk_{i}.wem")
					with open(wem_path, "wb") as wem:
						wem.write(d)
					wem_files.append(wem_path)
		elif ext.lower() == "b":
			aux = AuxFile()
			aux.load(aux_path)
			wem_files.extend(aux.extract_audio(out_dir_func, bnk_name))

	processed_files = texconv.wem_handle(wem_files, show_temp_files, progress_callback)
	if show_temp_files:
		return [out_path, ] + wem_files + processed_files
	else:
		return [out_path, ] + processed_files


def load_wem(ovl, wem_file_path, sized_str_entry, bnk_name, wem_id):
	bnk = os.path.splitext(sized_str_entry.name)[0]
	aux_path = f"{ovl.file_no_ext}_{bnk}_bnk_b.aux"
	if os.path.isfile(aux_path):
		if "_media_" not in aux_path:
			print("skipping events bnk", aux_path)
			return

		data = AuxFile()
		data.load(aux_path)
		data.inject_audio(wem_file_path, wem_id)
		data.save(aux_path)
		events = AuxFile()
		ss = sized_str_entry.name.rsplit("_", 1)[0]
		eventspath = f"{ovl.file_no_ext}_{ss}_events_bnk_b.aux"
		events.load(eventspath)
		print(events)
		events.inject_hirc(wem_file_path, wem_id)
		events.save(eventspath)

		# first uint of the buffer is the size of the data that should be read from the aux file
		buffers = sized_str_entry.data_entry.buffer_datas
		buffers[0] = struct.pack("<I", data.size_for_ovl) + buffers[0][4:]
		# update the buffer
		sized_str_entry.data_entry.update_data(buffers)
