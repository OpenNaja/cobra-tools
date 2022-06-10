# an experiment
import logging
import os

# from ovl_util.config import logging_setup

# logging_setup("ovl_tool_gui")
from generated.formats.dinosaurmaterialvariants.compound.DinoLayersHeader import DinoLayersHeader
from generated.formats.fgm.compound.FgmHeader import FgmHeader
from generated.formats.ovl_base import OvlContext


class LayeredMaterial:

	def __init__(self):
		self.layers = []

	def create_node(self):
		pass

	def load_mat_layers(self, layers_path):
		base_dir, layers_name = os.path.split(layers_path)
		basename, ext = os.path.splitext(layers_name)
		matname = basename.split("_layers")[0]
		logging.info(f"Material: {matname}")
		layers_root = DinoLayersHeader.from_xml_file(layers_path, OvlContext())
		for mask_i, layer in enumerate(layers_root.layers.data):
			mask_png_path = os.path.join(base_dir, f"{matname}.playered_blendweights_[{mask_i:02}].png")
			tex_fgm_path = get_fgm_path(base_dir, layer.texture_fgm_name)
			trans_fgm_path = get_fgm_path(base_dir, layer.transform_fgm_name)
			if not os.path.isfile(mask_png_path):
				logging.info(f"Found no mask texture for layer {mask_i}")
			elif not tex_fgm_path:
				logging.info(f"No texture fgm for layer {mask_i}")
			elif not trans_fgm_path:
				logging.info(f"No transform fgm for layer {mask_i}")
			else:
				logging.info(f"Layer {mask_i} is tiled")
				if os.path.isfile(tex_fgm_path) and os.path.isfile(trans_fgm_path):
					logging.info(f"Found files for layer")
					# self.layers.append(Layer(tex_fgm_path, trans_fgm_path))
					tex_fgm = FgmHeader.from_xml_file(tex_fgm_path, OvlContext())
					trans_fgm = FgmHeader.from_xml_file(trans_fgm_path, OvlContext())
					# print(self.tex_fgm)
					height_tex = tex_fgm.textures.data[1]
					height_dep = tex_fgm.dependencies.data[1]
					height_file_name = height_dep.dependency_name.data
					height_file_basename = os.path.splitext(height_file_name)[0]
					array_index = height_tex.value[0].array_index
					# print(height_file_name, array_index)
					tile_png_path = os.path.join(base_dir, f"{height_file_basename}_[{array_index:02}].png")
					if not os.path.isfile(tile_png_path):
						logging.info(f"Found no tile texture for layer {mask_i}")
					# print(tile_png_path)
					self.layers.append((mask_png_path, tile_png_path, trans_fgm))


# class Layer:
#
# 	def __init__(self, tex_fgm_path, trans_fgm_path):
# 		self.tex_fgm = FgmHeader.from_xml_file(tex_fgm_path, OvlContext())
# 		self.trans_fgm = FgmHeader.from_xml_file(trans_fgm_path, OvlContext())
# 		# print(self.tex_fgm)
# 		height_tex = self.tex_fgm.textures.data[1]
# 		height_dep = self.tex_fgm.dependencies.data[1]
# 		height_file_name = height_dep.dependency_name.data
# 		array_index = height_tex.value[0].array_index
# 		print(height_file_name, array_index)


def get_fgm_path(base_dir, fgm_name_ptr):
	fgm_basename = fgm_name_ptr.data
	if fgm_basename:
		fgm_path = os.path.join(base_dir, f"{fgm_basename}.fgm")
		return fgm_path


if __name__ == "__main__":
	# load_mat_layers("C:/Users/arnfi/Desktop/anim/tylosaurus_layers.dinosaurmateriallayers")
	layers = LayeredMaterial()
	layers.load_mat_layers("C:/Users/arnfi/Desktop/anim/ichthyosaurus_layers.dinosaurmateriallayers")
