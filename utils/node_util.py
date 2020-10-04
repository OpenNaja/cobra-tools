import os
import bpy


def get_tree(mat):
	mat.use_nodes = True

	tree = mat.node_tree
	# clear default nodes
	for node in tree.nodes:
		tree.nodes.remove(node)
	return tree


def load_tex(tree, tex_path):
	name = os.path.basename(tex_path)
	if name not in bpy.data.images:
		try:
			img = bpy.data.images.load(tex_path)
		except:
			print("Could not find image "+tex_path+", generating blank image!")
			img = bpy.data.images.new(name, 1, 1)
	else:
		img = bpy.data.images[name]
	tex = tree.nodes.new('ShaderNodeTexImage')
	tex.image = img
	tex.interpolation = "Smart"

	return tex