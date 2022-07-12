import logging
import os
import imageio
import numpy as np

from generated.formats.ovl.versions import is_ztuac


def flip_gb(im):
	"""Flips green and blue channels of image array"""
	im[:, :, 1] = 255 - im[:, :, 1]
	im[:, :, 2] = 255 - im[:, :, 2]


def check_any(iterable, string):
	"""Returns true if any of the entries of the iterable occur in string"""
	return any([i in string for i in iterable])


def has_components(png_file_path):
	return check_any((
		"playered_blendweights", "pbasepackedtexture", "proughnesspackedtexture", "pbaldnessscartexture",
		"markingbaldnessscartexture", "markingscartexture", "pflexicolourmaskssamplertexture",
		"pmetalsmoothnesscavitysamplertexture", "pmetalsmoothnesscavityopacitysamplertexture",
		"pspecularmaptexture", "pflexicolourmaskstexture", "pshellmap", "pfinalphatexture", "proughnessaopackedtexturedetailbase"), png_file_path)


def has_vectors(png_file_path):
	return check_any(("pnormaltexture", "pbasenormaltexture", "playered_warpoffset"), png_file_path)


def has_rg_b_a(png_file_path):
	return check_any(("pbasenormaltexture",), png_file_path)


def wrapper(png_file_path, size_info, ovl):
	out_files = []
	must_split = False
	split_components = has_components(png_file_path)
	must_flip_gb = has_vectors(png_file_path)
	split_rg_b_a = has_rg_b_a(png_file_path)
	if is_ztuac(ovl):
		must_flip_gb = False
	h = size_info.height
	w = size_info.width
	if hasattr(size_info, "array_size"):
		array_size = size_info.array_size
	else:
		array_size = 1
	# hack since some games have this set to 0 sometimes
	array_size = max(1, array_size)
	if array_size > 1:
		must_split = True
	logging.debug(f"split_components {split_components}")
	logging.debug(f"must_split {must_split}")
	logging.debug(f"split_rg_b_a {split_rg_b_a}")
	logging.debug(f"must_flip_gb {must_flip_gb}")
	logging.debug("Splitting PNG array")
	logging.debug(f"h {h}, w {w}, array_size {array_size}")
	if must_split or must_flip_gb or split_components or split_rg_b_a:
		im = imageio.imread(png_file_path)
		# (4096, 1024, 4)
		h, w, d = im.shape
		h //= array_size
		name, ext = os.path.splitext(png_file_path)
		if must_flip_gb:
			flip_gb(im)
		layer_i = 0
		# split components and or tiles if present
		if split_components:
			for hi in range(array_size):
				for di in range(d):
					file_path = f"{name}_[{layer_i:02}]{ext}"
					imageio.imwrite(file_path, im[hi * h:(hi + 1) * h, :, di], compress_level=2)
					out_files.append(file_path)
					layer_i += 1
			os.remove(png_file_path)
		# only split tiles but not components
		elif must_split:
			for layer_i in range(array_size):
				file_path = f"{name}_[{layer_i:02}]{ext}"
				imageio.imwrite(file_path, im[layer_i * h:(layer_i + 1) * h, :, :], compress_level=2)
				out_files.append(file_path)
			os.remove(png_file_path)
		# separate into rgb and a components
		elif split_rg_b_a:
			for hi in range(array_size):
				file_path = f"{name}_[{layer_i}]{ext}"
				normal = np.array(im[hi * h:(hi + 1) * h, :, 0:3])
				normal[:, :, 2] = 255
				imageio.imwrite(file_path, normal, compress_level=2)
				out_files.append(file_path)
				file_path = f"{name}_[{layer_i+1}]{ext}"
				imageio.imwrite(file_path, im[hi * h:(hi + 1) * h, :, 2], compress_level=2)
				out_files.append(file_path)
				file_path = f"{name}_[{layer_i+2}]{ext}"
				imageio.imwrite(file_path, im[hi * h:(hi + 1) * h, :, 3], compress_level=2)
				out_files.append(file_path)
				layer_i += 3
			os.remove(png_file_path)
		# don't split at all, overwrite
		else:
			imageio.imwrite(png_file_path, im, compress_level=2)
			out_files.append(png_file_path)
	else:
		out_files.append(png_file_path)
	return out_files


def is_array_tile(fp, array_name_bare):
	"""Return true if fp is an array tile of array_name_bare"""
	if fp.startswith(array_name_bare):
		in_dir, in_name_ext = os.path.split(fp)
		in_name, ext = os.path.splitext(in_name_ext)
		if ext.lower() == ".png":
			in_name_bare, suffix = split_name_suffix(in_name)
			# join arrays if there is a suffix
			if suffix is not None:
				return True


def is_corresponding_png(file_name, name_bare):
	if file_name.startswith(name_bare) and file_name.lower().endswith(".png"):
		return True


def split_name_suffix(name_bare):
	# grab the basic name, and the array index suffix if it exists
	if "_" in name_bare:
		in_name_bare, suffix = name_bare.rsplit("_", 1)
		if suffix and "[" in suffix:
			suffix = suffix[1:-1]
			suffix = int(suffix)
			return in_name_bare, suffix
	return name_bare, None


def check_same_dimensions(dimensions, files):
	"""Make sure that all array tiles have the same size"""
	if not all(x == dimensions[0] for x in dimensions):
		t_str = "\n".join([f"{im} [{h} x {w}]" for (h, w), im in zip(dimensions, files)])
		raise AttributeError(f"Array tiles have different dimensions:\n{t_str}")


def png_from_tex(tex_file_path, tmp_dir):
	"""This finds and if required, creates, a png file that is ready for DDS conversion (arrays or flipped channels)"""

	logging.debug(f"Looking for .png for {tex_file_path}")
	in_dir, in_name_ext = os.path.split(tex_file_path)
	in_name, ext = os.path.splitext(in_name_ext)
	png_file_path = os.path.join(in_dir, f"{in_name}.png")
	tmp_png_file_path = os.path.join(tmp_dir, f"{in_name}.png")
	corresponding_png_textures = [file for file in os.listdir(in_dir) if is_corresponding_png(file, in_name)]
	if not corresponding_png_textures:
		raise FileNotFoundError(f"Found no .png files for {tex_file_path}")
	# print(corresponding_png_textures)
	in_name_bare, suffix = split_name_suffix(os.path.splitext(corresponding_png_textures[0])[0])
	# join arrays if there is a suffix
	must_join = suffix is not None
	join_components = has_components(tex_file_path)
	join_rg_b_a = has_rg_b_a(tex_file_path)
	must_flip_gb = has_vectors(tex_file_path)

	# check if processing needs to be done
	if not must_join and not join_components and not must_flip_gb and not join_rg_b_a:
		assert len(corresponding_png_textures) == 1
		assert os.path.isfile(png_file_path)
		logging.debug(f"Need not process {png_file_path}")
		return png_file_path

	logging.debug(f"must_join {must_join}")
	logging.debug(f"join_components {join_components}")
	logging.debug(f"join_rg_b_a {join_rg_b_a}")
	logging.debug(f"must_flip_gb {must_flip_gb}")

	# non-tiled files that need fixes - normal maps
	if not must_join and not join_components and not join_rg_b_a:
		# just read the one input file
		assert len(corresponding_png_textures) == 1
		im = imageio.imread(png_file_path)

	# rebuild array from separated tiles
	if must_join or join_components or join_rg_b_a:
		array_textures = [file for file in corresponding_png_textures if is_array_tile(file, in_name_bare)]
		# read all images into arrays
		ims = [imageio.imread(os.path.join(in_dir, file)) for file in array_textures]
		logging.debug(f"Array tile names: {array_textures}")
		# load them all, then build im array from scratch
		array_size = len(array_textures)
		# check that all textures have the right dimensions
		dimensions = []
		for im, file in zip(ims, array_textures):
			# check for depth dimension
			has_d = len(im.shape) == 3
			# RGBA or RGBA image
			if has_d:
				h, w, d = im.shape
				if d != 4:
					# rgba files, obvious need to have RGB components, so don't complain
					if not join_rg_b_a:
						raise AttributeError(f"{file} does not have all 4 channels (RGBA) that are expected, it has {d}")
				dimensions.append((h, w))
			# no 3rd dimension, ie. single channel greyscale image
			else:
				h, w = im.shape
				d = 1
				dimensions.append((h, w))
		check_same_dimensions(dimensions, array_textures)
		if join_components:
			d = 4
			array_size //= d
		if join_rg_b_a:
			d = 4
			# since we have 2 components per tile
			array_size //= 3

		logging.debug(f"array_size {array_size}")
		if array_size == 0:
			raise FileNotFoundError(
				f"Only {len(array_textures)} array texture(s) were found in {in_dir}, resulting in an incomplete array. "
				f"Make sure you inject a PNG from a folder containing all other PNGs for that array!")
		out_shape = (h * array_size, w, d)
		im = np.zeros(out_shape, dtype=ims[0].dtype)
		if join_components:
			logging.debug("Rebuilding array texture from components")
			layer_i = 0
			for hi in range(array_size):
				for di in range(d):
					tile_shape = ims[layer_i].shape
					if len(tile_shape) == 2:
						im[hi * h:(hi + 1) * h, :, di] = ims[layer_i]
					elif len(tile_shape) == 3:
						logging.warning(
							f"Tile {array_textures[layer_i]} is not the expected single-channel float format, using first channel.")
						im[hi * h:(hi + 1) * h, :, di] = ims[layer_i][:, :, 0]
					layer_i += 1
		elif join_rg_b_a:
			logging.debug("Rebuilding array texture from RG + B + A")
			layer_i = 0
			for hi in range(array_size):
				# RG
				tile_shape = ims[layer_i].shape
				if len(tile_shape) == 3:
					im[hi * h:(hi + 1) * h, :, 0:2] = ims[layer_i][:, :, 0:2]
				else:
					raise AttributeError("RGB component must be RGB or RGBA")
				layer_i += 1
				# B
				im[hi * h:(hi + 1) * h, :, 2] = get_single_channel(ims[layer_i], array_textures[layer_i])
				layer_i += 1
				# A
				im[hi * h:(hi + 1) * h, :, 3] = get_single_channel(ims[layer_i], array_textures[layer_i])
				layer_i += 1
		else:
			logging.debug("Rebuilding array texture from RGBA tiles")
			for layer_i in range(array_size):
				im[layer_i * h:(layer_i + 1) * h, :, :] = ims[layer_i]

	# flip the green and blue channels of the array
	if must_flip_gb:
		flip_gb(im)

	# this is shared for all that have to be read
	logging.debug(f"Writing output to {tmp_png_file_path}")
	imageio.imwrite(tmp_png_file_path, im, compress_level=2)
	return tmp_png_file_path


def get_single_channel(im, name):
	tile_shape = im.shape
	if len(tile_shape) == 2:
		return im
	elif len(tile_shape) == 3:
		logging.warning(f"Tile {name} is not the expected single-channel float format, using first channel.")
		return im[:, :, 0]
