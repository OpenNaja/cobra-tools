import time
import numpy as np
from generated.array import Array
from generated.formats.ovl import is_pc
from generated.formats.voxelskirt.compound.Header import Header
# from generated.formats.ovl import *
from generated.io import IoFile


class VoxelskirtFile(Header, IoFile):

	def __init__(self, ):
		super().__init__()

	def load(self, filepath):
		start_time = time.time()
		# eof = super().load(filepath)

		# extra stuff
		self.bone_names = []
		self.bone_info = None
		with self.reader(filepath) as stream:
			self.read(stream)
			self.eoh = stream.tell()
			print(self)
			# self.heightmap = stream.read_floats((self.info.x, self.info.y))
			print(f"Min Height: {np.min(self.heightmap)}, Max Height: {np.max(self.heightmap)}")
			self.heightmap /= self.info.height
			# self.end_of_heightmap = stream.tell()
			# print(self.end_of_heightmap)
			# self.weights = stream.read_ubytes((self.info.x * self.info.y, 4))
			# print(self.weights)
			# self.end_of_weights = stream.tell()
			# print(self.end_of_weights)
			print(self.eoh)
			# print(self.weights.shape)
			# For non-PC maps, swap the axes so that the data layout is the same
			if not is_pc(self):
				# self.weights = np.swapaxes(self.weights, 0, 1)
				# self.weights = np.moveaxis(self.weights, (0, 1), (1, 0))
				self.weights = np.transpose(self.weights)

	def save(self, filepath):
		print("Writing verts and tris to temporary buffer")


if __name__ == "__main__":
	import matplotlib
	import matplotlib.pyplot as plt
	m = VoxelskirtFile()
	# files = ("C:/Users/arnfi/Desktop/deciduousskirt.voxelskirt",
	# 		  "C:/Users/arnfi/Desktop/alpineskirt.voxelskirt",
	# 		  "C:/Users/arnfi/Desktop/nublar.voxelskirt",
	# 		   "C:/Users/arnfi/Desktop/savannahskirt.voxelskirt")
	files = ("C:/Users/arnfi/Desktop/savannahskirt.voxelskirt",)
	for f in files:
		print(f)
		m.load(f)

		fig, ax = plt.subplots()
		ax.imshow(m.weights.reshape((m.info.x, m.info.y, 4))[:,:,1])
		# ax.plot(t, s)

		# ax.set(xlabel='time (s)', ylabel='voltage (mV)',
		# 	   title='About as simple as it gets, folks')
		# ax.grid()

		fig.savefig("test.png")
		plt.show()