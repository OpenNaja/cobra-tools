from generated.formats.bnk.compound.BKHDSection import BKHDSection
from generated.formats.bnk.compound.DIDXSection import DIDXSection
# from generated.formats.bnk.compound.DATASection import DATASection
import os


class AuxFileContainer:
	# Custom file struct

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.chunks = []
		self.bhkd = None
		self.didx = None
		self.data = None

	def read(self, stream):
		self.chunks = []
		chunk_id = "DUMM"
		while len(chunk_id) == 4:
			chunk_id = stream.read(4)
			print("reading chunk", chunk_id)
			if chunk_id == b"BKHD":
				self.bhkd = stream.read_type(BKHDSection)
				self.chunks.append(self.bhkd)
			elif chunk_id == b"DIDX":
				self.didx = stream.read_type(DIDXSection)
				self.chunks.append(self.didx)
			elif chunk_id == b"DATA":
				size = stream.read_uint()
				self.data = stream.read(size)
			elif chunk_id == b'\x00\x00\x00\x00':
				break
		for pointer in self.didx.data_pointers:
			pointer.data = self.data[pointer.data_section_offset: pointer.data_section_offset+pointer.wem_filesize]

	def extract_audio(self, out_dir):
		print("Extracting audio")
		paths = []
		for pointer in self.didx.data_pointers:
			wem_name = f"{pointer.wem_id}.wem"
			wem_path = os.path.normpath(os.path.join(out_dir, wem_name))
			paths.append(wem_path)
			print(wem_path)
			with open(wem_path, "wb") as f:
				f.write(pointer.data)
		return paths

	def write(self, stream):
		for chunk in self.chunks:
			stream.write_type(chunk)

	def __repr__(self):
		s = 'AuxFileContainer'
		for chunk in self.chunks:
			s += '\nchunk ' + chunk.__repr__()
		s += '\n'
		return s