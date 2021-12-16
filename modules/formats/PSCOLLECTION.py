import logging
import struct

from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET  # prob move this to a custom modules.helpers or utils?

from modules.formats.shared import get_padding


class PSCollectionLoader(BaseFile):

	def create(self):
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		pscollection = self.load_xml(self.file_entry.path)

		# pscollection needs 8 bytes for the ptr and the array count
		# then also needs more per each entry and each arg
		f_0 = self.create_fragments(self.sized_str_entry, 1)[0]
		self.write_to_pool(f_0.pointers[0], 2, b"")
		self.write_to_pool(self.sized_str_entry.pointers[0], 2, struct.pack("<QQ", 0, len(pscollection)))
		# point the first frag to the array of data now
		# ptr, count, ptr ptr
		self.write_to_pool(f_0.pointers[1], 2, b"".join(struct.pack("<QQQQ", 0, len(ps), 0, 0) for ps in pscollection))
		rel_offset = 0
		for prepared_statment in pscollection:
			# if there are args, make a frag for it
			if len(prepared_statment):
				f = self.create_fragments(self.sized_str_entry, 1)[0]
				args_data = b"".join(struct.pack('<BBBBIQQ', 0, int(arg.text), 1+i, 0, 0, 0, 0) for i, arg in enumerate(prepared_statment))
				self.ptr_relative(f.pointers[0], f_0.pointers[1], rel_offset=rel_offset)
				self.write_to_pool(f.pointers[1], 2, args_data + get_padding(len(args_data), alignment=16))

			# write name and sql as a name ptr each
			f_name, f_sql = self.create_fragments(self.sized_str_entry, 2)
			self.ptr_relative(f_name.pointers[0], f_0.pointers[1], rel_offset=rel_offset + 0x10)
			self.write_to_pool(f_name.pointers[1], 2, f"{prepared_statment.attrib['name']}\00".encode('utf-8'))
			self.ptr_relative(f_sql.pointers[0], f_0.pointers[1], rel_offset=rel_offset + 0x18)
			self.write_to_pool(f_sql.pointers[1], 2, f"{prepared_statment.attrib['sql']}\00".encode('utf-8'))

			# increase psptr to the next array member
			rel_offset += 0x20

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"Collecting {self.sized_str_entry.name}")

		pscount = struct.unpack("<QQ", self.sized_str_entry.pointers[0].data)[1]
		self.sized_str_entry.pscount = pscount
		# print(f"prepared statements: {self.sized_str_entry.pscount}")

		# get ptr to data array
		psfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
		psdata = psfragment.pointers[1].read_from_pool(0x20 * pscount)
		self.sized_str_entry.pslist = []
		offset = 0
		index = 1
		for x in range(pscount):
			_, argcount, _, _ = struct.unpack("<QQQQ", psdata[offset: offset + 0x20])
			# print(f"argcount: {argcount}")

			# if argcount get args
			psargs = []
			if argcount:
				argsfragment = self.ovs.frags_from_pointer(psfragment.pointers[1], 1)[0]
				argsdata = argsfragment.pointers[1].read_from_pool(0x18 * argcount)
				dataoffset = 0
				for x in range(argcount):
					_, argType, argindex, _, _, _, _ = struct.unpack('<BBBBIQQ',
																	 argsdata[dataoffset: dataoffset + 0x18])
					# print(f"argtype: {argType}  argindex: {argindex}")
					psargs.append(int(argType))
					dataoffset += 0x18

			# get name
			namefragment = self.ovs.frags_from_pointer(psfragment.pointers[1], 1)[0]
			namefragment.pointers[1].strip_zstring_padding()
			strval = namefragment.pointers[1].data.decode('utf-8')
			if strval[-1] == '\x00':
				strval = strval[:-1]
			name = strval
			# print(name)

			# get sql
			sqlfragment = self.ovs.frags_from_pointer(psfragment.pointers[1], 1)[0]
			sqlfragment.pointers[1].strip_zstring_padding()
			strval = sqlfragment.pointers[1].data.decode('utf-8')
			if strval[-1] == '\x00':
				strval = strval[:-1]
			sqldata = strval
			# print(sqldata)
			# print("----")
			# update offset
			offset += 0x20

			psentry = {'name': name, 'sql': sqldata, 'args': psargs}
			self.sized_str_entry.pslist.append(psentry)

	def load(self, file_path):
		pass

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")
		out_path = out_dir(name)
		xml_data = ET.Element('PSCollection')

		for ps in self.sized_str_entry.pslist:
			psitem = ET.SubElement(xml_data, 'PreparedStatement')
			psitem.set('name', str(ps['name']))
			psitem.set('sql', str(ps['sql']))

			if len(ps['args']):
				for arg in ps['args']:
					argitem = ET.SubElement(psitem, 'ArgumentType')
					argitem.text = str(arg)

		self.write_xml(out_path, xml_data)
		return out_path,
