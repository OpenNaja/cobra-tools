def collect_wmeta(self, ss_entry, address_0_fragments):
	print("\nwmeta:", ss_entry.name)
	return
	# Sized string initpos = position of first fragment
	ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 1)
	f = ss_entry.fragments[0]
	# print(f.pointers[0].data, f.pointers[0].address, len(f.pointers[0].data), len(ss_entry.pointers[0].data))
	_, count = struct.unpack("<2Q", ss_entry.pointers[0].data)
	print(count)
	if self.ovl.basename.lower() == "main.ovl":
		print("Debug mode for sound")
		print()
		for frag in self.fragments:
			if 4233228 <= frag.pointers[1].address < 4234772 or 2257932 <= frag.pointers[1].address < 4219472:
				# ss_entry.fragments.append(frag)
				frag.pointers[1].strip_zstring_padding()
				frag.name = frag.pointers[1].data[:-1]  # .decode()

	ss_entry.bnks = []
	# for bnk_index in range(count):
	# ss_entry.bnks = self.frags_from_pointer(ss_entry.fragments[0].pointers[1], 4*count)
	# ss_entry.fragments.extend(ss_entry.bnks)
	# for i in range(count):
	# 	fs = ss_entry.bnks[i*4: i*4+4]
	# 	for f in fs[:3]:
	# 		f.pointers[1].strip_zstring_padding()
	# 	print(fs[0].pointers[1].data)
	# 	print(fs[1].pointers[1].data)
	# 	for f in fs:
	# 		print(f.pointers[0].data)
	for i in range(count):
		print(f"\n\nbnk {i}")
		bnk = self.frags_accumulate(ss_entry.fragments[0].pointers[1], 112, address_0_fragments)
		# if bnk[3].pointers[0].data_size == 64:
		# 	bnk.extend(self.frags_from_pointer(ss_entry.fragments[0].pointers[1], 1))
		for f in bnk[:3]:
			f.pointers[1].strip_zstring_padding()
			print(f.pointers[1].data)
			f.name = f.pointers[1].data[:-1]  # .decode()
		# 	 if it's a media bnk like for the dinos, it has a pointer pointing to the start of the files that belong to this
		if len(bnk) > 3:
			b = bnk[3].pointers[0].data
			# this points to the child data
			ptr = bnk[3].pointers[1]
			if len(b) == 56:
				d = struct.unpack("<6Q2I", b)
				media_count = d[1]
				maybe_hash = d[6]
				print(f.name, media_count, maybe_hash, ptr.address)
				bk_frags = self.frags_from_pointer(ptr, media_count * 3)
				for j in range(media_count):
					z = bk_frags[j * 3: j * 3 + 3]
					for f in z:
						f.pointers[1].strip_zstring_padding()
						print(f.pointers[1].data)
		ss_entry.bnks.append(bnk)

# ss_entry.fragments.extend(bnk)

# ss_entry.vars = self.frags_from_pointer(ss_entry.fragments[0].pointers[1], count)
# # pointers[1].data is the name
# for var in ss_entry.vars:
# 	var.pointers[1].strip_zstring_padding()
# # The last fragment has padding that may be junk data to pad the size of the name block to multiples of 64
# ss_entry.fragments.extend(ss_entry.vars)
