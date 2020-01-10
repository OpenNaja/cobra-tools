import os
import imageio
import numpy as np

def flip_gb(im):
	"""Flips green and blue channels of image array"""
	im[:,:,1] = 255-im[:,:,1]
	im[:,:,2] = 255-im[:,:,2]

def check_any(iterable, string):
	"""Returns true if any of the entries of the iterable occur in string"""
	return any([i in string for i in iterable])

def has_components(png_file_path):
	return check_any(("playered_blendweights", "pbasepackedtexture", "proughnesspackedtexture", "pbaldnessscartexture", "markingbaldnessscartexture", "markingscartexture"), png_file_path)

def has_vectors(png_file_path):
	return check_any(("pnormaltexture", "playered_warpoffset"), png_file_path)

def wrapper(png_file_path, header_7):
	must_split = False
	split_components = has_components(png_file_path)
	must_flip_gb = has_vectors(png_file_path)
	if header_7.array_size > 1:
		must_split = True
	print("split_components", split_components)
	print("must_split", must_split)
	print("must_flip_gb", must_flip_gb)
	print("Splitting PNG array")
	h = header_7.height
	w = header_7.width
	array_size = header_7.array_size
	print("h, w, array_size",h, w, array_size)
	if must_split or must_flip_gb or split_components:
		im = imageio.imread(png_file_path)
		# print(im.shape)
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
					imageio.imwrite(name+f"_{layer_i:02}"+ext, im[hi*h:(hi+1)*h, :, di], compress_level=2)
					layer_i += 1
			os.remove(png_file_path)
		# only split tiles but not components
		elif must_split:
			for layer_i in range(array_size):
				imageio.imwrite(name+f"_{layer_i:02}"+ext, im[layer_i*h:(layer_i+1)*h, :, :], compress_level=2)
			os.remove(png_file_path)
		# don't split at all, overwrite
		else:
			imageio.imwrite(png_file_path, im, compress_level=2)

def is_array_tile(fp, array_name_bare):
	"""Return true if fp is an array tile of array_name_bare"""
	if fp.startswith(array_name_bare):
		in_dir, in_name_ext = os.path.split(fp)
		in_name, ext = os.path.splitext(in_name_ext)
		if ext.lower() == ".png":
			in_name_bare, suffix = split_name_suffix(in_name)
			# join arrays if there is a suffix
			if suffix != None:
				return True

def split_name_suffix(in_name):
	# grab the basic name, and the array index suffix if it exists
	try:
		in_name_bare, suffix = in_name.rsplit("_", 1)
		print(in_name_bare, suffix)
		suffix = int(suffix)
	except:
		in_name_bare = in_name
		suffix = None
	print("bare name",in_name_bare)
	print("suffix", suffix)
	return in_name_bare, suffix

def inject_wrapper(png_file_path, dupecheck, tmp_dir):
	"""This handles PNG modifications (arrays or flipped channels) and ensures the costly IO is only done once"""

	must_join = False
	join_components = has_components(png_file_path)
	must_flip_gb = has_vectors(png_file_path)
	
	print("PNG injection wrapper input",png_file_path)
	in_dir, in_name_ext = os.path.split(png_file_path)
	in_name, ext = os.path.splitext(in_name_ext)

	in_name_bare, suffix = split_name_suffix(in_name)
	# join arrays if there is a suffix
	must_join = suffix is not None

	# update output path
	out_file_path = os.path.join(tmp_dir, in_name_bare + ext)
	print("checking if dupe",out_file_path)
	if out_file_path in dupecheck:
		return
	dupecheck.append(out_file_path)

	print("must_join", must_join)
	print("join_components", join_components)
	print("must_flip_gb", must_flip_gb)

	# we can just return the original file
	if not must_join and not join_components and not must_flip_gb:
		return png_file_path

	# non-tiled files that need fixes - normal maps
	if not must_join and not join_components:
		# just read the one input file
		im = imageio.imread(png_file_path)
	
	# rebuild array from separated tiles
	if must_join or join_components:
		array_textures = [file for file in os.listdir(in_dir) if is_array_tile(file, in_name_bare)]
		# read all images into arrays
		ims = [imageio.imread(os.path.join(in_dir, file)) for file in array_textures]
		print("Array tile names:")
		print(array_textures)
		# load them all, then build im array from scratch
		array_size = len(array_textures)
		# check that all textures have the right dimensions
		for im, file in zip(ims, array_textures):
			in_shape = ims[0].shape
			# check for depth dimension
			has_d = len(in_shape) == 3
			# RGBA or RGBA image
			if has_d:
				h, w, d = in_shape
				if d != 4:
					raise AttributeError(f"{file} does not have all 4 channels (RGBA) that are expected, it has {d}")
			# no 3rd dimension, ie. single channel greyscale image
			else:
				h, w = in_shape
				d = 1
		if join_components:
			d = 4
			array_size //= d
		print("array_size",array_size)
		out_shape = (h*array_size, w, d)
		im = np.zeros(out_shape, dtype=ims[0].dtype)
		if join_components:
			print("Rebuilding array texture from components")
			layer_i = 0
			for hi in range(array_size):
				for di in range(d):
					tile_shape = ims[layer_i].shape
					if len(tile_shape) == 2:
						im[hi*h:(hi+1)*h, :, di] = ims[layer_i]
					elif len(tile_shape) == 3:
						print(f"Tile {array_textures[layer_i]} is not the expected single-channel float format, using first channel.")
						im[hi*h:(hi+1)*h, :, di] = ims[layer_i][:, :, 0]
					layer_i += 1
		else:
			print("Rebuilding array texture from RGBA tiles")
			for layer_i in range(array_size):
				im[layer_i*h:(layer_i+1)*h, :, :] = ims[layer_i]

	# flip the green and blue channels of the array
	if must_flip_gb:
		flip_gb(im)
	
	# this is shared for all that have to be read
	print("Writing png output")
	imageio.imwrite(out_file_path, im, compress_level=2)
	return out_file_path