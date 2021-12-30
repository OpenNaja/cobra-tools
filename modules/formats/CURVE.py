import logging
import struct
from modules.formats.shared import get_padding
from modules.formats.BaseFormat import BaseFile
from modules.helpers import zstr
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?


class CurveLoader(BaseFile):

	def create(self):
		f_0, f_1 = self._get_data(self.file_entry.path)
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		f = self.create_fragments(self.sized_str_entry, 1)[0]
		self.write_to_pool(f.pointers[1], 2, f_1)
		self.write_to_pool(self.sized_str_entry.pointers[0], 4, b"")
		self.write_to_pool(f.pointers[0], 4, f_0)

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"Collecting {self.sized_str_entry.name}")
		self.assign_fixed_frags(1)

		_, count = struct.unpack("<QQ", self.sized_str_entry.pointers[0].data)
		self.sized_str_entry.keyvalues = []
		logging.info(f"count {count}")

		# get ptr to data
		cfragment = self.sized_str_entry.fragments[0]
		cdata = cfragment.pointers[1].read_from_pool(0x8 * count)
		offset = 0
		for x in range(count):
			key, value = struct.unpack("<ff", cdata[offset: offset + 0x08])
			#logging.info(f"key:  {key}  value: {value}")
			item = { 'key' : key, 'value' : value }
			self.sized_str_entry.keyvalues.append(item)
			offset += 0x08

	def load(self, file_path):
		f_0, f_1 = self._get_data(file_path)
		self.sized_str_entry.fragments[0].pointers[1].update_data(f_1, update_copies=True)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")

		xml_data = ET.Element('AnimationCurveData')
		for item in self.sized_str_entry.keyvalues:
			xmlitem = ET.SubElement(xml_data, 'KeyValue')
			xmlitem.set('key', str(item['key']))
			xmlitem.text = str(item['value'])

		out_path = out_dir(name)
		self.write_xml(out_path, xml_data)
		return out_path,

	def _get_data(self, file_path):
		"""Loads and returns the data for a CURVE"""
		curvedata = self.load_xml(file_path)
		f_1 = bytearray()
		for item in curvedata:
			f_1 += struct.pack("<ff", float(item.attrib['key']), float(item.text))
		f_0 = struct.pack('<QQ', 0x00, len(curvedata))  # fragment pointer 0 data

		# there is not a reason to add this padding but just to be safe
		return f_0, f_1 + get_padding(len(f_1), alignment=8)
