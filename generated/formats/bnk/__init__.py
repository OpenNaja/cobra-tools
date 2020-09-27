
from generated.formats.bnk.compound.AuxFileContainer import AuxFileContainer
from generated.io import BinaryStream

from contextlib import contextmanager
from typing import *


class BnkFile(AuxFileContainer):

	def load(self, filepath):
		with self.nif_reader(filepath) as stream:
			self.read(stream)

	def save(self, filepath):
		with self.nif_writer(filepath) as stream:
			self.write(stream)

	@staticmethod
	@contextmanager
	def nif_reader(filepath) -> Generator[BinaryStream, None, None]:
		with open(filepath, "rb") as f:
			data = f.read()
		with BinaryStream(data) as stream:
			yield stream  # type: ignore

	@staticmethod
	@contextmanager
	def nif_writer(filepath) -> Generator[BinaryStream, None, None]:
		with BinaryStream() as stream:
			yield stream  # type: ignore
			with open(filepath, "wb") as f:
				# noinspection PyTypeChecker
				f.write(stream.getbuffer())


if __name__ == "__main__":
	bnk = BnkFile()
	bnk.load("C:/Users/arnfi/Desktop/Coding/ovl/aux files/dlc_dingo_dlc_dingo_media_bnk_B.aux")
	print(bnk)
