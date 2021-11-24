import struct

from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?


class PSCollectionLoader(BaseFile):

	def create(self):
		ss = self.get_content(self.file_entry.path)
		pool_index, pool = self.get_pool(2)
		offset = pool.data.tell()
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		self.sized_str_entry.pointers[0].pool_index = pool_index
		self.sized_str_entry.pointers[0].data_offset = offset

		# read all in a dict from the xml
		psdata = ET.ElementTree(ET.fromstring(ss))

		pslistdata = psdata.findall('.//PreparedStatement')
		pslist = []
		for psdata in pslistdata:
			psentry = { 'name': psdata.attrib['name'], 'sql': psdata.attrib['sql'], 'args': [] }

			argdata = psdata.findall('.//ArgumentType')
			psargs = []
			for arg in argdata:
				psargs.append(int(arg.text))
			psentry['args'] = psargs
			pslist.append(psentry)

		print(pslist)
		pscount = len(pslist)

		# pscollection needs 8 bytes for the ptr and the array count
		# then also needs more per each entry and each arg
		pool.data.write(struct.pack("<QQ", 0, pscount))  # room for 16 bytes

		# new offset for list pointers
		poffset = pool.data.tell()

		# point the first frag points to the array of data now
		new_frag0 = self.create_fragment()
		new_frag0.pointers[0].pool_index = pool_index
		new_frag0.pointers[0].data_offset = offset + 0x00
		new_frag0.pointers[1].pool_index = pool_index
		new_frag0.pointers[1].data_offset = poffset

		psptr = pool.data.tell() # ptr to the array entry for this ps, used to create frags from now
		for ps in pslist:
			d = struct.pack("<QQQQ", 0, len(ps['args']), 0, 0 )
			print(f"{d}")
			pool.data.write(struct.pack("<QQQQ", 0, len(ps['args']), 0, 0 )) # ptr, count, ptr ptr

		for ps in pslist:
			pdptr = pool.data.tell() # ptr to the ps args

			argcount = 1
			for argtype in ps['args']:
				d = struct.pack('<BBBBIQQ', 0, argtype, argcount, 0, 0, 0, 0 )
				print(f"{d}")
				pool.data.write(struct.pack('<BBBBIQQ', 0, argtype, argcount, 0, 0, 0, 0 )) 
				argcount += 1

			# fix possible padding
			if argcount % 2 == 0:
				d = struct.pack('<Q', 0 )
				print(f"{d}")
				pool.data.write(struct.pack('<Q', 0 )) 

			# if there are args, make a frag for it
			if len(ps['args']):
				new_frag = self.create_fragment()
				new_frag.pointers[0].pool_index = pool_index
				new_frag.pointers[0].data_offset = psptr
				new_frag.pointers[1].pool_index = pool_index
				new_frag.pointers[1].data_offset = pdptr

			# write name and add ptr
			nameptr = pool.data.tell() # 
			pool.data.write(f"{ps['name']}\00".encode('utf-8'))
			new_frag = self.create_fragment()
			new_frag.pointers[0].pool_index = pool_index
			new_frag.pointers[0].data_offset = psptr + 0x10
			new_frag.pointers[1].pool_index = pool_index
			new_frag.pointers[1].data_offset = nameptr


			# write sql statement and ptr
			sqlptr = pool.data.tell() # 
			pool.data.write(f"{ps['sql']}\00".encode('utf-8'))
			new_frag = self.create_fragment()
			new_frag.pointers[0].pool_index = pool_index
			new_frag.pointers[0].data_offset = psptr + 0x18
			new_frag.pointers[1].pool_index = pool_index
			new_frag.pointers[1].data_offset = sqlptr

			#increase psptr to the next array member
			psptr += 0x20

		pass

	def collect(self):
		self.assign_ss_entry()
		print(f"Collecting {self.sized_str_entry.name}")

		pscount = struct.unpack("<QQ", self.sized_str_entry.pointers[0].data)[1]
		self.sized_str_entry.pscount = pscount
		#print(f"prepared statements: {self.sized_str_entry.pscount}")

		#get ptr to data array
		psfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
		psdata = psfragment.pointers[1].read_from_pool(0x20*pscount)
		self.sized_str_entry.pslist = []
		offset = 0
		index  = 1
		for x in range(pscount):
			_, argcount, _, _ = struct.unpack("<QQQQ", psdata[ offset : offset + 0x20])
			#print(f"argcount: {argcount}")

			# if argcount get args
			psargs = []
			if argcount:
				argsfragment = self.ovs.frags_from_pointer(psfragment.pointers[1], 1)[0]
				argsdata = argsfragment.pointers[1].read_from_pool(0x18 * argcount)
				dataoffset = 0
				for x in range(argcount):
					_, argType, argindex, _, _, _, _ = struct.unpack('<BBBBIQQ', argsdata[ dataoffset : dataoffset+0x18 ] )
					#print(f"argtype: {argType}  argindex: {argindex}")
					psargs.append(int(argType))
					dataoffset += 0x18

			# get name
			namefragment = self.ovs.frags_from_pointer(psfragment.pointers[1], 1)[0]
			namefragment.pointers[1].strip_zstring_padding()
			name = namefragment.pointers[1].data.decode('utf-8')[:-1]
			#print(name)

			# get sql
			sqlfragment = self.ovs.frags_from_pointer(psfragment.pointers[1], 1)[0]
			sqlfragment.pointers[1].strip_zstring_padding()
			sqldata = sqlfragment.pointers[1].data.decode('utf-8')[:-1]
			#print(sqldata)
			#print("----")
			# update offset
			offset += 0x20

			psentry = { 'name': name, 'sql': sqldata, 'args': psargs }
			self.sized_str_entry.pslist.append(psentry) 


		#print(self.sized_str_entry.pslist)
		pass

	def load(self, file_path):
		pass

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		print(f"Writing {name}")
		# enumnamer only has a list of strings
		out_files = []
		out_path = out_dir(name)
		xmldata = ET.Element('PSCollection')

		for ps in self.sized_str_entry.pslist: 
			psitem = ET.SubElement(xmldata, 'PreparedStatement')
			psitem.set('name', str(ps['name']))
			psitem.set('sql',  str(ps['sql']))

			if len(ps['args']):
				for arg in ps['args']:
				  argitem = ET.SubElement(psitem, 'ArgumentType')
				  argitem.text = str(arg)

		xmltext = ET.tostring(xmldata)

		with open(out_path, 'w') as outfile:
			outfile.write(xmltext.decode('utf-8'))
			out_files.append(out_path)
		    
		return out_files

