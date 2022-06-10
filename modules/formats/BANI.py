import logging

from generated.formats.bani import BaniFile
from generated.formats.bani.compound.BanisRoot import BanisRoot
from generated.formats.bani.compound.BaniRoot import BaniRoot
from modules.formats.BaseFormat import MemStructLoader
from modules.helpers import as_bytes


class BaniLoader(MemStructLoader):
	extension = ".bani"
	target_class = BaniRoot

	def create(self):
		bani = BaniFile()
		bani.load(self.file_entry.path)
		self.header = bani.data
		self.create_root_entry()
		self.header.write_ptrs(self, self.root_ptr, self.file_entry.pool_type)
		# create banis fragment, link it during update
		self.attach_frag_to_ptr(self.header.banis, self.root_ptr.pool)
		# temporarily set frag so that register_ptrs works
		self.ptr_relative(self.header.banis.frag.struct_ptr, self.root_entry.struct_ptr)
		# store banis name for linking
		self.target_name = bani.banis_name

	def update(self):
		# link frag to banis
		banis_loader = self.ovl.loaders.get(self.target_name, None)
		if not banis_loader:
			logging.warning(f"Could not find '{self.target_name}' for '{self.file_entry.name}'")
			return
		logging.info(f"Linked '{self.file_entry.name}' to '{self.target_name}'")
		self.ptr_relative(self.header.banis.frag.struct_ptr, banis_loader.root_entry.struct_ptr)

	def extract(self, out_dir, show_temp_files, progress_callback):
		logging.info(f"Writing {self.root_entry.name}")

		# find banis name
		for root_entry in self.ovs.root_entries:
			if self.header.banis.frag.struct_ptr == root_entry.struct_ptr:
				banis_name = root_entry.name
				break
		else:
			banis_name = "None"

		# write bani file
		out_path = out_dir(self.root_entry.name)
		with open(out_path, 'wb') as outfile:
			outfile.write(b"BANI")
			outfile.write(as_bytes(banis_name))
			self.header.write(outfile)

		return out_path,


class BanisLoader(MemStructLoader):
	extension = ".banis"
	target_class = BanisRoot

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.root_entry.name
		if not self.data_entry:
			raise AttributeError(f"No data entry for {name}")
		buffers = self.data_entry.buffer_datas
		if len(buffers) != 1:
			raise AttributeError(f"Wrong amount of buffers for {name}")
		logging.info(f"Writing {name}")
		out_path = out_dir(name)
		out_paths = [out_path, ]
		with open(out_path, 'wb') as outfile:
			self.header.write(outfile)
			outfile.write(buffers[0])

		return out_paths

	def create(self):
		# create banis data
		root_entry, buffer_0 = self._get_data(self.file_entry.path)
		self.create_root_entry()
		self.write_data_to_pool(self.root_entry.struct_ptr, self.file_entry.pool_type, root_entry)
		self.create_data_entry((buffer_0,))

	@staticmethod
	def _get_data(file_path):
		with open(file_path, 'rb') as stream:
			header = stream.read(40)
			data = stream.read()
		return header, data


