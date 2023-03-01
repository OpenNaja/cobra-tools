import logging

from generated.formats.bani import BaniFile
from generated.formats.bani.compounds.BanisRoot import BanisRoot
from generated.formats.bani.compounds.BaniRoot import BaniRoot
from modules.formats.BaseFormat import MemStructLoader
from modules.helpers import as_bytes


class BaniLoader(MemStructLoader):
	extension = ".bani"
	target_class = BaniRoot

	def create(self, file_path):
		bani = BaniFile()
		bani.load(file_path)
		self.header = bani.data
		self.create_root_entry()
		self.header.write_ptrs(self, self.root_ptr, self.pool_type)
		# create banis fragment, link it during update
		self.attach_frag_to_ptr(self.header.banis, self.root_ptr.pool)
		# temporarily set frag so that register_ptrs works
		self.ptr_relative(self.header.banis.frag.struct_ptr, self.root_entry.struct_ptr)
		# store banis name for linking
		self.target_name = bani.banis_name

	def collect(self):
		super().collect()
		self.target_name = None

	def validate(self):
		self.target_name = self.find_banis_name()
		logging.debug(f"Found {self.target_name}")

	def update(self):
		# link frag to banis
		banis_loader = self.ovl.loaders.get(self.target_name, None)
		if not banis_loader:
			logging.warning(f"Could not find '{self.target_name}' for '{self.name}'")
			return
		logging.debug(f"Linked '{self.name}' to '{self.target_name}'")
		# todo - update api
		# self.ptr_relative(self.header.banis.frag.struct_ptr, banis_loader.root_entry.struct_ptr)

	def extract(self, out_dir):
		logging.info(f"Writing {self.name}")

		# find banis name
		banis_name = self.find_banis_name()

		# write bani file
		out_path = out_dir(self.name)
		with open(out_path, 'wb') as stream:
			stream.write(b"BANI")
			stream.write(as_bytes(banis_name))
			self.header.to_stream(self.header, stream, self.header.context)

		return out_path,

	def find_banis_name(self):
		for loader in self.ovl.loaders.values():
			if loader.ext == ".banis":
				if loader.root_ptr == self.header.banis.link:
					return loader.name
		return "None"


class BanisLoader(MemStructLoader):
	extension = ".banis"
	target_class = BanisRoot

	def extract(self, out_dir):
		name = self.name
		if not self.data_entry:
			raise AttributeError(f"No data entry for {name}")
		buffers = self.data_entry.buffer_datas
		if len(buffers) != 1:
			raise AttributeError(f"Wrong amount of buffers for {name}")
		logging.info(f"Writing {name}")
		out_path = out_dir(name)
		out_paths = [out_path, ]
		with open(out_path, 'wb') as stream:
			self.header.to_stream(self.header, stream, self.header.context)
			stream.write(buffers[0])

		return out_paths

	def create(self, file_path):
		with open(file_path, 'rb') as stream:
			self.header = self.target_class.from_stream(stream, self.context)
			data = stream.read()
		# self.create_root_entry()
		self.write_memory_data()
		self.create_data_entry((data,))


