import struct

from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?


class MergeDetailsLoader(BaseFile):
	extension = ".mergedetails"

	def create(self):
		pass

	def collect(self):
		self.assign_ss_entry()
		print(f"Collecting {self.sized_str_entry.name}")

		# there is a count for a pointer list, but all mergedetails have only 1 in the count so it is hard to tell
		# which one of the pointer in the struct is affected by it.
		_,_,_,_,_,count,flags = struct.unpack("<5QII", self.sized_str_entry.struct_ptr.read_from_pool(0x30))

		self.sized_str_entry.mergedetails  = {
			'flags': flags,
			'count': count,
			'query': "test sql;",
			'name' : "DLCPacks", # hardcode value of all mergedetails seen
			'field': "ChildDB"   # hardcode value of all mergedetails seen
		}
		print(self.sized_str_entry.mergedetails)

		# first frag pointer points to a list of 1 item, the item being name: DLCPacks
		# second frag pointer points to a list of 1 item, the item being query: SELECT ....
		# third frag pointer points to a list of 1 item, the item geing field: ChildDB

		pass

	def load(self, file_path):
		pass

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		print(f"Writing {name}")		

		out_files = []
		out_path = out_dir(name)

		md = self.sized_str_entry.mergedetails

		xmldata = ET.Element('MergeDetails')
		xmldata.set('name',   str(md['name']))
		xmldata.set('field',  str(md['field']))
		xmldata.set('flags',  str(md['flags']))
		xmldata.set('count',  str(md['count']))
		xmldata.text = md['query']

		xmltext = ET.tostring(xmldata)

		with open(out_path, 'w') as outfile:
			outfile.write(xmltext.decode('utf-8'))
			out_files.append(out_path)
		    
		return out_files

