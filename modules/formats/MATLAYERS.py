import logging

from generated.formats.dinosaurmaterialvariants.compound.DinoEffectsHeader import DinoEffectsHeader
from generated.formats.dinosaurmaterialvariants.compound.DinoLayersHeader import DinoLayersHeader
from generated.formats.dinosaurmaterialvariants.compound.DinoPatternsHeader import DinoPatternsHeader
from generated.formats.dinosaurmaterialvariants.compound.DinoVariantsHeader import DinoVariantsHeader
from modules.formats.BaseFormat import BaseFile


class MatlayersLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		ss_ptr = self.sized_str_entry.pointers[0]
		self.header = DinoLayersHeader.from_stream(ss_ptr.stream, self.ovl.context)
		self.header.read_ptrs(self.ovs, ss_ptr)
		# print(self.header)

	def load(self, file_path):
		self.header = DinoLayersHeader.from_xml_file(file_path, self.ovl.context)
		# print(self.header)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		self.header.to_xml_file(out_path)
		return out_path,

	def create(self):
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		ss_ptr = self.sized_str_entry.pointers[0]
		self.header = DinoLayersHeader.from_xml_file(self.file_entry.path, self.ovl.context)
		# print(self.header)
		self.header.write_ptrs(self, self.ovs, ss_ptr)
		# todo - may use wrong pools !
		# todo - may need padding here


class MatvarsLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		ss_ptr = self.sized_str_entry.pointers[0]
		self.header = DinoVariantsHeader.from_stream(ss_ptr.stream, self.ovl.context)
		self.header.read_ptrs(self.ovs, ss_ptr)
		# print(self.header)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		self.header.to_xml_file(out_path)
		return out_path,

	def create(self):
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		ss_ptr = self.sized_str_entry.pointers[0]

	def load(self, file_path):
		self.header = DinoVariantsHeader.from_xml_file(file_path, self.ovl.context)
		# print(self.header)


class MateffsLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		ss_ptr = self.sized_str_entry.pointers[0]
		self.header = DinoEffectsHeader.from_stream(ss_ptr.stream, self.ovl.context)
		self.header.read_ptrs(self.ovs, ss_ptr)
		print(self.header)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		self.header.to_xml_file(out_path)
		return out_path,


class MatpatsLoader(BaseFile):

	def collect(self):
		self.assign_ss_entry()
		ss_ptr = self.sized_str_entry.pointers[0]
		self.header = DinoPatternsHeader.from_stream(ss_ptr.stream, self.ovl.context)
		self.header.read_ptrs(self.ovs, ss_ptr)
		# print(self.header)

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		out_path = out_dir(name)
		self.header.to_xml_file(out_path)
		return out_path,

	def create(self):
		self.sized_str_entry = self.create_ss_entry(self.file_entry)
		ss_ptr = self.sized_str_entry.pointers[0]

		self.header = DinoPatternsHeader.from_xml_file(self.file_entry.path, self.ovl.context)
		# print(self.header)
		self.header.write_ptrs(self, self.ovs, ss_ptr)
		# todo - may use wrong pools !
		# todo - may need padding here

	def load(self, file_path):
		self.header = DinoPatternsHeader.from_xml_file(file_path, self.ovl.context)
		# print(self.header)
		# todo
