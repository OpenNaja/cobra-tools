import logging

from generated.formats.uimoviedefinition.compound.UiMovieHeader import UiMovieHeader
from modules.formats.BaseFormat import BaseFile


class UIMovieDefinitionLoader(BaseFile):

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		self.header.to_xml_file(out_path)
		return out_path,

	def collect(self):
		self.assign_ss_entry()
		ss_ptr = self.sized_str_entry.pointers[0]
		self.header = UiMovieHeader.from_stream(ss_ptr.stream, self.ovl.context)
		self.header.read_ptrs(self.ovs, ss_ptr, self.sized_str_entry)
		print(self.header)

	def create(self):
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		ss_ptr = self.sized_str_entry.pointers[0]

		self.header = UiMovieHeader.from_xml_file(self.file_entry.path, self.ovl.context)
		print(self.header)
		self.header.write_ptrs(self, self.ovs, ss_ptr)
		# todo - may use wrong pools !
		# todo - may need padding here
