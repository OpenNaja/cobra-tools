import os, tempfile, shutil, subprocess

BINARY = os.path.normpath( os.path.join( os.path.dirname(__file__), "texconv/texconv.exe") )
# print(BINARY)
# print(os.path.exists(BINARY))

def run_smart(args):
	argline = " ".join(['"' + x + '"' for x in args])
	subprocess.check_call(args)

def dds_to_png( dds_file_path, out_dir, height, show_dds):
	"""Converts a DDS file given by a path to a PNG file"""
	print("dds to png", dds_file_path, out_dir, height, show_dds)
	run_smart([BINARY, "-y", "-ft", "png", "-o", out_dir, "-f", "R8G8B8A8_UNORM", "-fl", "12.1", "-h", str(height), "-srgb", "-dx10", dds_file_path])
	clear_tmp( dds_file_path, show_dds)
	in_dir, in_name = os.path.split(dds_file_path)
	name = os.path.splitext(in_name)[0]
	return os.path.join(out_dir, name + '.png')

def png_to_dds( png_file_path, height, show_dds, codec = "BC7_UNORM", mips = 1):
	"""Converts a PNG file given by a path to a DDS file"""
	png_file_path = os.path.normpath(png_file_path)
	in_dir, in_name = os.path.split(png_file_path)
	
	out_dir = make_tmp( in_dir, show_dds )
	name = os.path.splitext(in_name)[0]
	run_smart([BINARY, "-y", "-ft", "dds", "-o", out_dir, "-f", codec, "-fl", "12.1", "-h", str(height), "-if", "BOX", "-dx10", "-m", str(mips), "-srgb", "-sepalpha", "-alpha", png_file_path])

	return os.path.join(out_dir, name + '.dds')

def make_tmp( in_dir, show_dds ):
	""" Make a new temp dir if show_dds is False """
	if show_dds:
		return in_dir
	else:
		return tempfile.mkdtemp("-cobra-dds")


def clear_tmp( dds_file_path, show_dds):
	if not show_dds:
		tmp, in_name = os.path.split(dds_file_path)
		shutil.rmtree(tmp)