import struct

from modules.formats.BaseFormat import BaseFile
from modules.formats.shared import get_versions, djb
from modules.helpers import as_bytes
from generated.formats.fgm import FgmFile


class FgmLoader(BaseFile):

	def create(self):
		pass

	def collect(self):
		self.assign_ss_entry()
		self.sized_str_entry.fragments = self.ovs.get_frag_after_terminator(self.sized_str_entry.pointers[0], (24, 32))

	def load(self, file_path):

		versions = get_versions(self.ovl)
		fgm_data = FgmFile()
		fgm_data.load(file_path)

		sizedstr_bytes = as_bytes(fgm_data.fgm_info, version_info=versions) + as_bytes(fgm_data.two_frags_pad,
																					   version_info=versions)

		# todo - move texpad into fragment padding?
		textures_bytes = as_bytes(fgm_data.textures, version_info=versions) + as_bytes(fgm_data.texpad,
																					   version_info=versions)
		attributes_bytes = as_bytes(fgm_data.attributes, version_info=versions)

		# the actual injection
		self.sized_str_entry.data_entry.update_data((fgm_data.buffer_bytes,))
		self.sized_str_entry.pointers[0].update_data(sizedstr_bytes, update_copies=True)

		if len(self.sized_str_entry.fragments) == 4:
			datas = (textures_bytes, attributes_bytes, fgm_data.zeros_bytes, fgm_data.data_bytes)
		# fgms without dependencies
		elif len(self.sized_str_entry.fragments) == 3:
			datas = (textures_bytes, attributes_bytes, fgm_data.data_bytes)
		# fgms for variants
		elif len(self.sized_str_entry.fragments) == 2:
			datas = (attributes_bytes, fgm_data.data_bytes)
		else:
			raise AttributeError("Unexpected fgm frag count")

		# inject fragment datas
		for frag, data in zip(self.sized_str_entry.fragments, datas):
			frag.pointers[1].update_data(data, update_copies=True)

		# update dependencies on ovl
		for dep_entry, tex_name in zip(self.file_entry.dependencies, fgm_data.texture_names):
			dep_entry.basename = tex_name
			dep_entry.name = dep_entry.basename + dep_entry.ext.replace(":", ".")
			dep_entry.file_hash = djb(tex_name.lower())

	def extract(self, out_dir, show_temp_files, progress_callback):
		name = self.sized_str_entry.name
		print("\nWriting", name)
		try:
			buffer_data = self.sized_str_entry.data_entry.buffer_datas[0]
			print("buffer size", len(buffer_data))
		except:
			print("Found no buffer data for", name)
			buffer_data = b""
		# basic fgms
		# zeros is the ptr to the dependencies block, which is only present if they are present
		if len(self.sized_str_entry.fragments) == 4:
			tex_info, attr_info, zeros, data_lib = self.sized_str_entry.fragments
			len_tex_info = tex_info.pointers[1].data_size
			len_zeros = zeros.pointers[1].data_size
		# no zeros, otherwise same as basic
		elif len(self.sized_str_entry.fragments) == 3:
			tex_info, attr_info, data_lib = self.sized_str_entry.fragments
			len_tex_info = tex_info.pointers[1].data_size
			len_zeros = 0
		# fgms for variants
		elif len(self.sized_str_entry.fragments) == 2:
			attr_info, data_lib = self.sized_str_entry.fragments
			len_tex_info = 0
			len_zeros = 0
		else:
			raise AttributeError("Fgm length is wrong")
	
		# write fgm
		fgm_header = struct.pack("<6I", len(self.sized_str_entry.fragments), len(self.file_entry.dependencies),
			len_tex_info, attr_info.pointers[1].data_size, len_zeros, data_lib.pointers[1].data_size,)
	
		# print(file_entry.textures)
		out_path = out_dir(name)
		# for i, f in enumerate(sized_str_entry.fragments):
		# 	with open(out_path+str(i), 'wb') as outfile:
		# 		outfile.write( f.pointers[1].data )
		with open(out_path, 'wb') as outfile:
			# write custom FGM header
			outfile.write(self.pack_header(b"FGM "))
			outfile.write(fgm_header)
			for tex in self.file_entry.dependencies:
				outfile.write(tex.basename.encode())
				outfile.write(b"\x00")
			outfile.write(self.sized_str_entry.pointers[0].data)
			# write each of the fragments
			for frag in self.sized_str_entry.fragments:
				outfile.write(frag.pointers[1].data)
			# write the buffer
			outfile.write(buffer_data)
		return out_path,
