import logging
import struct

from modules.formats.BaseFormat import BaseFile
from modules.helpers import as_bytes
import xml.etree.ElementTree as ET  # prob move this to a custom modules.helpers or utils?


class UIMovieDefinitionLoader(BaseFile):

	# the final format will be after the 3 float values there are 12 count (bytes) values, and 
	# then 10 ptr values (one for each count in order), however all uimoviedefinition in jwe1/2
	# have most of these counters to 0 so their ptr type is unknown.

	def create(self):
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		print(f"Loading {self.file_entry.path}")
		moviedef = self.load_xml(self.file_entry.path)

		namelistdata = moviedef.findall('.//Name')
		names = []
		for name in namelistdata:
			names.append(name.text)

		self.uinamelist = [data.text for data in moviedef.findall('.//Control')]
		self.assetpkglist = [data.text for data in moviedef.findall('.//AssetPackage')]
		self.uitriggerlist = [data.text for data in moviedef.findall('.//UITrigger')]
		self.uiInterfacelist = [data.text for data in moviedef.findall('.//Interface')]
		self.Count1List = [int(data.text) for data in moviedef.findall('.//List1')]
		self.Count2List = [int(data.text) for data in moviedef.findall('.//List2')]

		# writting the data in several chunks because of readability 
		ss = struct.pack("<32sI2H", b'', int(moviedef.attrib['flags1']), int(moviedef.attrib['flags2']),
									int(moviedef.attrib['flags3']))
		ss += struct.pack("<3f", float(moviedef.attrib['float1']), float(moviedef.attrib['float2']),
									float(moviedef.attrib['float3']))
		ss += struct.pack("<4B", 0, len(self.uitriggerlist), 0, len(self.uinamelist))
		ss += struct.pack("<4B", len(self.assetpkglist), 0, len(self.Count1List), len(self.Count2List))
		ss += struct.pack("<4B", len(self.uiInterfacelist), 0, 0, 0)
		ss += struct.pack("<80s", b'')
		self.write_to_pool(self.sized_str_entry.pointers[0], 2, ss)

		# main names list
		frag0, frag1, frag2, frag3 = self.create_fragments(self.sized_str_entry, 4)
		ss_ptr = self.sized_str_entry.pointers[0]
		self.ptr_relative(frag0.pointers[0], ss_ptr)
		self.ptr_relative(frag1.pointers[0], ss_ptr, rel_offset=8)
		self.ptr_relative(frag2.pointers[0], ss_ptr, rel_offset=16)
		self.ptr_relative(frag3.pointers[0], ss_ptr, rel_offset=24)
		self.write_to_pool(frag0.pointers[1], 2, f"{moviedef.attrib['MovieName']}\00".encode('utf-8'))
		self.write_to_pool(frag1.pointers[1], 2, f"{moviedef.attrib['PkgName']}\00".encode('utf-8'))
		self.write_to_pool(frag2.pointers[1], 2, f"{moviedef.attrib['CategoryName']}\00".encode('utf-8'))
		self.write_to_pool(frag3.pointers[1], 2, f"{moviedef.attrib['TypeName']}\00".encode('utf-8'))

		# Up to here should be enough to build almost any move without list
		# time now to attach all the lists

		if len(self.uitriggerlist):
			# for each line, add the frag ptr space and create the frag ptr
			item_frags = self.create_fragments(self.sized_str_entry, len(self.uitriggerlist))
			for frag in item_frags:
				self.write_to_pool(frag.pointers[0], 2, b"\x00" * 8)

			for item, frag in zip(self.uitriggerlist, item_frags):
				self.write_to_pool(frag.pointers[1], 2, as_bytes(item))

			# point the list frag to the end of the data now.
			new_frag1 = self.create_fragments(self.sized_str_entry, 1)[0]
			self.ptr_relative(new_frag1.pointers[0], self.sized_str_entry.pointers[0], 0x48)
			self.ptr_relative(new_frag1.pointers[1], item_frags[0].pointers[0])

		if len(self.uinamelist):
			# for each line, add the frag ptr space and create the frag ptr
			item_frags = self.create_fragments(self.sized_str_entry, len(self.uinamelist))
			for frag in item_frags:
				self.write_to_pool(frag.pointers[0], 2, b"\x00" * 8)

			for item, frag in zip(self.uinamelist, item_frags):
				self.write_to_pool(frag.pointers[1], 2, as_bytes(item))

			# point the list frag to the end of the data now.
			new_frag1 = self.create_fragments(self.sized_str_entry, 1)[0]
			self.ptr_relative(new_frag1.pointers[0], self.sized_str_entry.pointers[0], 0x58)
			self.ptr_relative(new_frag1.pointers[1], item_frags[0].pointers[0])

		if len(self.assetpkglist):
			# for each line, add the frag ptr space and create the frag ptr
			item_frags = self.create_fragments(self.sized_str_entry, len(self.assetpkglist))
			for frag in item_frags:
				self.write_to_pool(frag.pointers[0], 2, b"\x00" * 8)

			for item, frag in zip(self.assetpkglist, item_frags):
				self.write_to_pool(frag.pointers[1], 2, as_bytes(item))

			# point the list frag to the end of the data now.
			new_frag1 = self.create_fragments(self.sized_str_entry, 1)[0]
			self.ptr_relative(new_frag1.pointers[0], self.sized_str_entry.pointers[0], 0x60)
			self.ptr_relative(new_frag1.pointers[1], item_frags[0].pointers[0])

		if len(self.Count1List):
			# for each line, add the frag ptr space and create the frag ptr
			item_frag = self.create_fragments(self.sized_str_entry, 1)[0]
			for item in self.Count1List:
				print(f"item {item}")
				self.write_to_pool(item_frag.pointers[1], 2, struct.pack("<I", int(item)))

			# point the list frag to the end of the data now.
			new_frag1 = self.create_fragments(self.sized_str_entry, 1)[0]
			self.ptr_relative(new_frag1.pointers[0], self.sized_str_entry.pointers[0], 0x70)
			self.ptr_relative(new_frag1.pointers[1], item_frag.pointers[0])

		if len(self.Count2List):
			# for each line, add the frag ptr space and create the frag ptr
			item_frag = self.create_fragments(self.sized_str_entry, 1)[0]

			for item in self.Count2List:
				print(f"item {item}")
				self.write_to_pool(item_frag.pointers[1], 2, struct.pack("<I", int(item)))

			# point the list frag to the end of the data now.
			new_frag1 = self.create_fragments(self.sized_str_entry, 1)[0]
			self.ptr_relative(new_frag1.pointers[0], self.sized_str_entry.pointers[0], 0x78)
			self.ptr_relative(new_frag1.pointers[1], item_frag.pointers[0])


		if len(self.uiInterfacelist):
			# for each line, add the frag ptr space and create the frag ptr
			item_frags = self.create_fragments(self.sized_str_entry, len(self.uiInterfacelist))
			for frag in item_frags:
				self.write_to_pool(frag.pointers[0], 2, b"\x00" * 8)

			for item, frag in zip(self.uiInterfacelist, item_frags):
				self.write_to_pool(frag.pointers[1], 2, as_bytes(item))

			# point the list frag to the end of the data now.
			new_frag1 = self.create_fragments(self.sized_str_entry, 1)[0]
			self.ptr_relative(new_frag1.pointers[0], self.sized_str_entry.pointers[0], 0x80)
			self.ptr_relative(new_frag1.pointers[1], item_frags[0].pointers[0])













		if 1 == 1:
			return

		ss = self.get_content(self.file_entry.path)
		pool = self.get_pool(2)
		offset = pool.data.tell()
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		self.sized_str_entry.pointers[0].pool = pool
		self.sized_str_entry.pointers[0].data_offset = offset

		# read all in a dict from the xml
		xmldata = ET.ElementTree(ET.fromstring(ss))
		movie = xmldata.getroot()

		self.uinamelist = [data.text for data in xmldata.findall('.//Control')]
		self.uitriggerlist = [data.text for data in xmldata.findall('.//UITrigger')]
		self.uiInterfacelist = [data.text for data in xmldata.findall('.//Interface')]
		self.Count1List = [int(data.text) for data in xmldata.findall('.//List1')]
		self.Count2List = [int(data.text) for data in xmldata.findall('.//List2')]

		# writting the data in several chunks because of readability 
		pool.data.write(struct.pack("<32sI2H", b'', int(movie.attrib['flags1']), int(movie.attrib['flags2']),
									int(movie.attrib['flags3'])))
		pool.data.write(struct.pack("<3f", float(movie.attrib['float1']), float(movie.attrib['float2']),
									float(movie.attrib['float3'])))
		pool.data.write(struct.pack("<4B", 0, len(self.uitriggerlist), 0, len(self.uinamelist)))
		pool.data.write(struct.pack("<4B", 0, 0, len(self.Count1List), len(self.Count2List)))
		pool.data.write(struct.pack("<4B", len(self.uiInterfacelist), 0, 0, 0))
		pool.data.write(struct.pack("<80s", b''))

		# write name and add ptr
		nameptr = pool.data.tell()
		pool.data.write(f"{movie.attrib['MovieName']}\00".encode('utf-8'))
		new_frag = self.create_fragment()
		new_frag.pointers[0].pool = pool
		new_frag.pointers[0].data_offset = offset + 0x00
		new_frag.pointers[1].pool = pool
		new_frag.pointers[1].data_offset = nameptr

		# write pkgname and add ptr
		nameptr = pool.data.tell()
		pool.data.write(f"{movie.attrib['PkgName']}\00".encode('utf-8'))
		new_frag = self.create_fragment()
		new_frag.pointers[0].pool = pool
		new_frag.pointers[0].data_offset = offset + 0x08
		new_frag.pointers[1].pool = pool
		new_frag.pointers[1].data_offset = nameptr

		# write CategoryName and add ptr
		nameptr = pool.data.tell()
		pool.data.write(f"{movie.attrib['CategoryName']}\00".encode('utf-8'))
		new_frag = self.create_fragment()
		new_frag.pointers[0].pool = pool
		new_frag.pointers[0].data_offset = offset + 0x10
		new_frag.pointers[1].pool = pool
		new_frag.pointers[1].data_offset = nameptr

		# write TypeName and add ptr
		nameptr = pool.data.tell()
		pool.data.write(f"{movie.attrib['TypeName']}\00".encode('utf-8'))
		new_frag = self.create_fragment()
		new_frag.pointers[0].pool = pool
		new_frag.pointers[0].data_offset = offset + 0x18
		new_frag.pointers[1].pool = pool
		new_frag.pointers[1].data_offset = nameptr

		# write triggers at offset+0x48
		if len(self.uitriggerlist):

			# offset where first string starts
			doffset = pool.data.tell()

			# pack data now.. we are not doing rstrip to the lines.. worth considering to remove extra spaces
			pool.data.write("\00".join(self.uitriggerlist).encode('utf-8'))
			pool.data.write(b"\00")

			# new offset for list pointers
			poffset = pool.data.tell()

			# point the list frag to the end of the data now.
			new_frag0 = self.create_fragment()
			new_frag0.pointers[0].pool = pool
			new_frag0.pointers[0].data_offset = offset + 0x48
			new_frag0.pointers[1].pool = pool
			new_frag0.pointers[1].data_offset = poffset

			# for each line, add the frag ptr space and create the frag ptr
			for x in self.uitriggerlist:
				pool.data.write(struct.pack("<8s", b''))
				strfrag = self.create_fragment()
				strfrag.pointers[0].pool = pool
				strfrag.pointers[0].data_offset = poffset
				strfrag.pointers[1].pool = pool
				strfrag.pointers[1].data_offset = doffset

				poffset += 8
				doffset += len(x) + 1  # skip string lenght

		# write Controls at offset+0x58
		if self.uinamelist:

			# offset where first string starts
			doffset = pool.data.tell()

			# pack data now.. we are not doing rstrip to the lines.. worth considering to remove extra spaces
			pool.data.write("\00".join(self.uinamelist).encode('utf-8'))
			pool.data.write(b"\00")

			# new offset for list pointers
			poffset = pool.data.tell()

			# point the list frag to the end of the data now.
			new_frag0 = self.create_fragment()
			new_frag0.pointers[0].pool = pool
			new_frag0.pointers[0].data_offset = offset + 0x58
			new_frag0.pointers[1].pool = pool
			new_frag0.pointers[1].data_offset = poffset

			# for each line, add the frag ptr space and create the frag ptr
			for x in self.uinamelist:
				pool.data.write(struct.pack("<8s", b''))
				strfrag = self.create_fragment()
				strfrag.pointers[0].pool = pool
				strfrag.pointers[0].data_offset = poffset
				strfrag.pointers[1].pool = pool
				strfrag.pointers[1].data_offset = doffset

				poffset += 8
				doffset += len(x) + 1  # skip string lenght

		# write List1 at offset+0x70
		if len(self.Count1List):
			# offset where first string starts
			doffset = pool.data.tell()

			# pack data now.. 
			pool.data.write(struct.pack(f"<{len(self.Count1List)}I", *self.Count1List))
			# add some extra 00
			pool.data.write(struct.pack("<Q", 0))

			# point the list frag to the end of the data now.
			new_frag0 = self.create_fragment()
			new_frag0.pointers[0].pool = pool
			new_frag0.pointers[0].data_offset = offset + 0x70
			new_frag0.pointers[1].pool = pool
			new_frag0.pointers[1].data_offset = doffset

		# write List2 at offset+0x78
		if len(self.Count2List):
			# offset where first string starts
			doffset = pool.data.tell()

			# pack data now.. 
			pool.data.write(struct.pack(f"<{len(self.Count2List)}I", *self.Count2List))
			# add some extra 00
			pool.data.write(struct.pack("<Q", 0))

			# point the list frag to the end of the data now.
			new_frag0 = self.create_fragment()
			new_frag0.pointers[0].pool = pool
			new_frag0.pointers[0].data_offset = offset + 0x78
			new_frag0.pointers[1].pool = pool
			new_frag0.pointers[1].data_offset = doffset

		# write interfaces at offset+0x80
		if len(self.uiInterfacelist):

			# offset where first string starts
			doffset = pool.data.tell()

			# pack data now.. we are not doing rstrip to the lines.. worth considering to remove extra spaces
			pool.data.write("\00".join(self.uiInterfacelist).encode('utf-8'))
			pool.data.write(b"\00")
			# new offset for list pointers
			poffset = pool.data.tell()

			# point the list frag to the end of the data now.
			new_frag0 = self.create_fragment()
			new_frag0.pointers[0].pool = pool
			new_frag0.pointers[0].data_offset = offset + 0x80
			new_frag0.pointers[1].pool = pool
			new_frag0.pointers[1].data_offset = poffset

			# for each line, add the frag ptr space and create the frag ptr
			for x in self.uiInterfacelist:
				pool.data.write(struct.pack("<8s", b''))
				strfrag = self.create_fragment()
				strfrag.pointers[0].pool = pool
				strfrag.pointers[0].data_offset = poffset
				strfrag.pointers[1].pool = pool
				strfrag.pointers[1].data_offset = doffset

				poffset += 8
				doffset += len(x) + 1  # skip string lenght

	def collect(self):
		self.assign_ss_entry()
		logging.info(f"Collecting {self.sized_str_entry.name}")

		# it is a long struct
		unpackstr = "<32sI2H3f12B80s"
		_, self.flags1, self.flags2, self.flags3, self.float1, self.float2, self.float3, counta, count4, countc, ctrlcount, assetpkgcount, countf, count1, count2, count3, countj, _, _, _ = \
			struct.unpack(unpackstr, self.sized_str_entry.pointers[0].read_from_pool(0x90))


		print(f"counta {counta}")
		print(f"count4 {count4}")
		print(f"countc {countc}")
		print(f"ctrlcount {ctrlcount}")
		print(f"assetpkgcount {assetpkgcount}")
		print(f"countf {countf}")
		print(f"count1 {count1}")
		print(f"count2 {count2}")
		print(f"count3 {count3}")
		print(f"countj {countj}")

		# get name
		tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
		self.MovieName = self.p1_ztsr(tmpfragment)

		# get package (guess)
		tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
		self.PkgName = self.p1_ztsr(tmpfragment)

		# get category (guess)
		tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
		self.CategoryName = self.p1_ztsr(tmpfragment)

		# get type
		tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
		self.TypeName = self.p1_ztsr(tmpfragment)

		# will be finding frags now depending on the counts, starting with count4
		# corresponding to a list of strings of UI events/triggers
		self.uitriggerlist = []
		if count4:
			uilistfrag = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			tmpfragments = self.ovs.frags_from_pointer(uilistfrag.pointers[1], count4)
			for frag in tmpfragments:
				self.uitriggerlist.append(self.p1_ztsr(frag))

		# will be finding frags now depending on the counts, starting with count4
		# corresponding to a list of strings of UI events/triggers
		self.assetpkglist = []
		if assetpkgcount:
			assetpkgfrag = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			tmpfragments = self.ovs.frags_from_pointer(assetpkgfrag.pointers[1], assetpkgcount)
			for frag in tmpfragments:
				self.assetpkglist.append(self.p1_ztsr(frag))

		# list of UI controls
		self.uinamelist = []
		if ctrlcount:
			uilistfrag = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			tmpfragments = self.ovs.frags_from_pointer(uilistfrag.pointers[1], ctrlcount)
			for frag in tmpfragments:
				self.uinamelist.append(self.p1_ztsr(frag))
				
		self.Count1List = []
		if count1:
			tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			self.Count1List = list(struct.unpack(f"<{count1}I", tmpfragment.pointers[1].read_from_pool(0x4 * count1)))
		
		self.Count2List = []
		if count2:
			tmpfragment = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			self.Count2List = list(struct.unpack(f"<{count2}I", tmpfragment.pointers[1].read_from_pool(0x4 * count2)))

		self.uiInterfacelist = []
		if count3:
			uilistfrag = self.ovs.frags_from_pointer(self.sized_str_entry.pointers[0], 1)[0]
			tmpfragments = self.ovs.frags_from_pointer(uilistfrag.pointers[1], count3)
			for frag in tmpfragments:
				self.uiInterfacelist.append(self.p1_ztsr(frag))

	def load(self, file_path):
		pass

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		logging.info(f"Writing {name}")

		xmldata = ET.Element('UIMovieDefinition')
		xmldata.set('MovieName', str(self.MovieName))
		xmldata.set('PkgName', str(self.PkgName))
		xmldata.set('CategoryName', str(self.CategoryName))
		xmldata.set('TypeName', str(self.TypeName))
		xmldata.set('flags1', str(self.flags1))
		xmldata.set('flags2', str(self.flags2))
		xmldata.set('flags3', str(self.flags3))
		xmldata.set('float1', str(self.float1))
		xmldata.set('float2', str(self.float2))
		xmldata.set('float3', str(self.float3))

		for cl in self.uitriggerlist:
			clitem = ET.SubElement(xmldata, 'UITrigger')
			clitem.text = cl

		for cl in self.uinamelist:
			clitem = ET.SubElement(xmldata, 'Control')
			clitem.text = cl

		for cl in self.assetpkglist:
			clitem = ET.SubElement(xmldata, 'AssetPackage')
			clitem.text = cl

		for cl in self.uiInterfacelist:
			clitem = ET.SubElement(xmldata, 'Interface')
			clitem.text = cl

		for cl in self.Count1List:
			clitem = ET.SubElement(xmldata, 'List1')
			clitem.text = str(cl)

		for cl in self.Count2List:
			clitem = ET.SubElement(xmldata, 'List2')
			clitem.text = str(cl)

		out_path = out_dir(name)
		self.write_xml(out_path, xmldata)
		return out_path,
