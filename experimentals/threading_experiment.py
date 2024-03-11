gui.returns = 0
num_threads = 6
batch_size = len(ovl_files) // num_threads
offset = 0


def update_bump():
	print("update_bump")
	gui.returns += 1
	if gui.returns == num_threads:
		print("update_search")
		gui.search_files.emit((search_str, res))


for th in range(num_threads):
	slice_ovl_files = ovl_files[offset: offset + batch_size]
	offset += batch_size
	gui.run_in_threadpool(search_ovl_files_list, (update_bump,), gui, slice_ovl_files, search_str, start_dir, res)

# gui.run_in_threadpool(search_ovl_files_list, (update_search, ), gui, ovl_files, search_str, start_dir, res)
