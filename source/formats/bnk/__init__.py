from generated.formats.bnk.basic import basic_map
from generated.formats.bnk.compounds.AuxFileContainer import AuxFileContainer
from generated.formats.bnk.compounds.BnkFileContainer import BnkFileContainer
from generated.formats.ovl_base import OvlContext
from generated.io import IoFile
import os


class BnkFile(BnkFileContainer, IoFile):

	basic_map = basic_map

	def __init__(self):
		super().__init__(OvlContext())

	def load(self, filepath):
		with self.reader(filepath) as stream:
			self.read(stream)

	def save(self, filepath):
		self.old_size = os.path.getsize(filepath)
		with self.writer(filepath) as stream:
			self.write(stream)


class AuxFile(AuxFileContainer, IoFile):

	basic_map = basic_map

	def __init__(self):
		super().__init__(OvlContext())

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
