from generated.formats.voxelskirt import VoxelskirtFile
from modules.formats.shared import pack_header


def write_voxelskirt(archive, sized_str_entry, out_dir):
	name = sized_str_entry.name
	print(f"\nWriting {name}")

	ovl_header = pack_header(archive, b"VOXE")
	out_path = out_dir(name)
	buffers = sized_str_entry.data_entry.buffer_datas
	# write voxelskirt
	with open(out_path, 'wb') as outfile:
		# write the sized str and buffers
		# print(sized_str_entry.pointers[0].data)
		outfile.write(ovl_header)
		outfile.write(sized_str_entry.pointers[0].data)
		for buff in buffers:
			outfile.write(buff)
	return out_path,


def load_voxelskirt(ovl_data, file_path, sized_str_entry):
	vox = VoxelskirtFile()
	ss_bytes, buffer_bytes = vox.get_structs(file_path)
	sized_str_entry.data_entry.update_data((buffer_bytes,))
	sized_str_entry.pointers[0].update_data(ss_bytes, update_copies=True)

