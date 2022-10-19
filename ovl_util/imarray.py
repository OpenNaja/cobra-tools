import logging
import os
import imageio.v3 as iio
import numpy as np

from generated.formats.ovl.versions import is_ztuac


def reconstruct_z(im):
	"""Takes an array with 2 channels and adds a third channel"""
	h, w, d = im.shape
	assert d == 2
	im_rec = np.empty((h, w, 3), dtype=im.dtype)
	im_rec[:, :, :2] = im[:, :, :2]
	im_rec[:, :, 2] = 255
	return im_rec


def flip_gb(im):
	"""Flips green and blue channels of image array"""
	im = im.copy()
	im[:, :, 1] = 255 - im[:, :, 1]
	im[:, :, 2] = 255 - im[:, :, 2]
	return im


def check_any(iterable, string):
	"""Returns true if any of the entries of the iterable occur in string"""
	return any([i in string for i in iterable])


def has_rgb_a(png_file_path):
	return check_any(("pmossbasecolourroughnesspackedtexture", "ppackedtexture", "palbedoandroughnessdetail"), png_file_path)


def has_rg_b_a(png_file_path):
	return check_any(("pbasenormaltexture",), png_file_path)


def has_r_g_b_a(png_file_path):
	return check_any((
		"packedtexture", "playered_blendweights", "scartexture", "samplertexture",
		"pspecularmaptexture", "pflexicolourmaskstexture", "pshellmap", "pfinalphatexture",), png_file_path)


def has_vectors(png_file_path):
	return check_any(("normaltexture", "playered_warpoffset"), png_file_path)


# define additional functions for specific channel indices
channel_modes = {
	("RG_B_A", "RG"): reconstruct_z
	}


def channel_iter(channels):
	ch_i = 0
	# get the channels to use in each chunk, eg. RG (2), B (1), ...
	ch_names = channels.split("_")
	for ch_name in ch_names:
		ch_count = len(ch_name)
		# define which channels to use from im
		# if ch_count > 1:
		ch_slice = slice(ch_i, ch_i + ch_count)
		# else:
		# 	# need to use 1D or the png file will break
		# 	ch_slice = ch_i
		# logging.info(f"Channel {ch_slice}")
		yield ch_name, ch_slice
		# increment indices
		ch_i += ch_count


def split_png(png_file_path, ovl):
	"""Fixes normals and splits channels of one PNG file if needed"""
	out_files = []
	must_flip_gb = has_vectors(png_file_path)
	channels = get_split_mode(png_file_path)
	if is_ztuac(ovl):
		must_flip_gb = False
	logging.debug(f"{png_file_path} channels {channels}, must_flip_gb {must_flip_gb}")
	if must_flip_gb or channels:
		logging.info(f"Splitting {png_file_path} into {channels} channels")
		im = imread(png_file_path)
		if must_flip_gb:
			im = flip_gb(im)
		if not channels:
			# don't split at all, overwrite
			iio.imwrite(png_file_path, im, compress_level=2)
			out_files.append(png_file_path)
		else:
			path_basename, ext = os.path.splitext(png_file_path)
			for ch_name, ch_slice in channel_iter(channels):
				# get raw slice of im
				im_slice = im[:, :, ch_slice]
				# logging.debug(f"Image shape {im_slice.shape}")
				# is there an additional function to perform for this channel config and ch_i?
				function = channel_modes.get((channels, ch_name), None)
				if function is not None:
					im_slice = function(im_slice)
					# logging.debug(f"Image shape after function {im_slice.shape}")
				file_path = f"{path_basename}_{ch_name}{ext}"
				# if the last dimension (channels) is 1, remove it for single channel PNG
				iio.imwrite(file_path, np.squeeze(im_slice), compress_level=2)
				out_files.append(file_path)
			# remove the original PNG
			os.remove(png_file_path)
	else:
		out_files.append(png_file_path)
	return out_files


def get_split_mode(png_file_path):
	if has_rgb_a(png_file_path):
		return "RGB_A"
	if has_rg_b_a(png_file_path):
		return "RG_B_A"
	if has_r_g_b_a(png_file_path):
		return "R_G_B_A"


def is_corresponding_png(file_name, name_bare):
	if file_name.startswith(name_bare) and file_name.lower().endswith(".png"):
		return True


def check_same_dimensions(shapes, files):
	"""Make sure that all array tiles have the same size"""
	if not all(x == shapes[0] for x in shapes):
		t_str = "\n".join([f"{im} [{h} x {w}] {d}" for (h, w, d), im in zip(shapes, files)])
		raise AttributeError(f"Array tiles have different dimensions:\n{t_str}")


def imread(uri):
	# using pngs with palettes requires a conversion
	# print(iio.immeta(uri))
	return iio.imread(uri, mode="RGBA")


def join_png(path_basename, tmp_dir):
	"""This finds and if required, creates, a png file that is ready for DDS conversion (arrays or flipped channels)"""
	ext = ".png"
	path_basename = path_basename.lower()
	logging.debug(f"Looking for .png for {path_basename}")
	in_dir, basename = os.path.split(path_basename)
	png_file_path = os.path.join(in_dir, f"{basename}.png")
	tmp_png_file_path = os.path.join(tmp_dir, f"{basename}.png")
	lower_files = [file.lower() for file in os.listdir(in_dir)]
	corresponding_png_textures = [file for file in lower_files if is_corresponding_png(file, basename)]

	channels = get_split_mode(path_basename)
	must_flip_gb = has_vectors(path_basename)
	logging.debug(f"{png_file_path} channels {channels}, must_flip_gb {must_flip_gb}")
	
	# check if processing needs to be done
	if not must_flip_gb and not channels:
		assert os.path.isfile(png_file_path)
		logging.debug(f"Need not process {png_file_path}")
		return png_file_path

	# rebuild from channels
	if channels:
		# read all images into arrays
		ims = [imread(os.path.join(in_dir, file)) for file in corresponding_png_textures]
		# check that all textures have the same shape
		check_same_dimensions([im.shape for im in ims], corresponding_png_textures)
		# todo - maybe build shape from tex?
		im = np.zeros(ims[0].shape, dtype=np.uint8)
		# print(ims[0].shape, ims[0].dtype)
		for ch_name, ch_slice in channel_iter(channels):
			tile_png_path = f"{path_basename}_{ch_name}{ext}"
			# todo slice width is len(ch_name), make sure that is correct especially for expanded single channel images
			im[:, :, ch_slice] = imread(tile_png_path)[:, :, 0:len(ch_name)]
	else:
		# non-tiled files that need fixes - normal maps without channel packing
		# just read the one input file
		im = imread(png_file_path)

	# flip the green and blue channels
	if must_flip_gb:
		im = flip_gb(im)

	# this is shared for all pngs that have to be read
	logging.debug(f"Writing output to {tmp_png_file_path}")
	iio.imwrite(tmp_png_file_path, im, compress_level=2)
	return tmp_png_file_path


def get_single_channel(im, name):
	tile_shape = im.shape
	if len(tile_shape) == 2:
		return im
	# with imread converting to RGBA, this is now the only case
	elif len(tile_shape) == 3:
		logging.debug(f"Tile {name} is not the expected single-channel format, using first channel.")
		return im[:, :, 0]
