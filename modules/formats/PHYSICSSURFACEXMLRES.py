from generated.formats.physicssurfacesxmlres.structs.PhysicsSurfaceXMLResRoot import PhysicsSurfaceXMLResRoot
from modules.formats.BaseFormat import MemStructLoader


class PhysicsSurfaceXMLResLoader(MemStructLoader):
	target_class = PhysicsSurfaceXMLResRoot
	extension = ".physicssurfacesxmlres"

	def collect(self):
		super().collect()
		if self.ovl.do_debug:
			# print(self.header)
			if hasattr(self.header, "only_names_j_w_e_1"):
				mem = {}
				for s in self.header.only_names_j_w_e_1.arr.data:
					k = s.index
					if k in mem:
						continue
					mem[k] = s.name_1.data
				for k, v in sorted(mem.items()):
					print(f'<option value="{k}" name="{v}" />')
			if hasattr(self.header, "surfaces"):
				print()
				if self.header.surfaces.arr.data:
					for k, s in enumerate(self.header.surfaces.arr.data):
						v = s.surface.surface_name.data
						print(f'<option value="{k}" name="{v}" />')
			# for s in self.header.surfaces.data:
			# 	print(s.)