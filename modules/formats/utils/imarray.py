import logging
import os
from pathlib import Path
import imageio.v3 as iio
import numpy as np
import PIL

from constants import ConstantsProvider
from utils.shared import check_any
from generated.formats.ovl.versions import is_ztuac

logging.getLogger('PIL').setLevel(logging.WARNING)


def reconstruct_z(im):
	"""Takes an array with 2 channels and adds a third channel"""
	h, w, d = im.shape
	assert d == 2
	im_rec = np.empty((h, w, 3), dtype=im.dtype)
	im_rec[:, :, :2] = im[:, :, :2]
	# convert to range +-1
	im_f = im.astype(np.float32) / 127 - 1.0
	# take pythagoras
	norm_xy = np.clip(np.linalg.norm(im_f[:, :, :2], axis=-1), 0.0, 1.0)
	# resulting z is in in 0,1 range, scale back to uint8 range
	im_rec[:, :, 2] = np.round(np.sqrt(1.0 - norm_xy) * 127 + 127)
	return im_rec


def flip_gb(im):
	"""Flips green and blue channels of image array"""
	im = im.copy()
	im[:, :, 1] = 255 - im[:, :, 1]
	im[:, :, 2] = 255 - im[:, :, 2]
	logging.debug(f"Flipped GB channels")
	return im


def flip_g(im):
	"""Flips green channel of image array"""
	im = im.copy()
	im[:, :, 1] = 255 - im[:, :, 1]
	logging.debug(f"Flipped G channel")
	return im


def has_vectors(png_name, compression):
	if "pnormaltexture" in png_name:
		# PZ uses BC5, so just RG
		if "BC5" in compression:
			return "G"
		# pnormaltexture - JWE2 uses RGBA, with no need to flip channels
		else:
			return False
	if check_any(("normaltexture", "playered_warpoffset"), png_name):
		return "GB"


# define additional functions for specific channel indices
channel_modes = {
	("RG_B_A", "RG"): reconstruct_z,
	("RG", "RG"): reconstruct_z
	}


def channel_iter(channels):
	ch_i = 0
	# get the channels to use in each chunk, eg. RG (2), B (1), ...
	ch_names = channels.split("_")
	for ch_name in ch_names:
		ch_count = len(ch_name)
		# define which channels to use from im
		ch_slice = slice(ch_i, ch_i + ch_count)
		yield ch_name, ch_slice
		# increment indices
		ch_i += ch_count


def split_png(png_file_path, ovl, compression=None):
	"""Fixes normals and splits channels of one PNG file if needed"""
	out_files = []
	flip = has_vectors(png_file_path, compression)
	channels = get_split_mode(ovl.game, png_file_path, compression)
	if is_ztuac(ovl):
		flip = False
	if flip or channels:
		logging.info(f"Splitting {png_file_path} into {channels} channels")
		im = imread(png_file_path)
		if flip == "GB":
			im = flip_gb(im)
		if flip == "G":
			im = flip_g(im)
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

def get_extract_paths(png_file_path, ovl, compression=None):
	"""Fixes normals and splits channels of one PNG file if needed"""
	out_files = []
	flip = has_vectors(png_file_path, compression)
	channels = get_split_mode(ovl.game, png_file_path, compression)
	if is_ztuac(ovl):
		flip = False
	if flip or channels:
		if not channels:
			out_files.append(png_file_path)
		else:
			path_basename, ext = os.path.splitext(png_file_path)
			for ch_name, ch_slice in channel_iter(channels):
				file_path = f"{path_basename}_{ch_name}{ext}"
				out_files.append(file_path)
	else:
		out_files.append(png_file_path)
	return out_files


constants = ConstantsProvider(("texchannels",))


def get_split_mode(game, png_name, compression):
	# Get texture type
	suffixes = Path(png_name).suffixes
	try:
		tex_type = suffixes[0]
	except IndexError:
		tex_type = png_name

	try:
		# prioritize game-based hand rolled dicts
		all_tex_channels = constants[game]["texchannels"]
		all_tex_channels_lower = {tex_type.lower(): tex_channels for tex_type, tex_channels in all_tex_channels.items()}
		tex_id = tex_type[1:].rsplit("_[", 1)[0]  # strip the leading . and remove any array suffices
		tex_channels_map = all_tex_channels_lower.get(tex_id)
		if tex_channels_map is None:
			logging.warning(f"No texchannels map provided for {png_name}, falling back to legacy splitting")
		else:
			suggested_channels = set(tex_channels_map.keys())
			# remove empty channel ids
			valid_channels = [channel_id for channel_id in suggested_channels if channel_id]
			out_channels = []
			# clamping of channel IDs according to compression type to select the correct subtype
			for channel_id in valid_channels:
				if check_any(("BC5",), compression):
					# supports only two channels - only accept RG or R_G
					if channel_id not in ("RG", "R", "G"):
						continue
				else:
					if channel_id in ("RG", "R", "G"):
						# prefer RGB(A) if it is available
						if check_any(("RGB", "RGBA"), valid_channels):
							continue
				out_channels.append(channel_id)
			# sort the output to be in RGBA order
			out_channels = sorted(out_channels, key=lambda k: "RGBA".index(k[0]))
			return "_".join(out_channels)  # ignore empty identifiers = RGBA
	except:
		logging.exception(f"Game based splitting failed, falling back on legacy splitting rules")

	if check_any(("BC5",), compression):
		# two channels
		if check_any(("pbaseaotexture", "packed", "mask"), tex_type):
			return "R_G"
		else:
			return "RG"
	if not check_any(("BC5",), compression) and check_any(("pbasenormaltexture", "pgradheightarray", "pnormalmaptextureunique", "pnormaltexturedetailbase"), tex_type):
		# Ensure not BC5 for pnormalmaptextureunique, pnormaltexturedetailbase, which are BC5 in some games
		return "RG_B_A"
	if check_any(
			(
				"pmossbasecolourroughnesspackedtexture", "ppackedtexture", "palbedoandroughnessdetail", "pnormaltexture",
				"pbasecolourtexture", "pbasecolour2", "pdiffusetexture", "pdiffusealphatexture", "basecolourandmasktexture", "waternormalroughnessmap"
			), tex_type):
		return "RGB_A"
	if check_any((
		"packedtexture", "maskmap", "playered_blendweights", "playered_diffusetexture", "playered_heighttexture", "playered_packedtexture",
		"playered_remaptexture", "scartexture",
		# "samplertexture", - PC, but not all are packed (eg. paosamplertexture)
		"pflexicolourmaskssamplertexture", "pcavitysmoothnessopacitysamplertexture",
		"pspecularsmoothnesssamplertexture", "pmetalsmoothnesscavitysamplertexture",
		"pmetalsmoothnesscavityopacitysamplertexture",  # todo - maybe more packed samplertextures
		"pspecularmaptexture", "pflexicolourmaskstexture", "pshellmap", "pfinalphatexture", "ppiebaldtexture",
		"pcavityroughnessdielectricarray", "waterflowandtimeoffsetmap"), tex_type):
		return "R_G_B_A"


def imread(uri):
	# using pngs with palettes requires a conversion
	# print(iio.immeta(uri))
	return iio.imread(uri, mode="RGBA")


def join_png(game, path_basename, tmp_dir, compression=None):
	"""This finds and if required, creates, a png file that is ready for DDS conversion (arrays or flipped channels)"""
	ext = ".png"
	logging.debug(f"Looking for .png for {path_basename}")
	in_dir, basename = os.path.split(path_basename)
	basename = basename.lower()
	png_file_name = f"{basename}.png"
	png_file_path = os.path.join(in_dir, png_file_name)
	tmp_png_file_path = os.path.join(tmp_dir, png_file_name)
	channels = get_split_mode(game, basename, compression)
	flip = has_vectors(basename, compression)
	# check if processing needs to be done
	if not flip and not channels:
		if not os.path.isfile(png_file_path):
			raise FileNotFoundError(f"{png_file_path} does not exist")
		logging.debug(f"Need not process {png_file_path}")
		return png_file_path
	# rebuild from channel pngs, but only if the un-split png does not already exist
	if channels and not os.path.isfile(png_file_path):
		im = None
		for ch_name, ch_slice in channel_iter(channels):
			tile_png_path = f"{path_basename}_{ch_name}{ext}"
			if not os.path.isfile(tile_png_path):
				raise FileNotFoundError(f"Tile {os.path.basename(tile_png_path)} of {channels} does not exist")
				# logging.warning(f"Tile {os.path.basename(tile_png_path)} of {channels} does not exist")
				# continue
			tile = imread(tile_png_path)
			if im is None:
				im = np.zeros(tile.shape, dtype=np.uint8)
			else:
				if im.shape != tile.shape:
					logging.warning(f"Tile shape of {tile_png_path} ({tile.shape}) does not match expected shape ({im.shape}), resizing to match")
					# resize tile to match image shape
					tile = PIL.Image.fromarray(tile).resize(im.shape[0:2])
					tile = np.array(tile)
			# take a slice, starting at the first channel of the tile
			im[:, :, ch_slice] = tile[:, :, 0:len(ch_name)]
		logging.info(f"Joining {png_file_name} from {channels} channels")
	else:
		# non-tiled files that need fixes - normal maps without channel packing
		# just read the one input file
		im = imread(png_file_path)

	# flip channels
	if flip == "GB":
		im = flip_gb(im)
	if flip == "G":
		im = flip_g(im)

	# this is shared for all pngs that have to be read
	logging.debug(f"Writing output to {tmp_png_file_path}")
	iio.imwrite(tmp_png_file_path, im, compress_level=2)
	return tmp_png_file_path
