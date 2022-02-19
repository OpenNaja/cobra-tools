from generated.formats.manis.compound.ManiBlock import ManiBlock
from generated.formats.manis.compound.InfoHeader import InfoHeader
from generated.formats.ovl_base import OvlContext
from generated.io import IoFile
import os

from modules.formats.shared import get_padding_size


def hex_test():
	for i in range(20):
		x = 2 ** i
		print(i, bin(i), x, bin(x))


class ManisFile(InfoHeader, IoFile):

	def __init__(self):
		super().__init__(OvlContext())

	def load(self, filepath):
		# store file name for later
		self.file = filepath
		self.dir, self.basename = os.path.split(filepath)
		self.path_no_ext = os.path.splitext(self.file)[0]

		with self.reader(filepath) as stream:
			self.read(stream)
			for mi, name in zip(self.mani_infos, self.names):
				mi.name = name
			print(self)
			# read the first mani data
			for mani_info in self.mani_infos:
				mani_block = stream.read_type(ManiBlock, (self.context, mani_info,))
				print(mani_info)
				print(mani_block)
				# # return
				# # is this correct??
				# zeros = stream.read(4)
				# print(zeros, stream.tell())
				sum_bytes = sum(mb.byte_size for mb in mani_block.repeats)
				print("sum_bytes", sum_bytes)
				sum_bytes2 = sum(mb.byte_size + get_padding_size(mb.byte_size) for mb in mani_block.repeats)
				print("sum_bytes + padding", sum_bytes2)
				for mb, bone_name in zip(mani_block.repeats, self.bone_names):
					print(bone_name, stream.tell())
					data = stream.read(mb.byte_size)
					pad_size = get_padding_size(mb.byte_size)
					padding = stream.read(pad_size)
					print("end", stream.tell())
					# print(binascii.hexlify(data[:40]), padding, stream.tell())
					with open(os.path.join(self.dir, f"{self.path_no_ext}_{mani_info.name}_{bone_name}.maniskeys"), "wb") as f:
						f.write(data)
			for i, bone_name in enumerate(self.bone_names):
				print(i, bone_name)

	@property
	def buffers(self):
		return self.buffer_0_bytes, self.buffer_1_bytes, self.buffer_2_bytes


if __name__ == "__main__":
	mani = ManisFile()
	# mani.load("C:/Users/arnfi/Desktop/dilo/locomotion.maniset1c05e0f4.manis")
	# mani.load("C:/Users/arnfi/Desktop/ostrich/ugcres.maniset8982114c.manis")
	# mani.load("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/anim test/rot_x_0_22_42.manis")
	# mani.load("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/anim test/ugcres.maniset8982114c0.manis")
	# mani.load("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/anim test/ugcres.maniset8982114c1.manis")
	# mani.load("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/anim test/ugcres.maniset8982114c2.manis")
	# mani.load("C:/Users/arnfi/Desktop/Coding/ovl/PZ 1.6/anim/animation.maniset9637aeb4.manis")
	# mani.load("C:/Users/arnfi/Desktop/Coding/ovl/PZ 1.6/anim/animationmotionextractedbehaviour.maniset5f721adf.manis")
	# mani.load("C:/Users/arnfi/Desktop/Coding/ovl/PZ 1.6/anim/animationmotionextractedlocomotion.maniset58076276.manis")
	# mani.load("C:/Users/arnfi/Desktop/lemur/animationnotmotionextractedpartials.maniset919dac12.manis")
	# mani.load("C:/Users/arnfi/Desktop/lemur/animationmotionextractedfighting.maniset9c749130.manis")
	# mani.load("C:/Users/arnfi/Desktop/lemur/animationnotmotionextractedlocomotion.maniset87d072d8.manis")
	# mani.load("C:/Users/arnfi/Desktop/EA_WaterWheel/animation.maniset9637aeb4.manis")
	mani.load("C:/Users/arnfi/Desktop/Coding/Frontier/anim/Iron_piston/ugcres.maniset8982114c.manis")
	# print(mani)
	# hex_test()