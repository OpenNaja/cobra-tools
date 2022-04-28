import logging

from generated.formats.fgm.compound.AttributeInfo import AttributeInfo
from generated.formats.fgm.basic import basic_map
from generated.formats.fgm.compound.FgmInfoHeader import FgmInfoHeader
from generated.formats.fgm.compound.TextureInfo import TextureInfo
from generated.formats.ovl_base import OvlContext
from generated.formats.ovl_base.basic import ConvStream
from generated.io import IoFile
import os
import struct

# maps FGM dtype to struct dtype
dtypes = {0: "f", 1: "ff", 2: "fff", 3: "ffff", 5: "i", 6: "i"}  # 4:"I", 8:"I"


class FgmFile(FgmInfoHeader, IoFile):

	basic_map = basic_map

	def __init__(self):
		super().__init__(OvlContext())
		self.magic.data = b'FGM '
		self.shader_name = ""

	@staticmethod
	def read_z_str(stream, pos):
		stream.seek(pos)
		return stream.read_zstring()

	def load(self, filepath):
		# store file name for later
		self.file = filepath
		self.dir, self.basename = os.path.split(filepath)
		self.path_no_ext = os.path.splitext(self.file)[0]

		with self.reader(filepath) as stream:
			self.read(stream)
			self.eoh = stream.tell()
			print(self)
			data_start = stream.tell()
			self.data_bytes = stream.read(self.data_lib_size)
			name_start = data_start + self.data_lib_size
			self.buffer_bytes = stream.read()
			self.shader_name = self.read_z_str(stream, name_start)
			for texture in self.textures:
				logging.debug(f"Reading at {name_start + texture.offset}")
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
				stream.seek(data_start + attrib.value_offset)
				self.get_value(attrib, stream)
				if attrib.dtype == 6:
					attrib.value = list(bool(v) for v in attrib.value)

	def get_value(self, attrib, stream=None):
		fmt = dtypes[attrib.dtype]
		d_size = struct.calcsize(fmt)
		if stream:
			data = stream.read(d_size)
		else:
			data = b"\x00" * d_size
		attrib.value = list(struct.unpack(f"<{fmt}", data))

	def add_attrib(self, attr_name, attr_dtype):
		for attrib in self.attributes:
			if attrib.name == attr_name:
				logging.debug(f"Attribute '{attr_name}' already exists")
				return
		logging.debug(f"Adding attribute '{attr_name}'")
		attrib = AttributeInfo(self.context)
		attrib.name = attr_name
		attrib.dtype = attr_dtype
		self.get_value(attrib)
		self.attributes.append(attrib)
		self.attributes.sort(key=lambda a: a.name)

	def add_texture(self, tex_name, textured=True):
		for tex in self.textures:
			if tex.name == tex_name:
				logging.debug(f"Texture '{tex_name}' already exists")
				return
		logging.debug(f"Adding attribute '{tex_name}'")
		tex = TextureInfo(self.context)
		tex.name = tex_name
		tex.textured = textured
		if textured:
			tex.file = tex_name.lower()
			tex.is_textured = 8
		else:
			raise NotImplementedError(f"Unsure how to create texture '{tex_name}'")
		tex.indices.resize(4)
		self.textures.append(tex)
		self.textures.sort(key=lambda t: t.name)

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
		names_writer = ConvStream()
		data_writer = ConvStream()
		# shader name is at 0
		names_writer.write_zstring(self.shader_name)
		names_writer.write(b"\x00")
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
