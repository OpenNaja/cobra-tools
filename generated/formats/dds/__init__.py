from generated.formats.dds.struct.Header import Header
from generated.formats.dds.enum.D3D10ResourceDimension import D3D10ResourceDimension
from generated.io import IoFile


class DdsFile(Header, IoFile):

	def __init__(self,):
		super().__init__()
		self.buffer = b""

	def load(self, filepath):
		with self.reader(filepath) as stream:
			self.read(stream)
			self.buffer = stream.read()

	def save(self, filepath):
		with self.writer(filepath) as stream:
			self.write(stream)
			stream.write(self.buffer)


if __name__ == "__main__":
	m = DdsFile()
	m.load("C:/Users/arnfi/Desktop/parrot/parrot.pbasecolourtexture.dds")
	print(m)
	d = D3D10ResourceDimension()
	print(d)
	d = D3D10ResourceDimension(1)
	print(d)
