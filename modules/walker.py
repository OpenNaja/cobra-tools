import os


def walk_type(start_dir, extension="ovl"):
	print(f"Scanning {start_dir} for {extension} files")
	ret = []
	for root, dirs, files in os.walk(start_dir, topdown=False):
		for name in files:
			if name.lower().endswith("."+extension):
				ret.append(os.path.join(root, name))
	return ret

