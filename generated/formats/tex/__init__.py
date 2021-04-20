import io

from generated.formats.dds.struct.Header import Header
from generated.formats.dds.enum.D3D10ResourceDimension import D3D10ResourceDimension
from generated.io import IoFile


class DdsFile(Header, IoFile):

	def __init__(self,):
		super().__init__()
		self.buffer = b""
		self.emmpty_block = b""
		self.mips = []

	def load(self, filepath):
		with self.reader(filepath) as stream:
			self.read(stream)
			self.read_mips(stream)

	def save(self, filepath):
		with self.writer(filepath) as stream:
			self.write(stream)
			stream.write(self.buffer)

	def read_mips(self, stream):
		print("\nReading mips")

		# get compression type
		comp = self.dx_10.dxgi_format.name

		# get bpp from compression type
		if "BC1" in comp or "BC4" in comp:
			self.pixels_per_byte = 2
			self.empty_block = bytes.fromhex("00 00 00 00 00 00 00 00")
		else:
			self.pixels_per_byte = 1
			self.empty_block = bytes.fromhex("00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")
		min_bytes = len(self.empty_block)
		h = self.height
		w = self.width

		for mip_i in range(self.mipmap_count):
			# print(mip_i, h, w)
			num_pixels = h * w * self.dx_10.array_size
			# read at least one block
			num_bytes = max(min_bytes, num_pixels // self.pixels_per_byte)
			# address = stream.tell()
			# print(address, num_pixels, num_bytes)
			self.mips.append((h, w, stream.read(num_bytes)))
			h //= 2
			w //= 2
		# print(self.mips)
		self.buffer = b"".join([b for h, w, b in self.mips])
		print("End of mips", stream.tell())

	def pack_mips(self, num_mips):
		"""From a standard DDS stream, pack the lower mip levels into one image and pad with empty bytes"""
		out_mips = []
		packed_levels = []
		# print("\nstandard mips")
		# start packing when one line of the mip == 128 bytes
		for i, (h, w, b) in enumerate(self.mips):
			if i == num_mips:
				break
			if w // self.pixels_per_byte > 32:
				out_mips.append(b)
			else:
				packed_levels.append((h, w, b))

		# no packing at all, just grab desired mips and done
		if not packed_levels:
			print(f"Info: MIP packing is not needed.")
			return b"".join(out_mips)

		with io.BytesIO() as packed_writer:
			# 1 byte per pixel = 64 px
			# 0.5 bytes per pixel = 128 px
			total_width = 64 * self.pixels_per_byte
			# pack the last mips into one image
			for i, (height, width, level_bytes) in enumerate(packed_levels):
				# no matter what pixel size the mips represent, they must be at least one 4x4 chunk
				height = max(4, height)
				width = max(4, width)

				# write horizontal lines
				# get count of h slices, 1 block is 4x4 px
				num_slices_y = height // 4
				num_pad_x = (total_width - width) // 4
				bytes_per_line = len(level_bytes) // num_slices_y

				# write the bytes for this line from the mip bytes
				for slice_i in range(num_slices_y):
					# get the bytes that represent the blocks of this line
					sl = level_bytes[slice_i * bytes_per_line: (slice_i + 1) * bytes_per_line]
					packed_writer.write(sl)
					# fill the line with padding blocks
					for k in range(num_pad_x):
						packed_writer.write(self.empty_block)

				# add one fully blank line for those cases
				if num_slices_y == 1:
					for k in range(total_width // 4):
						packed_writer.write(self.empty_block)

			packed_mip_bytes = packed_writer.getvalue()

		out_mips.append(packed_mip_bytes)

		# get final merged output bytes
		return b"".join(out_mips)

	def pack_mips_pc(self, num_mips):
		"""Grab the lower mip levels according to the count"""
		first_mip_index = self.mipmap_count - num_mips
		print("first mip", first_mip_index)

		# get final merged output bytes
		return b"".join([b for h, w, b in self.mips[first_mip_index:]])


if __name__ == "__main__":
	m = DdsFile()
	m.load("C:/Users/arnfi/Desktop/parrot/parrot.pbasecolourtexture.dds")
	print(m)
	d = D3D10ResourceDimension()
	print(d)
	d = D3D10ResourceDimension(1)
	print(d)
