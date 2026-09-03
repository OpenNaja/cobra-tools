import struct

from generated.formats.bani import BanisFile
from generated.formats.bani.structs.BanisRoot import BanisRoot
from generated.formats.bani.structs.BaniRoot import BaniRoot
from modules.formats.BaseFormat import MimeVersionedLoader
from modules.helpers import as_bytes


class BaniLoader(MimeVersionedLoader):
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


class BanisLoader(MimeVersionedLoader):
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
		assert self.data_entry, f"No data entry for {name}"
		buffers = self.data_entry.buffer_datas
		assert len(buffers) == 1, f"Wrong amount of buffers for {name}"
		out_path = out_dir(name)
		with open(out_path, 'wb') as stream:
			stream.write(struct.pack("<II", self.mime_version, len(self.extra_loaders)))
			for bani in self.extra_loaders:
				stream.write(as_bytes(bani.basename))
				bani.header.to_stream(bani.header, stream, bani.header.context)
			self.header.to_stream(self.header, stream, self.header.context)
			# write the keys themselves
			if self.mime_version < 7:
				stream.write(buffers[0])
			else:
				for ptr in (self.header.gpu_anim_headers, self.header.channel_bones, self.header.channel_bones_lod, self.header.keys):
					ptr.data.to_stream(ptr.data, stream, self.header.context)
		return out_path,

	def create(self, file_path):
		banis = BanisFile()
		banis.load(file_path)
		self.header = banis.data
		self.write_memory_data()
		self.extra_loaders = []
		for bani in banis.anims:
			bani_name = f"{bani.name}.bani"
			bani_loader = self.ovl.create_file(f"dummy_dir/{bani_name}", bani_name)
			bani_loader.create_header(bani.data, self)
			self.extra_loaders.append(bani_loader)
		# newer versions store keys on the header
		if banis.version < 7:
			self.create_data_entry((banis.keys_bytes, ))
		else:
			# this dummy data is required
			self.create_data_entry((struct.pack("<IIII", 47, 4747, 474747, 47474747), ))


