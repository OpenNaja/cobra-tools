from generated.formats.dds.struct.Header import Header
from generated.formats.dds.enum.D3D10ResourceDimension import D3D10ResourceDimension
from generated.io import IoFile


class DdsFile(Header, IoFile):

	def __init__(self,):
		super().__init__()

	def load(self, filepath, commands=(), mute=False):
		eof = super().load(filepath)


if __name__ == "__main__":
	m = DdsFile()
	m.load("C:/Users/arnfi/Desktop/parrot/parrot.pbasecolourtexture.dds")
	print(m)
	d = D3D10ResourceDimension()
	print(d)
	d = D3D10ResourceDimension(1)
	print(d)
