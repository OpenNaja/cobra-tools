from generated.formats.manis.compound.ManiBlock import ManiBlock
from generated.formats.manis.compound.InfoHeader import InfoHeader
from generated.io import IoFile, BinaryStream
import os
import struct
import binascii


def get_padding(size, pad_to=16):
	mod = size % pad_to
	if mod:
		return pad_to - mod
	return 0


def hex_test():
	for i in range(20):
		x = 2 ** i
		print(i, bin(i), x, bin(x))

class ManisFile(InfoHeader, IoFile):

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
			print(self)
			#
			# read the first mani data
			mani_info = self.mani_infos[0]
			mani_block = stream.read_type(ManiBlock, (mani_info,))
			print(mani_block)
			# is this correct??
			zeros = stream.read(4)
			print(zeros, stream.tell())
			sum_bytes = sum(mb.byte_size for mb in mani_block.repeats)
			print("sum_bytes", sum_bytes)
			sum_bytes2 = sum(mb.byte_size + get_padding(mb.byte_size) for mb in mani_block.repeats)
			print("sum_bytes + padding", sum_bytes2)
			for mb in mani_block.repeats:
				data = stream.read(mb.byte_size)
				pad_size = get_padding(mb.byte_size)
				padding = stream.read(pad_size)
				print(binascii.hexlify(data[:40]))
			stream.tell()
			#
			# # seems to be pretty good until here, then it breaks
			#
			# # flags per frame?
			# frames_0 = [struct.unpack(f"<4B", stream.read(4)) for i in range(mani_info.frame_count)]
			# print("frames_0", frames_0)
			# print("pad", stream.read(1))
			# # could be bitfields per frame?
			# frames_1 = struct.unpack(f"<{mani_info.frame_count}I", stream.read(mani_info.frame_count * 4))
			# print("frames_1", frames_1)
			# zerom, frame_count, name_count, c_count = struct.unpack(f"<4I", stream.read(4 * 4))
			# print("zerom, frame_count, name_count, c_count", zerom, frame_count, name_count, c_count)
			# print("zeros", stream.read(76))
			# x, y = struct.unpack(f"<2H", stream.read(4))
			# print("x, y", x, y)


if __name__ == "__main__":
	mani = ManisFile()
	# mani.load("C:/Users/arnfi/Desktop/dilo/locomotion.maniset1c05e0f4.manis")
	# print(mani)
	# hex_test()