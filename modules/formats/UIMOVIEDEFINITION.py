import struct

from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?


class UIMovieDefinitionLoader(BaseFile):

	def create(self):
		pass

	def collect(self):
		self.assign_ss_entry()
		print(f"Collecting {self.sized_str_entry.name}")

		# it is a long struct
		unpackstr = "<32sI2H3f8BI80s" 
		_,flags1,flags2,flags3,fval1,fval2,fval3,_,count4,_,ctrlcount,_,_,count1,count2,count3,_ =\
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

		#print(f"prepared statements: {self.sized_str_entry.pscount}")
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
		print(ctrlcount)
		print(self.sized_str_entry.moviedef)


		# will be finding frags now depending on the counts, starting with count4
		# corresponding to a list of strings of UI events/triggers
		if count4:
			uilistfrag  = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			tmpfragment = self.ovs.frags_from_pointer(uilistfrag.pointers[1], count4)
			uitriggerlist = []
			for var in tmpfragment:
				var.pointers[1].strip_zstring_padding()
				uitriggerlist.append(var.pointers[1].data.decode('utf-8')[:-1])
			self.sized_str_entry.moviedef['UITriggerList'] = uitriggerlist

		# list of UI controls
		if ctrlcount:
			uilistfrag  = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			tmpfragment = self.ovs.frags_from_pointer(uilistfrag.pointers[1], ctrlcount)
			uinamelist = []
			for var in tmpfragment:
				var.pointers[1].strip_zstring_padding()
				uinamelist.append(var.pointers[1].data.decode('utf-8')[:-1])
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
				uiInterfacelist.append(var.pointers[1].data.decode('utf-8')[:-1])
			self.sized_str_entry.moviedef['InterfaceList'] = uiInterfacelist

		print(self.sized_str_entry.moviedef)
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


