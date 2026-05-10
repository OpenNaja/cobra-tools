import os

from modules.formats.utils import util_dir
from utils.shared import register_binary, requires_binary, run_binary

texconv = os.path.normpath(os.path.join(util_dir, "texconv/texconv.exe"))
register_binary("texconv", texconv)


@requires_binary("texconv")
def dds_to_png(dds_file_path, codec):
	"""Converts a DDS file given by a path to a PNG file"""
	out_dir, in_name = os.path.split(dds_file_path)
	name = os.path.splitext(in_name)[0]
	args = ["-y", "-ft", "png", "-o", out_dir, "-fl", "12.1", "-dx10"]
	# logging.info(f"Selective SRGB {codec}")
	if "SRGB" in codec:
		args.extend(("-f", "R8G8B8A8_UNORM_SRGB", "-srgb"))
	else:
		args.extend(("-f", "R8G8B8A8_UNORM"))
	args.append(dds_file_path)
	run_binary("texconv", args)
	return os.path.join(out_dir, name + '.png')


@requires_binary("texconv")
def png_to_dds(png_file_path, out_dir, codec="BC7_UNORM", num_mips=0, dds_use_gpu=False):
	"""Converts a PNG file given by a path to a DDS file"""
	png_file_path = os.path.normpath(png_file_path)
	in_dir, in_name = os.path.split(png_file_path)
	name = os.path.splitext(in_name)[0]
	args = ["-y", "-ft", "dds", "-o", out_dir, "-f", codec, "-fl", "12.1", "-if", "FANT_DITHER_DIFFUSION",
		"-dx10", "-m", str(num_mips), "-sepalpha"]
	if "SRGB" in codec:
		args.append("-srgb")
	if not dds_use_gpu:
		args.append("-nogpu")
	args.append(png_file_path)
	run_binary("texconv", args)
	return os.path.join(out_dir, name + '.dds')
