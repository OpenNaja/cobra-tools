from generated.formats.ovl_base import OvlContext
from generated.formats.physmat.compounds.PhysmatRoot import PhysmatRoot

files = ("C:/Users/arnfi/Desktop/pz.physmat", "C:/Users/arnfi/Desktop/jwe2.physmat")
for fp in files:
	with open(fp, "rb") as f:
		mat = PhysmatRoot.from_stream(f, OvlContext())
		print(mat)
		for s in ("all_surfaces_names", "surface_res_names", "classnames_names"):
			print("\n\n")
			print(s)
			for ind, offset in enumerate(getattr(mat, s)):
				print(ind, mat.names.get_str_at(offset))
