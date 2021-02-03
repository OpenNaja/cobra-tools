from modules.formats.shared import djb
#
# *file_hash = 1118995050
# *num_files = 0
# *ext_hash = 2830413767
print(djb("Casino:AssetPackageRes:assetpkg"))
print(djb("casino:assetpackageres:assetpkg"))
print(djb("Casino.AssetPackageRes.assetpkg"))
print(djb("casino.assetpackageres.assetpkg"))
print(djb("Casino:AssetPackageRes:"))
print(djb("casino:assetpackageres:"))
print(djb("Casino.AssetPackageRes."))
print(djb("casino.assetpackageres."))
print(djb("Casino:AssetPackageRes"))
print(djb("casino:assetpackageres"))
print(djb("Casino.AssetPackageRes"))
print(djb("casino.assetpackageres"))
print(djb(".assetpkg"))
print(djb(":assetpkg"))
print(djb("assetpkg"))
# print(djb("bani"))
#
# 	* sized_str_entries = [SizedStringEntry [Size: 0, Address: 0]
# 	* file_hash = 1118995050
# 	* ext_hash = 2830413767
# 	* pointers = [HeaderPointer [Size: 0, Address: 0]
# 	* header_index = 0
# 	* data_offset = 128
# ]
# , SizedStringEntry [Size: 0, Address: 0]
# 	* file_hash = 2846495040
# 	* ext_hash = 2830413767
# 	* pointers = [HeaderPointer [Size: 0, Address: 0]
# 	* header_index = 0
# 	* data_offset = 208
# ]
# , SizedStringEntry [Size: 0, Address: 0]
# 	* file_hash = 3013842650
# 	* ext_hash = 2830413767
# 	* pointers = [HeaderPointer [Size: 0, Address: 0]
# 	* header_index = 0
# 	* data_offset = 352
# ]
# , SizedStringEntry [Size: 0, Address: 0]
# 	* file_hash = 3074757116
# 	* ext_hash = 2830413767
# 	* pointers = [HeaderPointer [Size: 0, Address: 0]
# 	* header_index = 0
# 	* data_offset = 496
# ]
# , SizedStringEntry [Size: 0, Address: 0]
# 	* file_hash = 3776781890
# 	* ext_hash = 2830413767
# 	* pointers = [HeaderPointer [Size: 0, Address: 0]
# 	* header_index = 0
# 	* data_offset = 640
# ]
# , SizedStringEntry [Size: 0, Address: 0]
# 	* file_hash = 1056665418
# 	* ext_hash = 193491473
# 	* pointers = [HeaderPointer [Size: 0, Address: 0]
# 	* header_index = 0
# 	* data_offset = 656
# ]
# , SizedStringEntry [Size: 0, Address: 0]
# 	* file_hash = 1755461150
# 	* ext_hash = 193491473
# 	* pointers = [HeaderPointer [Size: 0, Address: 0]
# 	* header_index = 0
# 	* data_offset = 688
# ]
# , SizedStringEntry [Size: 0, Address: 0]
# 	* file_hash = 3921485951
# 	* ext_hash = 193491473
# 	* pointers = [HeaderPointer [Size: 0, Address: 0]
# 	* header_index = 0
# 	* data_offset = 720
# ]
# , SizedStringEntry [Size: 0, Address: 0]
# 	* file_hash = 1284844042
# 	* ext_hash = 193498567
# 	* pointers = [HeaderPointer [Size: 0, Address: 0]
# 	* header_index = 0
# 	* data_offset = 752


# START_GLOBALS
import numpy as np

# END_GLOBALS


class Matrix33(np.ndarray):

	def __init__(self, shape):
		print("HY")
		super().__init__((3, 3), dtype=np.float32)
	# START_CLASS

	def __repr__(self):
		return (
				"[ %6.3f %6.3f %6.3f ]\n"
				"[ %6.3f %6.3f %6.3f ]\n"
				"[ %6.3f %6.3f %6.3f ]\n"
				% (self.m_11, self.m_12, self.m_13, self.m_21, self.m_22, self.m_23, self.m_31, self.m_32, self.m_33))


m = Matrix33((1,2))
print(m)