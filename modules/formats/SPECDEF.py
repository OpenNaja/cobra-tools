from modules.formats.BaseFormat import BaseFile
import struct


class SpecdefLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		ss_pointer = self.sized_str_entry.pointers[0]
		print("\nSPECDEF:", self.sized_str_entry.name)
		ss_data = struct.unpack("<2H4B", ss_pointer.data)
		if ss_data[0] == 0:
			print("spec is zero ", ss_data[0])
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(ss_pointer, 3)
		if ss_data[2] > 0:
			data2_frag = self.ovs.frags_from_pointer(ss_pointer, 1)
			self.sized_str_entry.fragments.extend(data2_frag)
		if ss_data[3] > 0:
			data3_frag = self.ovs.frags_from_pointer(ss_pointer, 1)
			self.sized_str_entry.fragments.extend(data3_frag)
		if ss_data[4] > 0:
			data4_frag = self.ovs.frags_from_pointer(ss_pointer, 1)
			self.sized_str_entry.fragments.extend(data4_frag)
		if ss_data[5] > 0:
			data5_frag = self.ovs.frags_from_pointer(ss_pointer, 1)
			self.sized_str_entry.fragments.extend(data5_frag)

		if ss_data[0] > 0:
			self.sized_str_entry.fragments.extend(self.ovs.frags_from_pointer(self.sized_str_entry.fragments[1].pointers[1], ss_data[0]))
			self.sized_str_entry.fragments.extend(self.ovs.frags_from_pointer(self.sized_str_entry.fragments[2].pointers[1], ss_data[0]))

		if ss_data[2] > 0:
			self.sized_str_entry.fragments.extend(self.ovs.frags_from_pointer(data2_frag[0].pointers[1], ss_data[2]))
		if ss_data[3] > 0:
			self.sized_str_entry.fragments.extend(self.ovs.frags_from_pointer(data3_frag[0].pointers[1], ss_data[3]))
		if ss_data[4] > 0:
			self.sized_str_entry.fragments.extend(self.ovs.frags_from_pointer(data4_frag[0].pointers[1], ss_data[4]))
		if ss_data[5] > 0:
			self.sized_str_entry.fragments.extend(self.ovs.frags_from_pointer(data5_frag[0].pointers[1], ss_data[5]))

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		print(f"\nWriting {name}")

		ovl_header = self.pack_header(b"SPEC")
		out_path = out_dir(name)

		# save .bin data
		with open(out_path + ".bin", 'wb') as outfile:
			print("Exporting binary specdef file")
			outfile.write(ovl_header)
			outfile.write(self.sized_str_entry.pointers[0].data)
			for f in self.sized_str_entry.fragments:
				outfile.write(f.pointers[1].data)
			outfile.close()

		# save .text file
		with open(out_path, 'w') as outfile:
			print("Exporting text specdef file")
			attribcount, flags, namecount, childspeccount, managercount, scriptcount = struct.unpack("<2H4B",
																									 self.sized_str_entry.pointers[
																										 0].data)
			outfile.write(f"Name : {name}\nFlags: {flags:x}\n")

			# debug print all fragments
			# for f in sized_str_entry.fragments:
			#	print(f.pointers[1].data)

			# skip frags here based on counts
			offset = 3 + (namecount > 0) + (childspeccount > 0) + (managercount > 0) + (scriptcount > 0)

			if attribcount > 0:
				outfile.write(f"Attributes:\n")
				lend = len(self.sized_str_entry.fragments[0].pointers[1].data)

				# this frag has padding
				dtypes = struct.unpack(f"<{attribcount}I", self.sized_str_entry.fragments[0].pointers[1].data[:4 * attribcount])

				for i in range(0, attribcount):
					iname = self.sized_str_entry.fragments[offset + i].pointers[1].data.decode().rstrip('\x00')
					dtype = dtypes[i]
					# todo: the tflags structure depends on the dtype value
					# tflags = struct.unpack(f"<{4}I", sized_str_entry.fragments[offset + attribcount + i].pointers[1].data)
					tflags = self.sized_str_entry.fragments[offset + attribcount + i].pointers[1].data
					outstr = f" - Type: {dtype:02} Name: {iname}  Flags: {tflags}"
					# print(outstr)
					outfile.write(outstr + "\n")

				# skip the attrib names and data
				offset += 2 * attribcount

			if namecount > 0:
				outfile.write(f"Names:\n")
				for i in range(0, namecount):
					iname = self.sized_str_entry.fragments[offset + i].pointers[1].data.decode().rstrip('\x00')
					outstr = f" - Name: {iname}"
					# print(outstr)
					outfile.write(outstr + "\n")

				# skip the names
				offset += namecount

			if childspeccount > 0:
				outfile.write(f"Child Specdefs:\n")
				for i in range(0, childspeccount):
					iname = self.sized_str_entry.fragments[offset + i].pointers[1].data.decode().rstrip('\x00')
					outstr = f" - Specdef: {iname}"
					# print(outstr)
					outfile.write(outstr + "\n")

				# skip the names
				offset += childspeccount

			if managercount > 0:
				outfile.write(f"Managers:\n")
				for i in range(0, managercount):
					iname = self.sized_str_entry.fragments[offset + i].pointers[1].data.decode().rstrip('\x00')
					outstr = f" - Manager: {iname}"
					# print(outstr)
					outfile.write(outstr + "\n")

				# skip the names
				offset += managercount

			if scriptcount > 0:
				outfile.write(f"Scripts:\n")
				for i in range(0, scriptcount):
					iname = self.sized_str_entry.fragments[offset + i].pointers[1].data.decode().rstrip('\x00')
					outstr = f" - Script: {iname}"
					# print(outstr)
					outfile.write(outstr + "\n")

			outfile.close()

		return out_path + ".bin", out_path,
