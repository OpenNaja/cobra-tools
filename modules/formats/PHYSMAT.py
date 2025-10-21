from generated.formats.physmat.structs.PhysmatRoot import PhysmatRoot
from modules.formats.BaseFormat import MemStructLoader


class PhysmatLoader(MemStructLoader):
	target_class = PhysmatRoot
	extension = ".physmat"

	def extract(self, out_dir):
		print(self.header)
		for s in ("all_surfaces", "surface_res", "classnames"):
			print("\n\n")
			print(s)
			names = []
			arr = getattr(self.header, f"{s}_names")
			for ind, offset in enumerate(arr):
				lut = None
				if s in ("surface_res", "classnames"):
					lut = getattr(self.header, f"{s}_indices")[ind]
				else:
					lut = f'{bin(getattr(self.header, f"all_surfaces_flags")[ind])[2:]:>64s}'
				name = self.header.names.get_str_at(offset)
				print(f'{ind:>3d}', lut, name)
				names.append(name)
			print(sorted(names))
		return super().extract(out_dir)
