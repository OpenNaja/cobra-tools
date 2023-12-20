import os

from generated.formats.manis import ManisFile
from generated.formats.wsm.compounds.WsmHeader import WsmHeader


def resize(folder, fac=1.0):
	bone_name = "srb"
	out_folder = os.path.join(folder, "resized")
	os.makedirs(out_folder, exist_ok=True)
	for filename in os.listdir(folder):
		if filename.endswith(".manis"):
			filepath = os.path.join(folder, filename)
			manis = ManisFile()
			manis.load(filepath)
			for mi in manis.mani_infos:
				k = mi.keys
				if mi.dtype.compression != 0:
					ck = k.compressed
					ck.loc_bounds.mins *= fac
					ck.loc_bounds.scales *= fac
				else:
					k.pos_bones *= fac
					k.floats *= fac

				wsm_name = f"{mi.name}_{bone_name}.wsm"
				wsm_path = os.path.join(folder, wsm_name)
				if os.path.isfile(wsm_path):
					wsm = WsmHeader.from_xml_file(wsm_path, mi.context)
					for vec in wsm.locs.data:
						vec.x *= fac
						vec.y *= fac
						vec.z *= fac
					wsm_out_path = os.path.join(out_folder, wsm_name)
					with WsmHeader.to_xml_file(wsm, wsm_out_path):
						pass
			out_path = os.path.join(out_folder, filename)
			manis.save(out_path)


resize("C:/Users/arnfi/Desktop/resize", fac=2.0)
