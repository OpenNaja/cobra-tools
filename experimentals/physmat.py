from generated.formats.ovl_base import OvlContext
from generated.formats.physmat.compounds.PhysmatRoot import PhysmatRoot

files = ("C:/Users/arnfi/Desktop/pz.physmat", "C:/Users/arnfi/Desktop/jwe2.physmat")
for fp in files:
	with open(fp, "rb") as f:
		mat = PhysmatRoot.from_stream(f, OvlContext())
		print(mat)
		for s in ("all_surfaces", "surface_res", "classnames"):
			print("\n\n")
			print(s)
			for ind, offset in enumerate(getattr(mat, f"{s}_names")):
				lut = None
				if s in ("surface_res", "classnames"):
					lut = getattr(mat, f"{s}_indices")[ind]
				print(ind, mat.names.get_str_at(offset), lut)
