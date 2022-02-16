import logging
import struct
import traceback

from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?

from modules.helpers import as_bytes


class AnimalresearchunlockssettingsLoader(BaseFile):

	def create(self):
		xml = self._get_data(self.file_entry.path)
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		# type 4 throughout
		root_f = self.create_fragments(self.sized_str_entry, 1)[0]
		array_bytes = b""
		data = []
		for level in xml:
			# ptr to start always exists
			f = self.create_fragments(self.sized_str_entry, 1)[0]
			# print(level.unlockables)
			followups = level.find('followups')
			unlockables = level.find('unlockables')
			# 40 bytes
			array_bytes += struct.pack("<5Q", 0, 0, len(followups), 0, len(unlockables))
			# only create these pointers if the arrays exist
			# we create the arrays later once we have written the main array
			f_followups = self.create_fragments(self.sized_str_entry, bool(followups))
			f_unlockables = self.create_fragments(self.sized_str_entry, bool(unlockables))
			data.append((f, f_followups, f_unlockables, level.attrib["name"], followups, unlockables))

		# write array data
		self.write_to_pool(root_f.pointers[1], 4, array_bytes)

		# now the levels
		offset = 0
		for f, f_followup, f_unlockable, name, followups, unlockables in data:
			self.ptr_relative(f.pointers[0], root_f.pointers[1], offset)
			self.write_to_pool(f.pointers[1], 2, as_bytes(name))
			if len(followups):
				f_followups = self.create_fragments(self.sized_str_entry, len(followups))
				for f_u, f_e in zip(f_followups, followups):
					self.write_to_pool(f_u.pointers[0], 4, b"\x00" * 16)
					self.write_to_pool(f_u.pointers[1], 2, as_bytes(f_e.attrib["name"]))
				# make level's ptr point to start of followups region
				f_u_ptr = f_followup[0]
				self.ptr_relative(f_u_ptr.pointers[0], root_f.pointers[1], offset+8)
				self.ptr_relative(f_u_ptr.pointers[1], f_followups[0].pointers[0])
			# point to unlockables
			if len(unlockables):
				f_unlockables = self.create_fragments(self.sized_str_entry, len(unlockables))
				for f_u, f_e in zip(f_unlockables, unlockables):
					self.write_to_pool(f_u.pointers[0], 4, b"\x00" * 8)
					self.write_to_pool(f_u.pointers[1], 2, as_bytes(f_e.attrib["name"]))
				# make level's ptr point to start of unlockables region
				f_u_ptr = f_unlockable[0]
				self.ptr_relative(f_u_ptr.pointers[0], root_f.pointers[1], offset+24)
				self.ptr_relative(f_u_ptr.pointers[1], f_unlockables[0].pointers[0])
			offset += 40

		# write the basics - array count + its data
		self.write_to_pool(self.sized_str_entry.pointers[0], 4, struct.pack("<2Q", 0, len(xml)))
		self.ptr_relative(root_f.pointers[0], self.sized_str_entry.pointers[0])

	def collect(self):
		self.assign_ss_entry()
		ss_pointer = self.sized_str_entry.pointers[0]
		_, count = struct.unpack("<QQ", ss_pointer.data)
		# logging.debug(ss_pointer.data)
		# logging.debug(f"{self.file_entry.name} has {count} entries")
		self.assign_fixed_frags(1)
		root_f = self.sized_str_entry.fragments[0]
		# logging.debug(root_f)
		ptr1 = root_f.pointers[1]

		entry_size = 40
		out_frags, array_data = self.collect_array(ptr1, count, entry_size)
		self.sized_str_entry.fragments.extend(out_frags)
		self.frag_data_pairs = []
		for i in range(count):
			x = i * entry_size
			# level x
			# has children x + 8
			# num children x + 24
			frags_entry = self.get_frags_between(out_frags, ptr1.data_offset + x, ptr1.data_offset + x+entry_size)
			entry_bytes = array_data[x:x+entry_size]
			self.frag_data_pairs.append((frags_entry, entry_bytes))
			# rel_offsets = [f.pointers[0].data_offset-x for f in frags_entry]
			data = struct.unpack("<QQQQQ", entry_bytes)
			next_level = data[2]
			children_count = data[4]
			if not frags_entry:
				continue
			level_frag = frags_entry[0]
			level_frag.children = []
			level_frag.next = []
			# logging.debug(f"level_frag: {level_frag.pointers[1].data}")
			if children_count:
				ptr_frag = frags_entry[2]
				level_frag.children = self.ovs.frags_from_pointer(ptr_frag.pointers[1], children_count)
				# for f in level_frag.children:
				# 	logging.debug(f"child: {f.pointers[1].data}")
			if next_level:
				ptr_frag = frags_entry[1]
				level_frag.next = self.ovs.frags_from_pointer(ptr_frag.pointers[1], next_level)
				# for f in level_frag.next:
				# 	logging.debug(f"next: {f.pointers[1].data}")
			self.sized_str_entry.fragments.extend(level_frag.children)
			self.sized_str_entry.fragments.extend(level_frag.next)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		xmldata = ET.Element('AnimalResearchUnlockSettings')
		for frags, entry_bytes in self.frag_data_pairs:
			layer = ET.SubElement(xmldata, 'level')
			if not frags:
				continue
			level = frags[0]
			layer.set('name', self.get_zstr(level.pointers[1].data))
			unlockables = ET.SubElement(layer, 'unlockables')
			for unlockable_f in level.children:
				unlockable = ET.SubElement(unlockables, 'unlockable')
				unlockable.set('name', self.get_zstr(unlockable_f.pointers[1].data))
			followups = ET.SubElement(layer, 'followups')
			for next_f in level.next:
				followup = ET.SubElement(followups, 'followup')
				followup.set('name', self.get_zstr(next_f.pointers[1].data))
		self.write_xml(out_path, xmldata)
		return out_path,

	def _get_data(self, file_path):
		return self.load_xml(file_path)


class AnimalresearchstartunlockedssettingsLoader(BaseFile):

	def create(self):
		pass

	def collect(self):
		self.assign_ss_entry()
		ss_pointer = self.sized_str_entry.pointers[0]
		_, count = struct.unpack("<QQ", ss_pointer.data)
		# logging.debug(ss_pointer.data)
		# logging.debug(f"{self.file_entry.name} has {count} entries")
		self.frag_data_pairs = []
		# content5 has one that lacks the fixed fragments
		if count:
			self.assign_fixed_frags(1)
			root_f = self.sized_str_entry.fragments[0]
			# logging.debug(root_f)
			ptr1 = root_f.pointers[1]

			entry_size = 16
			out_frags, array_data = self.collect_array(ptr1, count, entry_size)
			self.sized_str_entry.fragments.extend(out_frags)

			for i in range(count):
				x = i * entry_size
				frags_entry = self.get_frags_between(out_frags, ptr1.data_offset + x, ptr1.data_offset + x+entry_size)
				entry_bytes = array_data[x:x+entry_size]
				self.frag_data_pairs.append((frags_entry, entry_bytes))

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		xmldata = ET.Element('AnimalResearchStartUnlockedSettings')
		for frags, entry_bytes in self.frag_data_pairs:
			layer = ET.SubElement(xmldata, 'unlockState')
			if not frags:
				continue
			entity, level = frags
			layer.set('name', self.get_zstr(entity.pointers[1].data))
			layer.set('level', self.get_zstr(level.pointers[1].data))
		self.write_xml(out_path, xmldata)
		return out_path,
