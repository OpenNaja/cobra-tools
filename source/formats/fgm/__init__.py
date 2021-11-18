from generated.formats.fgm.compound.FgmInfoHeader import FgmInfoHeader
from generated.io import IoFile, BinaryStream
import os
import struct

# maps FGM dtype to struct dtype
# dtypes = {0:"f", 1:"ff", 2:"fff", 3:"ffff", 4:"I", 5:"i", 6:"i", 8:"I"}
dtypes = {0: "f", 1: "ff", 2: "fff", 3: "ffff", 5: "i", 6: "i"}


class FgmContext(object):
	def __init__(self):
		self.version = 0
		self.user_version = 0

	def __repr__(self):
		return f"{self.version} | {self.user_version}"


class FgmFile(FgmInfoHeader, IoFile):

	def __init__(self):
		super().__init__(FgmContext())

	@staticmethod
	def read_z_str(stream, pos):
		stream.seek(pos)
		return stream.read_zstring()

	def load(self, filepath):
		# store file name for later
		self.file = filepath
		self.dir, self.basename = os.path.split(filepath)
		self.file_no_ext = os.path.splitext(self.file)[0]

		with self.reader(filepath) as stream:
			self.read(stream)
			self.eoh = stream.tell()
			# print(self)
			data_start = stream.tell()
			self.data_bytes = stream.read(self.data_lib_size)
			name_start = data_start + self.data_lib_size
			self.buffer_bytes = stream.read()
			self.shader_name = self.read_z_str(stream, name_start)
			for texture in self.textures:
				texture.name = self.read_z_str(stream, name_start + texture.offset)
				# convert to bool
				texture.textured = texture.is_textured == 8
				if texture.textured:
					texture.value = list(x for x in texture.indices)
					texture.file = self.texture_files[texture.indices[0]]
				else:
					texture.value = list(x for x in texture.colors)
					texture.file = None

			# read float / bool / int values
			for attrib in self.attributes:
				attrib.name = self.read_z_str(stream, name_start + attrib.offset)
				fmt = dtypes[attrib.dtype]
				stream.seek(data_start + attrib.value_offset)
				attrib.value = list(struct.unpack("<" + fmt, stream.read(struct.calcsize(fmt))))
				if attrib.dtype == 6:
					attrib.value = list(bool(v) for v in attrib.value)

		# self.print_readable()

	def print_readable(self, ):
		print("\nShader =", self.shader_name)
		print("\nTextures")
		for texture in self.textures:
			l = "(textured)" if texture.textured else ""
			s = '{} {} = {}'.format(texture.name, l, texture.value)
			print(s)
			print(texture)
			print()
		print("\nAttributes")
		for attrib in self.attributes:
			s = '{} = {}'.format(attrib.name, attrib.value)
			print(s)
			print(attrib)
			print()

	def save(self, filepath):
		names_writer = BinaryStream()
		data_writer = BinaryStream()
		# shader name is at 0
		names_writer.write_zstring(self.shader_name)
		# attribs are written first
		for attrib in self.attributes:
			attrib.offset = names_writer.tell()
			names_writer.write_zstring(attrib.name)
			attrib.value_offset = data_writer.tell()
			b = struct.pack(f"<{dtypes[attrib.dtype]}", *attrib.value)
			data_writer.write(b)
		self.texture_files.clear()
		for texture in self.textures:
			# if the texture has a file, store its index
			if texture.textured:
				texture.indices[0] = len(self.texture_files)
				self.texture_files.append(texture.file)
			texture.offset = names_writer.tell()
			names_writer.write_zstring(texture.name)
		# update counts
		data_bytes = data_writer.getvalue()
		self.data_lib_size = len(data_bytes)
		self.dependency_count = len(self.texture_files)
		self.fgm_info.texture_count = len(self.textures)
		self.fgm_info.attribute_count = len(self.attributes)
		# write the output stream
		with self.writer(filepath) as stream:
			self.write(stream)
			stream.write(data_bytes)
			stream.write(names_writer.getvalue())

	def get_attr_dict(self):
		return {attrib.name.lower(): attrib for attrib in self.attributes}

	def get_color_ramp(self, key_type, d_type):
		attr_dict = self.get_attr_dict()
		out = []
		for i in range(1, 13):
			try:
				k = f"u_{key_type}_{i:02}_Position"
				pos = attr_dict[k.lower()].value[0]
				k = f"u_{key_type}_{i:02}_{d_type}"
				rgb = attr_dict[k.lower()].value
				print(i, pos, rgb)
				out.append((pos, rgb))
			except:
				pass
		return out


if __name__ == "__main__":
	fgm = FgmFile()
	# fgm.load("C:/Users/arnfi/Desktop/parrot/parrot.fgm")
	# fgm.load("C:/Users/arnfi/Desktop/Coding/Frontier/JWE2/ichthyo/ichthyosaurus_pattern_01_04.fgm")
	fgm.load("C:/Users/arnfi/Desktop/Coding/Frontier/JWE2/ichthyo/ichthyosaurus.fgm")
	# fgm.load("C:/Users/arnfi/Desktop/Coding/Frontier/JWE2/ichthyo/ichthyosaurus_patternset_01.fgm")
	# fgm.get_color_ramp()
	# fgm.save("C:/Users/arnfi/Desktop/parrot/parrot2.fgm")
	print(fgm)
