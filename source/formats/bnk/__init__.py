from generated.formats.bnk.compound.AuxFileContainer import AuxFileContainer
from generated.formats.bnk.compound.BnkFileContainer import BnkFileContainer
from generated.io import IoFile
import os


class BnkFile(BnkFileContainer, IoFile):

	def load(self, filepath):
		with self.reader(filepath) as stream:
			self.read(stream)

	def save(self, filepath):
		self.old_size = os.path.getsize(filepath)
		with self.writer(filepath) as stream:
			self.write(stream)


class AuxFile(AuxFileContainer, IoFile):

	def load(self, filepath):
		with self.reader(filepath) as stream:
			self.read(stream)

	def save(self, filepath):
		self.old_size = os.path.getsize(filepath)
		with self.writer(filepath) as stream:
			self.write(stream)


if __name__ == "__main__":
	# bnk = BnkFile()
	# bnk.load("C:/Users/arnfi/Desktop/Coding/ovl/aux files/dlc_dingo_dlc_dingo_media_bnk_B.aux")
	# print(bnk)
	bnk = BnkFile()
	bnk.load("C:/Users/arnfi/Desktop/Coding/ovl/aux files/music_vehicleradio_events.bnk")
	print(bnk)
