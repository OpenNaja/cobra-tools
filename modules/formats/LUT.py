import os

from generated.array import Array
from generated.formats.base.basic import Ushort
from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.lut.structs.LutHeader import LutHeader
from modules.formats.BaseFormat import MemStructLoader


class LutLoader(MemStructLoader):
	extension = ".lut"
	target_class = LutHeader

	def extract(self, out_dir):
		out_files = super().extract(out_dir)
		paths = [*out_files]

		size = self.header.colors_in_column_count
		file_name = f"{self.basename}.cube"
		file_path = out_dir(file_name)
		paths.append(file_path)
		with open(file_path, 'w') as text:
			text.write(
				f'#Created by: Cobra Tools\n'
				f'TITLE "{file_name}"\n'
				f'#LUT size\n'
				f'LUT_3D_SIZE {size}\n'
				f'#data domain\n'
				f'DOMAIN_MIN 0.0 0.0 0.0\n'
				f'DOMAIN_MAX 1.0 1.0 1.0\n')
			for color in self.header._colors.data:
				text.write(f"{color[0]:.6f} {color[1]:.6f} {color[2]:.6f}\n")
		return paths

	def create(self, file_path):
		self.header = self.target_class.from_xml_file(file_path, self.ovl.context)
		file_dir = os.path.dirname(file_path)
		file_name = f"{self.basename}.cube"
		file_path = os.path.join(file_dir, file_name)
		with open(file_path, 'r') as text:
			i = 0
			for line in text.readlines():
				if line.startswith(("#", "TITLE", "DOMAIN")):
					continue
				elif line.startswith("LUT_3D_SIZE"):
					self.header.colors_in_column_count = int(line.split()[1])
					self.header.dimensions = 3
					self.header.colors_count = self.header.colors_in_column_count ** self.header.dimensions
					if self.header.colors_count > 65535:
						raise AttributeError(
							f"LUT can only hold 65535 items. "
							f"Size {self.header.colors_in_column_count} uses {self.header.colors_count} items")
					self.header._colors.data = Array(self.header.context, arg=0, template=None, shape=(self.header.colors_count,), dtype=Vector3, set_default=True)
				elif line.strip():
					self.header._colors.data[i][:] = [float(x) for x in line.split()]
					i += 1
		self.write_memory_data()
