import os
import itertools
import struct
import io
import time

from generated.formats.ms2.compound.Ms2InfoHeader import Ms2InfoHeader
from generated.formats.ms2.compound.Mdl2InfoHeader import Mdl2InfoHeader
from generated.formats.ms2.compound.Ms2BoneInfo import Ms2BoneInfo
from generated.formats.ms2.compound.PcModel import PcModel
from generated.io import IoFile


def findall(p, s):
	'''Yields all the positions of
	the pattern p in the string s.'''
	i = s.find(p)
	while i != -1:
		yield i
		i = s.find(p, i+1)


class Ms2File(Ms2InfoHeader, IoFile):

	def __init__(self, ):
		super().__init__()

	def load(self, filepath, mdl2, quick=False, map_bytes=False):
		start_time = time.time()
		# eof = super().load(filepath)

		# extra stuff
		self.bone_info = None
		with self.reader(filepath) as stream:
			self.read(stream)
			# this is for the PC format
			# for mdl2_info in self.model_infos:
			#     pc_model = stream.read_type(PcModel, (mdl2_info,))
			#     print(pc_model)
			#     break
			self.eoh = stream.tell()
			print("end of header: ", self.eoh)
			# first get all bytes of the whole bone infos block
			bone_info_bytes = stream.read(self.bone_info_size)
			# find the start of each using this identifier
			zero_f = bytes.fromhex("00 00 00 00")
			one_f = bytes.fromhex("00 00 80 3F")
			# lion has a 1 instead of a 4
			bone_info_marker_1 = bytes.fromhex("FF FF 00 00 00 00 00 00 01")
			# this alone is not picky enough for mod_f_wl_unq_laboratory_corner_002_dst
			bone_info_marker_4 = bytes.fromhex("FF FF 00 00 00 00 00 00 04")
			# there's 8 bytes before this
			bone_info_starts = []
			for a, b in ((zero_f, bone_info_marker_1),
						 (one_f, bone_info_marker_1),
						 (zero_f, bone_info_marker_4),
						 (one_f, bone_info_marker_4),
						 ):
				bone_info_starts.extend(x - 4 for x in findall(a + b, bone_info_bytes))

			bone_info_starts = list(sorted(bone_info_starts))
			print("bone_info_starts", bone_info_starts)

			if bone_info_starts:
				idx = mdl2.index
				if idx >= len(bone_info_starts):
					print("reset boneinfo index")
					idx = 0
				bone_info_address = self.eoh + bone_info_starts[idx]
				print("using bone info {} at address {}".format(idx, bone_info_address))
				stream.seek(bone_info_address)
				self.bone_info = Ms2BoneInfo()
				self.bone_info.read(stream)
				print(self.bone_info)
				print("end of bone info at", stream.tell())

				self.bone_names = [self.names[i] for i in self.bone_info.name_indices]
			else:
				print("No bone info found")
				self.bone_names = []

		# numpy chokes on bytes io objects
		with open(filepath, "rb") as stream:
			stream.seek(self.eoh + self.bone_info_size)
			# get the starting position of buffer #2, vertex & face array
			self.start_buffer2 = stream.tell()
			print("vert array start", self.start_buffer2)
			print("tri array start", self.start_buffer2 + self.buffer_info.vertexdatasize)

			if not quick:
				base = mdl2.model_info.pack_offset
				for model in mdl2.models:
					model.populate(self, stream, self.start_buffer2, self.bone_names, base)

			if map_bytes:
				for model in mdl2.models:
					model.read_bytes_map(self.start_buffer2, stream)
				return


class Mdl2File(Mdl2InfoHeader, IoFile):

	def __init__(self, ):
		super().__init__()

	def load(self, filepath):

		self.file = filepath
		self.dir, self.basename = os.path.split(filepath)
		self.file_no_ext = os.path.splitext(self.file)[0]
		start_time = time.time()
		# eof = super().load(filepath)

		# read the file
		with self.reader(filepath) as stream:
			self.read(stream)
		# print(self)

		self.ms2_path = os.path.join(self.dir, self.name)
		self.ms2_file = Ms2File()
		self.ms2_file.load(self.ms2_path, self, )

		# set material links
		for mat_1 in self.materials_1:
			try:
				name = self.ms2_file.names[mat_1.material_index]
				model = self.models[mat_1.model_index]
				model.material = name
			except:
				print(f"Couldn't match material {mat_1.material_index} to model {mat_1.model_index} - bug?")
		# todo - doesn't seem to be correct, at least not for JWE dinos
		self.lod_names = [self.ms2_file.names[lod.strznameidx] for lod in self.lods]
		print("lod_names", self.lod_names)
		print(f"Finished reading in {time.time() - start_time:.2f} seconds!")


if __name__ == "__main__":
	m = Mdl2File()
	m.load("C:/Users/arnfi/Desktop/prim/models.ms2")
	print(m)
