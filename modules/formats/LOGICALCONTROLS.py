import struct

from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?

# .logicalcontrols need to be in Init.ovl for loading on time.

# Apparently the binding value is from a = 1..
# HUD_MapMode:          13  209     m and M
# HUD_Notifications:    14  210     n and N

class LogicalControlsLoader(BaseFile):

	def create(self):
		print(f"Importing {self.file_entry.path}")
		ss = self.get_content(self.file_entry.path)

		pool = self.get_pool(2)
		offset = pool.data.tell()
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		self.sized_str_entry.pointers[0].pool = pool
		self.sized_str_entry.pointers[0].data_offset = offset

		# read all in a dict from the xml
		lcmaindata = ET.ElementTree(ET.fromstring(ss))

		lclistdata = lcmaindata.findall('.//LogicalControl')
		lclist = []
		for lcdata in lclistdata:
			lcentry = { 'name': lcdata.attrib['name'], 'flags': int(lcdata.attrib['flags']), 'defaults': [] }

			argxmldata = lcdata.findall('.//DefaultValue')
			lcargs = []
			for arg in argxmldata:
				argdata = {'k1a': int(arg.attrib['k1a']), 'k1b': int(arg.attrib['k1b']), 'k2': int(arg.attrib['k2']), 'k3': int(arg.attrib['k3']), 'k4': int(arg.attrib['k4'])}
				lcargs.append(argdata)
			lcentry['defaults'] = lcargs
			lclist.append(lcentry)

		lccount = len(lclist)

		# start packing the main struct body, for now only support button configs
		pool.data.write(struct.pack("<4Q4BIQ", 0,0,0,0, lccount, 0,0,0,0,0))  # room for 16 bytes

		# new offset for list pointers
		poffset = pool.data.tell()

		# write now the array of data
		if lccount > 0:
			# point the first frag to the array of data now
			new_frag0 = self.create_fragment()
			new_frag0.pointers[0].pool = pool
			new_frag0.pointers[0].data_offset = offset + 0x00
			new_frag0.pointers[1].pool = pool
			new_frag0.pointers[1].data_offset = poffset

			# it is an array so pack all data in it first, then we make pointers
			for lc in lclist:
				# space for 2 pointers, then the count of the second pointer then 0
				pool.data.write(struct.pack("<QQII", 0,0, len(lc['defaults']), lc['flags']))

			for lc in lclist:
				# write name
				nameptr = pool.data.tell()
				pool.data.write(f"{lc['name']}\00".encode('utf-8'))
				new_frag = self.create_fragment()
				new_frag.pointers[0].pool = pool
				new_frag.pointers[0].data_offset = poffset
				new_frag.pointers[1].pool = pool
				new_frag.pointers[1].data_offset = nameptr

				# write default options now
				if len(lc['defaults']) > 0:
					dataptr = pool.data.tell()
					for df in lc['defaults']:
						pool.data.write(struct.pack("<HHIII", df['k1a'], df['k1b'], df['k2'], df['k3'], df['k4']))

					#add frag to the data
					new_frag = self.create_fragment()
					new_frag.pointers[0].pool = pool
					new_frag.pointers[0].data_offset = poffset+0x08
					new_frag.pointers[1].pool = pool
					new_frag.pointers[1].data_offset = dataptr

				# next entry
				poffset += 0x18

		# repeat for other counters now


	def collect(self):
		self.assign_ss_entry()
		print(f"Collecting {self.sized_str_entry.name}")

		# there are 4 counters for diff types of controls, c1 is buttons, c4 is axis, the others are confused for now
		# 
		_,_,_,_, c1, c2, c3, c4, flags, _ = struct.unpack("<4Q4BIQ", self.sized_str_entry.pointers[0].read_from_pool(0x30))
		logicalcontrols = []

		# process normal buttons
		if c1 > 0:
			psfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			psdata = psfragment.pointers[1].read_from_pool(0x18*c1)
			self.sized_str_entry.pslist = []
			offset = 0
			index  = 1
			for x in range(c1):
				_,_, dcount, flags, = struct.unpack("<QQII", psdata[ offset : offset + 0x18])

				# get name
				namefragment = self.ovs.frags_from_pointer(psfragment.pointers[1], 1)[0]
				namefragment.pointers[1].strip_zstring_padding()
				strval = namefragment.pointers[1].data.decode('utf-8')
				if strval[-1] == '\x00':
					strval = strval[:-1]
				name = strval

				doffset = 0
				defaults = []
				if dcount > 0:
					deffragment = self.ovs.frags_from_pointer(psfragment.pointers[1], 1)[0]
					defdata = deffragment.pointers[1].read_from_pool(0x10*dcount)
					for t in range(dcount):
						k1a, k1b, k2, k3, k4 = struct.unpack("<HHIII", defdata[ doffset : doffset + 0x10])
						doffset += 0x10
						defaultentry = { 'k1a': k1a, 'k1b': k1b, 'k2': k2, 'k3': k3, 'k4': k4 }
						defaults.append(defaultentry) 

				offset += 0x18
				controlentry = { 'type': 'Button', 'name': name, 'flags': flags, 'dcount': dcount, 'defaults': defaults}
				logicalcontrols.append(controlentry) 

		print(f"Captured {len(logicalcontrols)} controls")
		self.sized_str_entry.logicalcontrols = logicalcontrols
		pass

	def load(self, file_path):
		pass

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		print(f"Writing {name}")		

		out_files = []
		out_path = out_dir(name)

		logicalcontrols = self.sized_str_entry.logicalcontrols
		xmldata = ET.Element('LogicalControls')

		for lc in logicalcontrols: 
			lcitem = ET.SubElement(xmldata, 'LogicalControl')
			lcitem.set('name',  str(lc['name']))
			lcitem.set('type',  str(lc['type']))
			lcitem.set('flags', str(lc['flags']))

			if len(lc['defaults']):
				for arg in lc['defaults']:
					argitem = ET.SubElement(lcitem, 'DefaultValue')
					argitem.set('k1a',  str(arg['k1a']))
					argitem.set('k1b',  str(arg['k1b']))
					argitem.set('k2',  str(arg['k2']))
					argitem.set('k3',  str(arg['k3']))
					argitem.set('k4',  str(arg['k4']))

		xmltext = ET.tostring(xmldata)

		with open(out_path, 'w') as outfile:
			outfile.write(xmltext.decode('utf-8'))
			out_files.append(out_path)
		return out_files

