from generated.formats.matcol.compound.MaterialcollectionInfoHeader import MaterialcollectionInfoHeader
from generated.io import IoFile


class MatcolContext(object):
	def __init__(self):
		self.version = 0
		self.user_version = 0

	def __repr__(self):
		return f"{self.version} | {self.user_version}"


class MatcolFile(MaterialcollectionInfoHeader, IoFile):

	def __init__(self):
		super().__init__(MatcolContext())

	def load(self, filepath, commands=(), mute=False):
		eof = super().load(filepath)

	@property
	def game(self, ):
		# JWE style
		if self.user_version == 24724:
			return "Jurassic World Evolution"
		# PZ Style
		elif self.user_version == 8340:
			return "Planet Zoo"
		else:
			return "Unknown Game"


if __name__ == "__main__":
	m = MatcolFile()
	m.load("C:/Users/arnfi/Desktop/carch/carcharodontosaurus.matcol")
	print(m)
