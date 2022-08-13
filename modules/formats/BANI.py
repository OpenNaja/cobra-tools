import logging

from generated.formats.bani import BaniFile
from generated.formats.bani.compounds.BanisRoot import BanisRoot
from generated.formats.bani.compounds.BaniRoot import BaniRoot
from generated.formats.ovl_base.basic import ConvStream
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

	def collect(self):
		super().collect()
		self.target_name = self.find_banis_name()

	def update(self):
		# link frag to banis
		banis_loader = self.ovl.loaders.get(self.target_name, None)
		if not banis_loader:
			logging.warning(f"Could not find '{self.target_name}' for '{self.file_entry.name}'")
			return
		logging.debug(f"Linked '{self.file_entry.name}' to '{self.target_name}'")
		self.ptr_relative(self.header.banis.frag.struct_ptr, banis_loader.root_entry.struct_ptr)

	def extract(self, out_dir):
		logging.info(f"Writing {self.root_entry.name}")

		# find banis name
		banis_name = self.find_banis_name()

		# write bani file
		out_path = out_dir(self.root_entry.name)
		with open(out_path, 'wb') as outfile:
			outfile.write(b"BANI")
			outfile.write(as_bytes(banis_name))
			with ConvStream() as stream:
				self.header.write(stream)
				outfile.write(stream.getvalue())

		return out_path,

	def find_banis_name(self):
		for root_entry in self.ovs.root_entries:
			if self.header.banis.frag.struct_ptr == root_entry.struct_ptr:
				return root_entry.name
		return "None"


class BanisLoader(MemStructLoader):
	extension = ".banis"
	target_class = BanisRoot

	def extract(self, out_dir):
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
		root_data, buffer_0 = self._get_data(self.file_entry.path)
		self.create_root_entry()
		self.write_data_to_pool(self.root_entry.struct_ptr, self.file_entry.pool_type, root_data)
		self.create_data_entry((buffer_0,))

	@staticmethod
	def _get_data(file_path):
		with open(file_path, 'rb') as stream:
			header = stream.read(40)
			data = stream.read()
		return header, data


