import struct

from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?


class UIMovieDefinitionLoader(BaseFile):

	# the final format will be after the 3 float values there are 10 count (bytes) values, and 
	# then 10 ptr values (one for each count in order), however all uimoviedefinition in jwe1/2
	# have most of these counters to 0 so their ptr type is unknown.

	def create(self):
		ss = self.get_content(self.file_entry.path)
		pool_index, pool = self.get_pool(2)
		offset = pool.data.tell()
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		self.sized_str_entry.pointers[0].pool_index = pool_index
		self.sized_str_entry.pointers[0].data_offset = offset

		moviedef  = {
			'ControlList'  : [],
			'InterfaceList': [],
			'UITriggerList': [],
			'Count1List'   : [],
			'Count2List'   : []
		}

		# read all in a dict from the xml
		xmldata = ET.ElementTree(ET.fromstring(ss))

		movie = xmldata.getroot()

		listdata = xmldata.findall('.//Control')
		for data in listdata:
			moviedef['ControlList'].append(data.text)

		listdata = xmldata.findall('.//UITrigger')
		for data in listdata:
			moviedef['UITriggerList'].append(data.text)

		listdata = xmldata.findall('.//Interface')
		for data in listdata:
			moviedef['InterfaceList'].append(data.text)

		listdata = xmldata.findall('.//List1')
		for data in listdata:
			moviedef['Count1List'].append(int(data.text))

		listdata = xmldata.findall('.//List2')
		for data in listdata:
			moviedef['Count2List'].append(int(data.text))

		# writting the data in several chunks because of readability 
		pool.data.write(struct.pack("<32sI2H", b'', int(movie.attrib['flags1']),int(movie.attrib['flags2']),int(movie.attrib['flags3'])))
		pool.data.write(struct.pack("<3f", float(movie.attrib['float1']),float(movie.attrib['float2']),float(movie.attrib['float3'])))
		pool.data.write(struct.pack("<4B", 0, len(moviedef['UITriggerList']), 0, len(moviedef['ControlList'])))
		pool.data.write(struct.pack("<4B", 0, 0, len(moviedef['Count1List']), len(moviedef['Count2List'])))
		pool.data.write(struct.pack("<4B", len(moviedef['InterfaceList']), 0, 0, 0))
		pool.data.write(struct.pack("<80s", b''))

		# write name and add ptr
		nameptr = pool.data.tell() # 
		pool.data.write(f"{movie.attrib['MovieName']}\00".encode('utf-8'))
		new_frag = self.create_fragment()
		new_frag.pointers[0].pool_index = pool_index
		new_frag.pointers[0].data_offset = offset + 0x00
		new_frag.pointers[1].pool_index = pool_index
		new_frag.pointers[1].data_offset = nameptr

		# write pkgname and add ptr
		nameptr = pool.data.tell() # 
		pool.data.write(f"{movie.attrib['PkgName']}\00".encode('utf-8'))
		new_frag = self.create_fragment()
		new_frag.pointers[0].pool_index = pool_index
		new_frag.pointers[0].data_offset = offset + 0x08
		new_frag.pointers[1].pool_index = pool_index
		new_frag.pointers[1].data_offset = nameptr

		# write CategoryName and add ptr
		nameptr = pool.data.tell() # 
		pool.data.write(f"{movie.attrib['CategoryName']}\00".encode('utf-8'))
		new_frag = self.create_fragment()
		new_frag.pointers[0].pool_index = pool_index
		new_frag.pointers[0].data_offset = offset + 0x10
		new_frag.pointers[1].pool_index = pool_index
		new_frag.pointers[1].data_offset = nameptr

		# write TypeName and add ptr
		nameptr = pool.data.tell() # 
		pool.data.write(f"{movie.attrib['TypeName']}\00".encode('utf-8'))
		new_frag = self.create_fragment()
		new_frag.pointers[0].pool_index = pool_index
		new_frag.pointers[0].data_offset = offset + 0x18
		new_frag.pointers[1].pool_index = pool_index
		new_frag.pointers[1].data_offset = nameptr


		# write triggers at offset+0x48
		if len(moviedef['UITriggerList']):

			# offset where first string starts
			doffset = pool.data.tell()

			# pack data now.. we are not doing rstrip to the lines.. worth considering to remove extra spaces
			pool.data.write("\00".join(moviedef['UITriggerList']).encode('utf-8'))
			pool.data.write(b"\00")

			# new offset for list pointers
			poffset = pool.data.tell()

			# point the list frag to the end of the data now.
			new_frag0 = self.create_fragment()
			new_frag0.pointers[0].pool_index = pool_index
			new_frag0.pointers[0].data_offset = offset + 0x48
			new_frag0.pointers[1].pool_index = pool_index
			new_frag0.pointers[1].data_offset = poffset

			# for each line, add the frag ptr space and create the frag ptr
			for x in moviedef['UITriggerList']:
				pool.data.write(struct.pack("<8s", b''))
				strfrag = self.create_fragment()
				strfrag.pointers[0].pool_index = pool_index
				strfrag.pointers[0].data_offset = poffset
				strfrag.pointers[1].pool_index = pool_index
				strfrag.pointers[1].data_offset = doffset

				poffset += 8
				doffset += len(x) + 1 # skip string lenght

		# write Controls at offset+0x58
		if len(moviedef['ControlList']):

			# offset where first string starts
			doffset = pool.data.tell()

			# pack data now.. we are not doing rstrip to the lines.. worth considering to remove extra spaces
			pool.data.write("\00".join(moviedef['ControlList']).encode('utf-8'))
			pool.data.write(b"\00")

			# new offset for list pointers
			poffset = pool.data.tell()

			# point the list frag to the end of the data now.
			new_frag0 = self.create_fragment()
			new_frag0.pointers[0].pool_index = pool_index
			new_frag0.pointers[0].data_offset = offset + 0x58
			new_frag0.pointers[1].pool_index = pool_index
			new_frag0.pointers[1].data_offset = poffset

			# for each line, add the frag ptr space and create the frag ptr
			for x in moviedef['ControlList']:
				pool.data.write(struct.pack("<8s", b''))
				strfrag = self.create_fragment()
				strfrag.pointers[0].pool_index = pool_index
				strfrag.pointers[0].data_offset = poffset
				strfrag.pointers[1].pool_index = pool_index
				strfrag.pointers[1].data_offset = doffset

				poffset += 8
				doffset += len(x) + 1 # skip string lenght

		# write List1 at offset+0x70
		if len(moviedef['Count1List']):
			# offset where first string starts
			doffset = pool.data.tell()

			# pack data now.. 
			pool.data.write( struct.pack(f"<{len(moviedef['Count1List'])}I", *moviedef['Count1List']))
			# add some extra 00
			pool.data.write( struct.pack("<Q", 0))

			# point the list frag to the end of the data now.
			new_frag0 = self.create_fragment()
			new_frag0.pointers[0].pool_index = pool_index
			new_frag0.pointers[0].data_offset = offset + 0x70
			new_frag0.pointers[1].pool_index = pool_index
			new_frag0.pointers[1].data_offset = doffset


		# write List2 at offset+0x78
		if len(moviedef['Count2List']):
			# offset where first string starts
			doffset = pool.data.tell()

			# pack data now.. 
			pool.data.write( struct.pack(f"<{len(moviedef['Count2List'])}I", *moviedef['Count2List']))
			# add some extra 00
			pool.data.write( struct.pack("<Q", 0))

			# point the list frag to the end of the data now.
			new_frag0 = self.create_fragment()
			new_frag0.pointers[0].pool_index = pool_index
			new_frag0.pointers[0].data_offset = offset + 0x78
			new_frag0.pointers[1].pool_index = pool_index
			new_frag0.pointers[1].data_offset = doffset

		# write interfaces at offset+0x80
		if len(moviedef['InterfaceList']):

			# offset where first string starts
			doffset = pool.data.tell()

			# pack data now.. we are not doing rstrip to the lines.. worth considering to remove extra spaces
			pool.data.write("\00".join(moviedef['InterfaceList']).encode('utf-8'))
			pool.data.write(b"\00")
			# new offset for list pointers
			poffset = pool.data.tell()

			# point the list frag to the end of the data now.
			new_frag0 = self.create_fragment()
			new_frag0.pointers[0].pool_index = pool_index
			new_frag0.pointers[0].data_offset = offset + 0x80
			new_frag0.pointers[1].pool_index = pool_index
			new_frag0.pointers[1].data_offset = poffset

			# for each line, add the frag ptr space and create the frag ptr
			for x in moviedef['InterfaceList']:
				pool.data.write(struct.pack("<8s", b''))
				strfrag = self.create_fragment()
				strfrag.pointers[0].pool_index = pool_index
				strfrag.pointers[0].data_offset = poffset
				strfrag.pointers[1].pool_index = pool_index
				strfrag.pointers[1].data_offset = doffset

				poffset += 8
				doffset += len(x) + 1 # skip string lenght

		pass

	def collect(self):
		self.assign_ss_entry()
		print(f"Collecting {self.sized_str_entry.name}")

		# it is a long struct
		unpackstr = "<32sI2H3f12B80s" 
		_,flags1,flags2,flags3,fval1,fval2,fval3,counta,count4,countc,ctrlcount,counte, countf,count1,count2,count3,countj,_,_,_ =\
		struct.unpack(unpackstr, self.sized_str_entry.pointers[0].read_from_pool(0x90))

		self.sized_str_entry.moviedef  = {
			'flags1': flags1,
			'flags2': flags2,
			'flags3': flags3,
			'float1': fval1,
			'float2': fval2,
			'float3': fval3,
			'ControlList': [],
			'InterfaceList': [],
			'UITriggerList': [],
			'Count1List': [],
			'Count2List':[]
		}

		# get name
		tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
		tmpfragment.pointers[1].strip_zstring_padding()
		self.sized_str_entry.moviedef['MovieName'] = tmpfragment.pointers[1].data.decode('utf-8')[:-1]

		# get package (guess)
		tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
		tmpfragment.pointers[1].strip_zstring_padding()
		self.sized_str_entry.moviedef['PkgName'] = tmpfragment.pointers[1].data.decode('utf-8')[:-1]

		# get category (gues)
		tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
		tmpfragment.pointers[1].strip_zstring_padding()
		self.sized_str_entry.moviedef['CategoryName'] = tmpfragment.pointers[1].data.decode('utf-8')[:-1]

		# get type (gues)
		tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
		tmpfragment.pointers[1].strip_zstring_padding()
		self.sized_str_entry.moviedef['TypeName'] = tmpfragment.pointers[1].data.decode('utf-8')[:-1]
		#print(ctrlcount)
		#print(self.sized_str_entry.moviedef)

		# will be finding frags now depending on the counts, starting with count4
		# corresponding to a list of strings of UI events/triggers
		if count4:
			uilistfrag  = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			tmpfragment = self.ovs.frags_from_pointer(uilistfrag.pointers[1], count4)
			uitriggerlist = []
			for var in tmpfragment:
				var.pointers[1].strip_zstring_padding()
				strval = var.pointers[1].data.decode('utf-8')
				if strval[-1] == '\x00':
					strval = strval[:-1]
				uitriggerlist.append(strval)
			self.sized_str_entry.moviedef['UITriggerList'] = uitriggerlist

		# list of UI controls
		if ctrlcount:
			uilistfrag  = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			tmpfragment = self.ovs.frags_from_pointer(uilistfrag.pointers[1], ctrlcount)
			uinamelist = []
			for var in tmpfragment:
				var.pointers[1].strip_zstring_padding()
				strval = var.pointers[1].data.decode('utf-8')
				if strval[-1] == '\x00':
					strval = strval[:-1]
				uinamelist.append(strval)
			self.sized_str_entry.moviedef['ControlList'] = uinamelist

		if count1:
			tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			templlist = struct.unpack(f"<{count1}I", tmpfragment.pointers[1].read_from_pool(0x4 * count1))
			self.sized_str_entry.moviedef['Count1List'] = templlist
			pass

		if count2:
			tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			templlist = struct.unpack(f"<{count2}I", tmpfragment.pointers[1].read_from_pool(0x4 * count2))
			self.sized_str_entry.moviedef['Count2List'] = templlist
			pass

		if count3:
			uilistfrag  = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			tmpfragment = self.ovs.frags_from_pointer(uilistfrag.pointers[1], count3)
			uiInterfacelist = []
			for var in tmpfragment:
				var.pointers[1].strip_zstring_padding()
				strval = var.pointers[1].data.decode('utf-8')
				if strval[-1] == '\x00':
					strval = strval[:-1]
				uiInterfacelist.append(strval)
			self.sized_str_entry.moviedef['InterfaceList'] = uiInterfacelist

		#print(self.sized_str_entry.moviedef)
		pass

	def load(self, file_path):
		pass

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		print(f"Writing {name}")

		out_files = []
		out_path = out_dir(name)

		md = self.sized_str_entry.moviedef

		xmldata = ET.Element('UIMovieDefinition')
		xmldata.set('MovieName', str(md['MovieName']))
		xmldata.set('PkgName',  str(md['PkgName']))
		xmldata.set('CategoryName', str(md['CategoryName']))
		xmldata.set('TypeName',  str(md['TypeName']))
		xmldata.set('flags1',  str(md['flags1']))
		xmldata.set('flags2',  str(md['flags2']))
		xmldata.set('flags3',  str(md['flags3']))
		xmldata.set('float1',  str(md['float1']))
		xmldata.set('float2',  str(md['float2']))
		xmldata.set('float3',  str(md['float3']))

		for cl in md['UITriggerList']:
			clitem = ET.SubElement(xmldata, 'UITrigger')
			clitem.text = cl

		for cl in md['ControlList']:
			clitem = ET.SubElement(xmldata, 'Control')
			clitem.text = cl

		for cl in md['InterfaceList']:
			clitem = ET.SubElement(xmldata, 'Interface')
			clitem.text = cl

		for cl in md['Count1List']:
			clitem = ET.SubElement(xmldata, 'List1')
			clitem.text = str(cl)

		for cl in md['Count2List']:
			clitem = ET.SubElement(xmldata, 'List2')
			clitem.text = str(cl)

		xmltext = ET.tostring(xmldata)

		with open(out_path, 'w') as outfile:
			outfile.write(xmltext.decode('utf-8'))
			out_files.append(out_path)
		    
		return out_files


