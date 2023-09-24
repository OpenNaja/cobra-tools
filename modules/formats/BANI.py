import logging
import os
import struct

from generated.formats.bani import BanisInfoHeader
from generated.formats.bani.compounds.BanisRoot import BanisRoot
from generated.formats.bani.compounds.BaniRoot import BaniRoot
from modules.formats.BaseFormat import MemStructLoader
from modules.helpers import as_bytes


class BaniLoader(MemStructLoader):
	extension = ".bani"
	target_class = BaniRoot
	can_extract = False

	def create(self, file_path):
		pass

	def create_header(self, data, banis_loader):
		self.header = data
		self.write_memory_data()
		pool, _ = self.root_ptr
		# delete old link if it exists
		self.delete_frag(pool, self.header.banis.io_start, *banis_loader.root_ptr)
		self.attach_frag_to_ptr(pool, self.header.banis.io_start, *banis_loader.root_ptr)
		self.header.banis.link = banis_loader.root_ptr
		# print(self.fragments)


class BanisLoader(MemStructLoader):
	extension = ".banis"
	target_class = BanisRoot

	def validate(self):
		self.extra_loaders = []
		for loader in self.ovl.loaders.values():
			if loader.ext == ".bani":
				if self.root_ptr == loader.header.banis.link:
					self.extra_loaders.append(loader)
		self.extra_loaders.sort(key=lambda bani: bani.name)

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
			stream.write(struct.pack("<I", len(self.extra_loaders)))
			for bani in self.extra_loaders:
				stream.write(as_bytes(os.path.splitext(bani.name)[0]))
				bani.header.to_stream(bani.header, stream, bani.header.context)
			self.header.to_stream(self.header, stream, self.header.context)
			stream.write(buffers[0])
		return out_paths

	def create(self, file_path):
		with open(file_path, 'rb') as stream:
			banis = BanisInfoHeader.from_stream(stream, self.context)
			self.header = banis.data
			keys = stream.read()
		self.write_memory_data()
		self.extra_loaders = []
		for bani in banis.anims:
			bani_loader = self.ovl.create_file(f"dummy_dir/{bani.name}.bani")
			bani_loader.create_header(bani.data, self)
			self.extra_loaders.append(bani_loader)
		self.create_data_entry((keys,))


