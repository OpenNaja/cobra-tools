from generated.formats.fgm.compound.FgmInfoHeader import FgmInfoHeader
from generated.io import IoFile, BinaryStream
import os
import struct

# maps FGM dtype to struct dtype
# dtypes = {0:"f", 1:"ff", 2:"fff", 3:"ffff", 4:"I", 5:"i", 6:"i", 8:"I"}
dtypes = {0: "f", 1: "ff", 2: "fff", 3: "ffff", 5: "i", 6: "i"}


class FgmFile(FgmInfoHeader, IoFile):

	@property
	def game(self, ):
		# JWE style
		if self.flag_2 == 24724:
			return "Jurassic World Evolution"
		# PC style
		elif self.version == 18:
			return "Planet Coaster"
		# PZ Style
		elif self.flag_2 == 8340:
			return "Planet Zoo"
		else:
			return "Unknown Game"

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

			self.zeros_bytes = stream.read(self.zeros_size)
			data_start = stream.tell()
			self.data_bytes = stream.read(self.data_lib_size)
			self.buffer_bytes = stream.read()

			name_start = data_start + self.data_lib_size
			self.shader_name = self.read_z_str(stream, name_start)
			for texture in self.textures:
				texture.name = self.read_z_str(stream, name_start + texture.offset)
				# convert to bool
				texture.textured = texture.is_textured == 8
				if texture.textured:
					texture.value = list(x for x in texture.indices)
				else:
					texture.value = list(x for x in texture.colors)

			# read float / bool / int values
			for attrib in self.attributes:
				attrib.name = self.read_z_str(stream, name_start + attrib.offset)
				fmt = dtypes[attrib.dtype]
				stream.seek(data_start + attrib.first_value_offset)
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
			attrib.first_value_offset = data_writer.tell()
			fmt = dtypes[attrib.dtype]
			b = struct.pack("<" + fmt, *attrib.value)
			data_writer.write(b)
		for texture in self.textures:
			if texture.textured:
				for i in range(len(texture.indices)):
					# uint - hashes
					texture.indices[i] = max(0, texture.value[i])
			texture.offset = names_writer.tell()
			names_writer.write_zstring(texture.name)

		# write the output stream
		with self.writer(filepath) as stream:
			self.write(stream)
			stream.write(b"\x00" * self.zeros_size)
			stream.write(data_writer.getvalue())
			stream.write(names_writer.getvalue())


if __name__ == "__main__":
	fgm = FgmFile()
	fgm.load("C:/Users/arnfi/Desktop/parrot/parrot.fgm")
	fgm.save("C:/Users/arnfi/Desktop/parrot/parrot2.fgm")
	# print(fgm)
