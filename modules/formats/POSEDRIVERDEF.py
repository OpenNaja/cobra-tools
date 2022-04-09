import logging
import struct
import traceback

from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?

from modules.helpers import as_bytes


class PosedriverdefLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		ss_ptr = self.sized_str_entry.pointers[0]
		_, count = struct.unpack("<QQ", ss_ptr.data)
		self.assign_fixed_frags(1)
		frag = self.sized_str_entry.fragments[0]
		ptr1 = frag.pointers[1]

		entry_size = 48
		out_frags, array_data = self.collect_array(ptr1, count, entry_size)
		self.sized_str_entry.fragments.extend(out_frags)
		self.frag_data_pairs = []
		for i in range(count):
			x = i * entry_size
			# name a x
			# name b x + 16
			# data x + 32
			frags_entry = self.get_frags_between(out_frags, ptr1.data_offset + x, ptr1.data_offset + x+entry_size)
			entry_bytes = array_data[x:x+entry_size]
			self.frag_data_pairs.append((frags_entry, entry_bytes))

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		xmldata = ET.Element('PoseDriverDef')
		for frags, entry_bytes in self.frag_data_pairs:
			bone = ET.SubElement(xmldata, 'bone')
			if not frags:
				continue
			joint, driven, data = frags
			bone.set('joint', self.get_zstr(joint.pointers[1].data))
			bone.set('driven_joint', self.get_zstr(driven.pointers[1].data))
			# 64 bytes
			data = struct.unpack("<16f", data.pointers[1].data)
			# 48 bytes
			entry_data = struct.unpack("<Q BBHI 4Q", entry_bytes)
			bone.set('data', data)
			bone.set('entry_data', entry_data)
		self.write_xml(out_path, xmldata)
		return out_path,

	def _get_data(self, file_path):
		return self.load_xml(file_path)
