import os
import imageio

def wrapper(png_file_path, header_7):
	must_split = False
	split_components = False
	flip_gb = False
	if "playered_blendweights" in png_file_path:
		split_components = True
	if "pnormaltexture" in png_file_path or "playered_warpoffset" in png_file_path:
		flip_gb = True
	if header_7.array_size > 1:
		must_split = True
	print("Splitting PNG array")
	h = header_7.height
	w = header_7.width
	array_size = header_7.array_size
	print("h, w, array_size",h, w, array_size)
	if must_split or flip_gb:
		im = imageio.imread(png_file_path)
		print(im.shape)
		(4096, 1024, 4)
		h, w, d = im.shape
		h //= array_size
		name, ext = os.path.splitext(png_file_path)
		if flip_gb:
			im[:,:,1] = 255-im[:,:,1]
			im[:,:,2] = 255-im[:,:,2]
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
