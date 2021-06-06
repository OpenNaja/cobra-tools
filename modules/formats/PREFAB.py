def prefab_unpack_temp(self, len, data):
	if len % 4 != 0:
		ret = data
	elif len >= 50:
		num = int(len / 4)
		strr = "<" + str(num) + "I"
		ret = struct.unpack(strr, data)
	else:
		num = int(len / 4)
		strr = "<" + str(num) + "I"
		ret = struct.unpack(strr, data)
	return ret


def prefab_unpack_ss(self, len, data):
	num = int(len)
	strr = "<" + str(num) + "B"
	ret = struct.unpack(strr, data)
	return ret


def collect_prefab(self, ss_entry, ad0_fragments):
	ssdata = self.prefab_unpack_ss(len(ss_entry.pointers[0].data), ss_entry.pointers[0].data)
	# if ss_entry.name in ("dingo_game.prefab"+"cassowary_game.prefab"+"red_kangaroo_game.prefab"+"koala_game.prefab"):
	print("\nPREFAB:", ss_entry.name)
	print(ssdata)
	if (ssdata[4] == 0) and (ssdata[6] == 0):
		ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 1)
	elif (ssdata[4] != 0) and (ssdata[6] == 0):
		ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 4)
		f3_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[3].pointers[0].data),
										ss_entry.fragments[3].pointers[0].data)
		f2_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),
										ss_entry.fragments[2].pointers[0].data)
	elif (ssdata[4] == 0) and (ssdata[6] != 0):
		ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 3)
		f3_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),
										ss_entry.fragments[2].pointers[0].data)
		f2_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),
										ss_entry.fragments[2].pointers[0].data)
	elif (ssdata[4] != 0) and (ssdata[6] != 0):
		ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 6)
		f5_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[5].pointers[0].data),
										ss_entry.fragments[5].pointers[0].data)
		f2_d0 = self.prefab_unpack_temp(len(ss_entry.fragments[2].pointers[0].data),
										ss_entry.fragments[2].pointers[0].data)
	else:
		ss_entry.fragments = self.frags_from_pointer(ss_entry.pointers[0], 1)
	gub = []
	fug = []

	if (ssdata[4] != 0) and (ssdata[6] == 0):
		if len(f3_d0) == 8:
			gub = self.frags_from_pointer(ss_entry.pointers[0], 1)
			ss_entry.fragments += gub
		ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[0].pointers[1], ssdata[4])
		if f2_d0[
			2] == 536870911:  # in ("dingo_game.prefab"+"cassowary_game.prefab"+"red_kangaroo_game.prefab"+"koala_game.prefab"):
			ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 18)
			for x in range(34, 52):
				if x == 34:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																				 2)
				elif x == 35:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																				 5)
				elif x == 38:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																				 3)
				elif x == 41:
					ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
				elif x == 43:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																				 2)
				elif x == 45:
					ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
				elif x == 47:
					ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
				elif x == 48:
					ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
				elif x == 50:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																				 2)
				elif x == 51:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																				 2)
		# elif  f2_d0[2] ==127:
		#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 6)
		# elif  f2_d0[2] ==3:
		#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 1)
		# elif  f2_d0[2] ==63:
		#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 5)
		# elif  f2_d0[2] ==1:
		#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 1)
		# elif  f2_d0[2] ==7:
		#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 4)
		# elif  f2_d0[2] ==15:
		#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 3)
		if len(f3_d0) == 8:
			fug += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[4].pointers[1], 5)
			ss_entry.fragments += fug
			gub_d1 = self.prefab_unpack_temp(len(gub[0].pointers[1].data), gub[0].pointers[1].data)
			fug0_d1 = self.prefab_unpack_temp(len(fug[0].pointers[1].data), fug[0].pointers[1].data)
			fug1_d1 = self.prefab_unpack_temp(len(fug[1].pointers[1].data), fug[1].pointers[1].data)
			fug2_d1 = self.prefab_unpack_temp(len(fug[2].pointers[1].data), fug[2].pointers[1].data)
			fug3_d1 = self.prefab_unpack_temp(len(fug[3].pointers[1].data), fug[3].pointers[1].data)
			fug4_d1 = self.prefab_unpack_temp(len(fug[4].pointers[1].data), fug[4].pointers[1].data)
			print("gub", gub_d1)
			print("fug0", fug0_d1)
			print("fug1", fug1_d1)
			print("fug2", fug2_d1)
			print("fug3", fug3_d1)
			print("fug4", fug4_d1)
			if fug0_d1[len(fug0_d1) - 1] == 0:
				ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[1].pointers[1], len(
					fug0_d1) - 1)  # count equal to len(fug[0].pointers[1].data)/4 -1
				ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[2].pointers[1], len(
					fug0_d1) - 1)  # count equal to len(fug[0].pointers[1].data)/4 -1
			else:
				ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[1].pointers[1], len(
					fug0_d1))  # count equal to len(fug[0].pointers[1].data)/4 -1
				ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[2].pointers[1], len(
					fug0_d1))  # count equal to len(fug[0].pointers[1].data)/4 -1
			if gub_d1[0] == 1638405:
				ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 8)
			elif gub_d1[0] == 1966113:
				ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 13)
			elif gub_d1[0] == 1966113:
				ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 13)

	elif (ssdata[4] == 0) and (ssdata[6] != 0):
		if len(f2_d0) == 4:
			gub = self.frags_from_pointer(ss_entry.pointers[0], 1)
			ss_entry.fragments += gub
		ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[1].pointers[1], ssdata[6])


	elif (ssdata[4] != 0) and (ssdata[6] != 0):
		if len(f5_d0) == 4:
			gub = self.frags_from_pointer(ss_entry.pointers[0], 1)
			ss_entry.fragments += gub
		ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[0].pointers[1], ssdata[4])
		if f2_d0[
			2] == 536870911:  # in ("dingo_game.prefab"+"cassowary_game.prefab"+"red_kangaroo_game.prefab"+"koala_game.prefab"):
			ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 18)
			for x in range(34, 52):
				if x == 34:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																				 2)
				elif x == 35:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																				 5)
				elif x == 38:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																				 3)
				elif x == 41:
					ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
				elif x == 43:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																				 2)
				elif x == 45:
					ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
				elif x == 47:
					ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
				elif x == 48:
					ss_entry.fragments += self.frags_from_pointer_equalsb(ss_entry.fragments[x].pointers[1])
				elif x == 50:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																				 2)
				elif x == 51:
					ss_entry.fragments += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[x].pointers[1],
																				 2)
		# elif  f2_d0[2] ==127:
		#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 6)
		# elif  f2_d0[2] ==3:
		#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 1)
		# elif  f2_d0[2] ==63:
		#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 5)
		# elif  f2_d0[2] ==1:
		#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 1)
		# elif  f2_d0[2] ==7:
		#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 4)
		# elif  f2_d0[2] ==15:
		#	ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[2].pointers[1], 3)
		if len(f5_d0) == 4:
			fug += self.frags_from_pointer_equalsb_counts(ss_entry.fragments[6].pointers[1], 5)
			ss_entry.fragments += fug
			gub_d1 = self.prefab_unpack_temp(len(gub[0].pointers[1].data), gub[0].pointers[1].data)
			fug0_d1 = self.prefab_unpack_temp(len(fug[0].pointers[1].data), fug[0].pointers[1].data)
			fug1_d1 = self.prefab_unpack_temp(len(fug[1].pointers[1].data), fug[1].pointers[1].data)
			fug2_d1 = self.prefab_unpack_temp(len(fug[2].pointers[1].data), fug[2].pointers[1].data)
			fug3_d1 = self.prefab_unpack_temp(len(fug[3].pointers[1].data), fug[3].pointers[1].data)
			fug4_d1 = self.prefab_unpack_temp(len(fug[4].pointers[1].data), fug[4].pointers[1].data)
			print("gub", gub_d1)
			print("fug0", fug0_d1)
			print("fug1", fug1_d1)
			print("fug2", fug2_d1)
			print("fug3", fug3_d1)
			print("fug4", fug4_d1)
			if fug0_d1[len(fug0_d1) - 1] == 0:
				ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[1].pointers[1], len(
					fug0_d1) - 1)  # count equal to len(fug[0].pointers[1].data)/4 -1
				ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[2].pointers[1], len(
					fug0_d1) - 1)  # count equal to len(fug[0].pointers[1].data)/4 -1
			else:
				ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[1].pointers[1], len(
					fug0_d1))  # count equal to len(fug[0].pointers[1].data)/4 -1
				ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[2].pointers[1], len(
					fug0_d1))  # count equal to len(fug[0].pointers[1].data)/4 -1
			# if gub_d1[0] == 393217:
			# ss_entry.fragments+=  self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 0) #count equal to len(fug[0].pointers[1].data)/4 -1
			if gub_d1[0] == 1638405:
				ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 8)
			elif gub_d1[0] == 1966113:
				ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 13)
			elif gub_d1[0] == 1966113:
				ss_entry.fragments += self.frags_from_pointer_equalsb_counts(fug[4].pointers[1], 13)

		ss_entry.fragments += self.frags_from_pointer(ss_entry.fragments[4].pointers[1], ssdata[6])

	zzz = 0
	# if ss_entry.name in "dingo_game.prefab":
	for fragg in ss_entry.fragments:
		if zzz < 6:
			print("frag" + str(zzz))
			print(self.prefab_unpack_temp(len(fragg.pointers[0].data), fragg.pointers[0].data))
			print(self.prefab_unpack_temp(len(fragg.pointers[1].data), fragg.pointers[1].data))
			zzz += 1
