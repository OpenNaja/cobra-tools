import struct

from modules.formats.BaseFormat import BaseFile
import xml.etree.ElementTree as ET # prob move this to a custom modules.helpers or utils?


class LogicalControlsLoader(BaseFile):

	def create(self):
		pass

	def collect(self):
		self.assign_ss_entry()
		print(f"Collecting {self.sized_str_entry.name}")

		pass

	def load(self, file_path):
		pass

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		print(f"Writing {name}")		

		out_files = []
		    
		return out_files

