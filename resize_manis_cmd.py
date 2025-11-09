import argparse
import os

from utils.logs import logging_setup
from generated.formats.manis import ManisFile
from generated.formats.ms2 import Ms2File
from generated.formats.wsm.structs.WsmHeader import WsmHeader


def resize(folder, fac=1.0):
	"""Change size by fac for all manis and wsm files in folder"""
	# create output folder
	out_folder = os.path.join(folder, "resized")
	os.makedirs(out_folder, exist_ok=True)
	manis = ManisFile()
	ms2 = Ms2File()
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		out_path = os.path.join(out_folder, filename)

		if filename.endswith(".manis"):
			manis.load(file_path)
			manis.resize(fac)
			manis.save(out_path)
		elif filename.endswith(".wsm"):
			wsm = WsmHeader.from_xml_file(file_path, manis.context)
			for vec in wsm.locs.data:
				vec.x *= fac
				vec.y *= fac
				vec.z *= fac
			with WsmHeader.to_xml_file(wsm, out_path):
				pass
		elif filename.endswith(".ms2"):
			ms2.load(file_path, read_editable=True)
			ms2.resize(fac)
			ms2.save(out_path)


if __name__ == '__main__':
	logging_setup("resize_manis_cmd")
	parser = argparse.ArgumentParser(prog='codegen')
	parser.add_argument('dir', nargs='?', help='Folder containing all ms2, manis and wsm files')
	parser.add_argument('fac', nargs='?', default=1.0, type=float, help='Scale factor to scale by, as used in Blender')
	args = parser.parse_args()
	resize(args.dir, args.fac)
