import os, tempfile, shutil, subprocess, struct

util_dir = os.path.dirname(__file__)
BINARY = os.path.normpath( os.path.join( util_dir , "texconv/texconv.exe") )
ww2ogg = os.path.normpath( os.path.join( util_dir, "ww2ogg/ww2ogg.exe") )
pcb = os.path.normpath( os.path.join( util_dir, "ww2ogg/packed_codebooks_aoTuV_603.bin") )
revorb = os.path.normpath( os.path.join( util_dir, "revorb/revorb.exe") )
# print(BINARY)
# print(os.path.exists(BINARY))


def run_smart(args):
	# argline = " ".join(['"' + x + '"' for x in args])
	subprocess.check_call(args)


def wem_handle( wem_files, out_dir, show_dds, progress_callback):
	for wem_i, wem_file in enumerate(wem_files):

		progress_callback("Converting audio", value=wem_i, vmax=len(wem_files))
		print("checking wem format", wem_file, out_dir, show_dds)
		out_name = os.path.splitext(os.path.basename(wem_file))[0]
		out_file = os.path.join(out_dir, out_name)
		# read the format
		with open(wem_file, "rb") as f:
			f.seek(20)
			fmt = struct.unpack("<h", f.read(2))[0]
		# print("fmt", fmt)
		if fmt == -1:
			wem_to_ogg(wem_file, out_file)
		elif fmt == -2:
			wem_to_wav(wem_file, out_file)
		else:
			raise NotImplementedError(f"Unknown RIFF format {fmt} in {out_name}! Please report to the devs!")
	clear_tmp(wem_file, show_dds)


def wem_to_ogg(wem_file, out_file):
	run_smart([ww2ogg, wem_file, "-o", out_file+".ogg", "--pcb", pcb, ])
	run_smart([revorb, out_file+".ogg"])


def wem_to_wav(wem_file, out_file):
	with open(wem_file, "rb") as f:
		data = f.read()
	with open(out_file+".wav", "wb") as f:
		# header up for the format chunk
		f.write(data[:20])
		# wav, stereo
		f.write(struct.pack("<hh", 1, 2))
		# the rest
		f.write(data[24:])


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