import os
import imageio

def flip_gb(im):
	"""Flips green and blue channels of image array"""
	im[:,:,1] = 255-im[:,:,1]
	im[:,:,2] = 255-im[:,:,2]

def wrapper(png_file_path, header_7):
	must_split = False
	split_components = False
	must_flip_gb = False
	if "playered_blendweights" in png_file_path:
		split_components = True
	if "pnormaltexture" in png_file_path or "playered_warpoffset" in png_file_path:
		must_flip_gb = True
	if header_7.array_size > 1:
		must_split = True
	print("Splitting PNG array")
	h = header_7.height
	w = header_7.width
	array_size = header_7.array_size
	print("h, w, array_size",h, w, array_size)
	if must_split or must_flip_gb:
		im = imageio.imread(png_file_path)
		# print(im.shape)
		# (4096, 1024, 4)
		h, w, d = im.shape
		h //= array_size
		name, ext = os.path.splitext(png_file_path)
		if must_flip_gb:
			flip_gb(im)
		if must_split:
			if split_components:
				layer_i = 0
				for hi in range(array_size):
					for di in range(d):
						imageio.imwrite(name+f"_{layer_i:02}"+ext, im[hi*h:(hi+1)*h, :, di])
						layer_i += 1
			else:
				for layer_i in range(array_size):
					imageio.imwrite(name+f"_{layer_i:02}"+ext, im[layer_i*h:(layer_i+1)*h, :, :])
			os.remove(png_file_path)
		else:
			imageio.imwrite(png_file_path, im)

def inject_wrapper(png_file_path, dupecheck, tmp_dir):
	"""This handles PNG modifications (arrays or flipped channels) and ensures the costly IO is only done once"""
	print("PNG injection wrapper input",png_file_path)
	in_dir, in_name_ext = os.path.split(png_file_path)
	in_name, ext = os.path.splitext(in_name_ext)
	# grab the basic name, and the array index suffix if it exists
	try:
		in_name_bare, suffix = in_name.rsplit("_", 1)
		suffix = int(suffix)
		must_join = True
		print("bare name",in_name_bare)
		print("suffix", suffix)
	except:
		in_name_bare = in_name

	# update output path
	out_file_path = os.path.join(tmp_dir, in_name_bare+ext)
	print("checking if dupe",out_file_path)
	if out_file_path in dupecheck:
		return
	dupecheck.append(out_file_path)

	# out_file_path = png_file_path
	must_join = False
	join_components = False
	must_flip_gb = False
	if "playered_blendweights" in png_file_path:
		join_components = True
	if "pnormaltexture" in png_file_path or "playered_warpoffset" in png_file_path:
		must_flip_gb = True
	print("must_join", must_join)
	print("join_components", join_components)
	print("must_flip_gb", must_flip_gb)

	# we can just return the original file
	if not must_join and not join_components and not must_flip_gb:
		return png_file_path

	# non-tilef files that need fixes - normal maps
	if not must_join and not join_components:
		# just read the one input file
		im = imageio.imread(png_file_path)
	
	# rest is not supported for now
	if must_join or join_components:
		array_textures = [file for file in os.listdir(in_dir) if file.startswith(in_name_bare)]
		print("Loading pieces of an array texture is not supported right now")
		print(array_textures)
		# load them all, then build im array from scratch
		return

	# flip the green and blue channels of the array
	if must_flip_gb:
		flip_gb(im)
	
	# this is shared for all that have to be read
	imageio.imwrite(out_file_path, im)
	return out_file_path