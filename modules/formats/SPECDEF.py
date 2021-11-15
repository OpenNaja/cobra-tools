import logging

from modules.formats.BaseFormat import BaseFile
import struct


class SpecdefLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		ss_pointer = self.sized_str_entry.pointers[0]
		logging.info(f"SPECDEF: {self.sized_str_entry.name}")
		ss_data = struct.unpack("<2H4B", ss_pointer.data)
		logging.info(f"{ss_data}")
		if ss_data[0] == 0:
			logging.info(f"spec is zero ")
		self.sized_str_entry.fragments = self.ovs.frags_from_pointer(ss_pointer, 3, reuse=False)
		attrib_count = ss_data[0]
		conditions = ss_data[2:]
		self.condition_frags = []
		for condition in conditions:
			if condition > 0:
				frag = self.ovs.frags_from_pointer(ss_pointer, 1, reuse=False)[0]
				self.sized_str_entry.fragments.append(frag)
				# logging.debug(frag.pointers[0].data)
				self.condition_frags.append(frag)
			else:
				self.condition_frags.append(None)

		if attrib_count > 0:
			self.sized_str_entry.fragments.extend(self.ovs.frags_from_pointer(self.sized_str_entry.fragments[1].pointers[1], attrib_count, reuse=False))
			self.sized_str_entry.fragments.extend(self.ovs.frags_from_pointer(self.sized_str_entry.fragments[2].pointers[1], attrib_count, reuse=False))

		for cond_frag, cond_count in zip(self.condition_frags, conditions):
			if cond_frag:
				self.sized_str_entry.fragments.extend(self.ovs.frags_from_pointer(cond_frag.pointers[1], cond_count, reuse=False))

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
			attrib_count, flags, name_count, childspec_count, manager_count, script_count = struct.unpack(
				"<2H4B", self.sized_str_entry.pointers[0].data)
			outfile.write(f"Name : {name}\nFlags: {flags:x}\n")

			# debug print all fragments
			# for f in sized_str_entry.fragments:
			#	print(f.pointers[1].data)

			# skip frags here based on counts
			offset = 3 + (name_count > 0) + (childspec_count > 0) + (manager_count > 0) + (script_count > 0)

			if attrib_count > 0:
				outfile.write(f"Attributes:\n")
				lend = len(self.sized_str_entry.fragments[0].pointers[1].data)

				# this frag has padding
				dtypes = struct.unpack(f"<{attrib_count}I", self.sized_str_entry.fragments[0].pointers[1].data[:4 * attrib_count])

				for i in range(0, attrib_count):
					iname = self.sized_str_entry.fragments[offset + i].pointers[1].data.decode().rstrip('\x00')
					dtype = dtypes[i]
					# todo: the tflags structure depends on the dtype value
					# tflags = struct.unpack(f"<{4}I", sized_str_entry.fragments[offset + attrib_count + i].pointers[1].data)
					tflags = self.sized_str_entry.fragments[offset + attrib_count + i].pointers[1].data

					try:
						if dtype == 0:
							# boot on the second byte
							tflags = bool(tflags[1])
						elif dtype == 9:
							# vector3 float
							tflags = struct.unpack("3fI", tflags[:16])
						elif dtype == 12:
							# vector3 float
							tflags = struct.unpack("3f", tflags[:12])
					except:
						logging.warning(f"Unexpected data {tflags} (size: {len(tflags)}) for type {dtype}")
					outstr = f" - Type: {dtype:02} Name: {iname}  Flags: {tflags}"
					# print(outstr)
					outfile.write(outstr + "\n")

				# skip the attrib names and data
				offset += 2 * attrib_count

			if name_count > 0:
				outfile.write(f"Names:\n")
				for i in range(0, name_count):
					iname = self.sized_str_entry.fragments[offset + i].pointers[1].data.decode().rstrip('\x00')
					outstr = f" - Name: {iname}"
					# print(outstr)
					outfile.write(outstr + "\n")

				# skip the names
				offset += name_count

			if childspec_count > 0:
				outfile.write(f"Child Specdefs:\n")
				for i in range(0, childspec_count):
					iname = self.sized_str_entry.fragments[offset + i].pointers[1].data.decode().rstrip('\x00')
					outstr = f" - Specdef: {iname}"
					# print(outstr)
					outfile.write(outstr + "\n")

				# skip the names
				offset += childspec_count

			if manager_count > 0:
				outfile.write(f"Managers:\n")
				for i in range(0, manager_count):
					iname = self.sized_str_entry.fragments[offset + i].pointers[1].data.decode().rstrip('\x00')
					outstr = f" - Manager: {iname}"
					# print(outstr)
					outfile.write(outstr + "\n")

				# skip the names
				offset += manager_count

			if script_count > 0:
				outfile.write(f"Scripts:\n")
				for i in range(0, script_count):
					iname = self.sized_str_entry.fragments[offset + i].pointers[1].data.decode().rstrip('\x00')
					outstr = f" - Script: {iname}"
					# print(outstr)
					outfile.write(outstr + "\n")

		return out_path + ".bin", out_path,
