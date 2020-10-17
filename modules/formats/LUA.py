from util import texconv


def write_lua(archive, sized_str_entry, out_dir):
	name = sized_str_entry.name
	print("\nWriting",name)

	try:
		buffer_data = sized_str_entry.data_entry.buffer_datas[0]
		print("buffer size",len(buffer_data))
	except:
		print("Found no buffer data for",name)
		buffer_data = b""
	if len(sized_str_entry.fragments) != 2:
		print("must have 2 fragments")
		return
	# write lua
	out_path = out_dir(name)
	print(out_path)
	with open(out_path+".bin", 'wb') as outfile:
		# write the buffer
		outfile.write(buffer_data)
	texconv.bin_to_lua(out_path+".bin")
	with open(out_path+"meta", 'wb') as outfile:
		# write each of the fragments
		# print(sized_str_entry.pointers[0].data)
		outfile.write(sized_str_entry.pointers[0].data)
		for frag in sized_str_entry.fragments:
			# print(frag.pointers[0].data)
			# print(frag.pointers[1].data)
			outfile.write(frag.pointers[0].data)
			outfile.write(frag.pointers[1].data)

	return out_path, out_path+".bin", out_path+"meta"
