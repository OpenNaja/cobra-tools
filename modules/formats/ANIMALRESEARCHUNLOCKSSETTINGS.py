import logging
import struct

from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?


class AnimalresearchunlockssettingsLoader(BaseFile):

	def create(self):
		xml = self._get_data(self.file_entry.path)


	def collect(self):
		self.assign_ss_entry()
		ss_pointer = self.sized_str_entry.pointers[0]
		_, count = struct.unpack("<QQ", ss_pointer.data)
		# logging.debug(ss_pointer.data)
		# logging.debug(f"{self.file_entry.name} has {count} entries")
		self.assign_fixed_frags(1)
		frag = self.sized_str_entry.fragments[0]
		# logging.debug(frag)
		ptr1 = frag.pointers[1]

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
			name = level_frag.pointers[1].data
			# logging.debug(f"level_frag: {name}")
			if children_count:
				ptr_frag = frags_entry[2]
				level_frag.children = self.ovs.frags_from_pointer(ptr_frag.pointers[1], children_count)
				for f in level_frag.children:
					name = f.pointers[1].data
					# logging.debug(f"child: {name}")
			if next_level:
				ptr_frag = frags_entry[1]
				level_frag.next = self.ovs.frags_from_pointer(ptr_frag.pointers[1], next_level)
				for f in level_frag.next:
					name = f.pointers[1].data
					# logging.debug(f"next: {name}")
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
		self.assign_fixed_frags(1)
		frag = self.sized_str_entry.fragments[0]
		# logging.debug(frag)
		ptr1 = frag.pointers[1]

		entry_size = 16
		out_frags, array_data = self.collect_array(ptr1, count, entry_size)
		self.sized_str_entry.fragments.extend(out_frags)

		self.frag_data_pairs = []
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
