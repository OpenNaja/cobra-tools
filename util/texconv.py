import os, tempfile, shutil, subprocess

BINARY = os.path.normpath( os.path.join( os.path.dirname(__file__), "texconv/texconv.exe") )
# print(BINARY)
# print(os.path.exists(BINARY))

def run_smart(args):
	argline = " ".join(['"' + x + '"' for x in args])
	subprocess.check_call(args)

def load_dds_texconv( dds_file_path ):
	# tmp = tempfile.mkdtemp("-cobra-dds-load")
	in_dir, in_name = os.path.split(dds_file_path)
	tmp = in_dir
	name = os.path.splitext(in_name)[0]
	# result = tmp + '\\' + name + '.png'
	run_smart([BINARY, "-y", "-ft", "png", "-o", tmp, "-f", "R8G8B8A8_UNORM", "-srgb", "-dx10", dds_file_path])
	# os.remove(dds_file_path)
	# finally:
		# shutil.rmtree(tmp)


def save_dds_texconv( png_file_path, codec = "BC7_UNORM", mips = 1):
	# tmp = tempfile.mkdtemp("-cobra-dds-save")
	png_file_path = os.path.normpath(png_file_path)
	in_dir, in_name = os.path.split(png_file_path)
	tmp = in_dir
	name = os.path.splitext(in_name)[0]
	result = tmp + '\\' + name + '.dds'
	run_smart([BINARY, "-y", "-ft", "dds", "-o", tmp, "-f", codec, "-if", "BOX", "-dx10", "-m", str(mips), "-srgb", "-sepalpha", "-alpha", png_file_path])
	return result