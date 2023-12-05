import logging

import bpy
import math
from bpy_types import bpy_types
import os

from constants import ConstantsProvider
from generated.array import Array
from generated.formats.fgm.compounds.FgmHeader import FgmHeader
from generated.formats.fgm.compounds.TexIndex import TexIndex
from generated.formats.fgm.compounds.TextureData import TextureData
from generated.formats.fgm.compounds.TextureInfo import TextureInfo
from generated.formats.fgm.enums.FgmDtype import FgmDtype
from generated.formats.ms2 import Ms2Version, get_game, Ms2Context
from generated.formats.ovl import set_game, games
from generated.formats.ovl_base import OvlContext
from generated.formats.tex.compounds.SizeInfo import SizeInfo
from generated.formats.tex.compounds.TexHeader import TexHeader
from generated.formats.tex.enums.DdsType import DdsType


def write_file(path, content, overwrite=False):
	""" write  content to a file
	:param path: file path
	:param content: the content to write
	:return: content of the file
	"""
	if overwrite is False and os.path.exists(path):
		return
	try:
		os.makedirs(os.path.dirname(path))
	except:
		pass
	with open(path, 'w', newline='') as f:
		print(f"Creating {path}")
		f.write(content.strip())


def get_object_names(col):
	obj_names = [o.name for o in bpy.data.collections[col.name].objects if
				 '_Hitcheck' not in o.name and o.hide_render == False]
	return obj_names


def get_object_material_names(ob):
	mats = []
	if ob.type == "MESH":
		for mat_slot in ob.material_slots:
			if mat_slot.material:
				mat = mat_slot.material
				mats.append(mat.name)
	return mats


def get_unique_material_names(col):
	materials = []
	for obj_name in get_object_names(col):
		ob = bpy.data.objects[obj_name]
		mat_names = get_object_material_names(ob)
		missing = (set(mat_names) - set(materials))
		materials.extend(missing)
	return materials


def get_shared_material_names(col):
	materials = []
	mat_names = get_unique_material_names(col)
	for mat_name in mat_names:
		mat = bpy.data.materials[mat_name]
		if mat.users > 1:
			materials.append(mat_name)
	return materials


def generate_material_attributes(folder, mat_name):
	""" Creates the Attributes section of the FGM using the
		existing fgm property collection
	"""
	mat = bpy.data.materials[mat_name]
	attributes = "     <attributes>\n"
	for key in mat.fgm.__annotations__.keys():

		default_value = getattr(mat.fgm, key)
		try:
			value = mat.fgm[key]
		except:
			value = default_value

		if key == 'pWeather_Enable':
			print('WEATHER ' + str(type(value)) + " " + str(type(default_value)))

		dtype = ''
		name = key
		# ignore extra attributes we don't need to export.
		if type(default_value) is str:
			pass

		elif type(default_value) is float:
			dtype = 'FLOAT'

		elif type(default_value) is int:
			dtype = 'INT'

		elif type(default_value) is bool:
			dtype = 'BOOL'
			value = int(value)

		elif isinstance(value, bpy_types.bpy_prop_array) or str(type(default_value)) == "<class 'Vector'>":
			dtype = 'FLOAT_3'
			value = str(value[0]) + " " + str(value[1]) + " " + str(value[2])

		else:
			print(key + " " + str(value) + " " + str(type(value)))
			raise TypeError("Wrong Attribute Type")

		if dtype is not '':
			attribute = f"        <attribinfo name=\"{name}\" dtype=\"FgmDtype.{dtype}\">\n            <value>{value}</value>\n        </attribinfo>\n"
			attributes += attribute

	attributes += "     </attributes>\n"
	return attributes


def generate_material_info(folder, mat_name, fgm_root, mod_game, shader_name):
	mat = bpy.data.materials[mat_name]
	textures = [x.image.name for x in mat.node_tree.nodes if x.type == 'TEX_IMAGE']
	# print("Material textures: " + str(textures))
	slots = {
		"_BC": "Base colour",
		"_SM": "Smoothness",
		"_RN": "Roughness",
		"_CA": "Cavity",
		"_AO": "Ambient Occlusion",
		"_MT": "Metalness",
		"_NM": "Normal Map",
		"_NG": "Normal Map Variant",
		"_OP": "Alpha Clip",
		"_AL": "Alpha Blend",
		"_EM": "Emissive",
		"_SP": "Specular",
		"_F1": "Flexi Colour Alpha Blend Mask 01",
		"_F2": "Flexi Colour Alpha Blend Mask 02",
		"_F3": "Flexi Colour Alpha Blend Mask 03",
		"_F4": "Flexi Colour Alpha Blend Mask 04",
		# custom keys follow
		"_FO": "Flexi Opacity",
	}
	# populate colours from BSDF node.
	bsdf = mat.node_tree.nodes.get("Principled BSDF")
	defaults = {
		# cast RGBA to list
		"_BC": list(bsdf.inputs["Base Color"].default_value),
		# "_SM": "Smoothness",
		"_RN": [bsdf.inputs["Roughness"].default_value, ],
		"_CA": [1.0, 1.0, 1.0, 1.0],
		"_AO": [1.0, 1.0, 1.0, 1.0],
		"_MT": [bsdf.inputs["Metallic"].default_value, ],
		"_NM": [0.5, 0.5, 1.0, 1.0],
		# "_NG": "Normal Map Variant",
		"_OP": [bsdf.inputs["Alpha"].default_value, ],
		# "_AL": "Alpha Blend",
		"_EM": list(bsdf.inputs["Emission"].default_value),
		"_SP": [bsdf.inputs["Specular"].default_value, ],
		# "_F1": "Flexi Colour Alpha Blend Mask 01",
		# "_F2": "Flexi Colour Alpha Blend Mask 02",
		# "_F3": "Flexi Colour Alpha Blend Mask 03",
		# "_F4": "Flexi Colour Alpha Blend Mask 04",
		"_FO": [1.0, ],
	}
	# populate material textures
	texture_info = {}
	for slot, slot_desc in slots.items():
		slot_key = f"{mat_name}{slot}"
		# todo - use node label? or file name
		if slot_key in textures:
			texture_info[slot] = bpy.data.images[slot_key]
		else:
			texture_info[slot] = defaults.get(slot, None)

	c = ConstantsProvider(("shaders", "textures"))
	try:
		tex_channel_map = c[mod_game.value]["textures"][shader_name]
	except:
		logging.warning(f"No presets for shader '{shader_name}' game {mod_game}")
		raise
	# print(tex_channel_map)
	for tex_name, tex_keys in tex_channel_map.items():

		tex_index = TexIndex(fgm_root.context)

		tex = TextureInfo(fgm_root.context)
		tex.name = tex_name
		dep = TextureData(fgm_root.context, arg=tex)

		raw_entries = [texture_info[k] for k in tex_keys]
		raw_types = [type(e) for e in raw_entries]
		print(tex_name, raw_entries, raw_types)
		if any(k in (bpy.types.Image, ) for k in raw_types):
			# texture needs to be used or generated
			tex.dtype = FgmDtype.TEXTURE
			tex.reset_field("value")
			tex.value[:] = [tex_index]
			dep.dependency_name.data = f'{mat_name}.{tex_name}.tex'
			size = textures_find_size(raw_entries)
			print(f"size: {size}")
			for tk, t_channel in tex_keys.items():
				texture_save_or_generate(texture_info[tk], folder, f'{mat_name}.{tex_name}{t_channel}.png', size)
			tex_path = os.path.join(folder, f'{mat_name}.{tex_name}.tex')
			# pick suitable DDS compression
			comp = "BC7_UNORM"
			if tex_name == "pNormalTexture" and len(tex_keys) == 1:
				comp = "BC5_UNORM"
			tex_file = TexHeader(tex.context)
			# pick reasonable stream count
			tex_file.stream_count = 1
			tex_file.size_info.data = SizeInfo(tex_file.context)
			size_info = tex_file.size_info.data.data
			# pick empty MIP setting so that they are filled by the plugin
			size_info.num_mips = 0
			# todo - PC would need its own DdsTypeCoaster enum
			tex_file.compression_type = DdsType[comp]
			with tex_file.to_xml_file(tex_file, tex_path) as xml_root:
				pass
		else:
			# only RGBA input
			tex.dtype = FgmDtype.RGBA
			tex.reset_field("value")
			dep.dependency_name.data = ''
			# flatten used colors
			keys = [channel for group in raw_entries if group is not None for channel in group]
			# don't store if less than 4 values
			if len(keys) < 4:
				continue
			for v in tex.value:
				v.r, v.g, v.b, v.a = [int(channel*255) for channel in keys[:4]]
		fgm_root.textures.data.append(tex)
		fgm_root.name_foreach_textures.data.append(dep)


def export_fgm_at(folder, mod_game, mat_name):
	print("\nExporting Material: " + os.path.join(folder, mat_name + '.fgm'))
	b_mat = bpy.data.materials[mat_name]
	print("Shader type: " + b_mat.blend_method)
	textures = [x.image.name for x in b_mat.node_tree.nodes if x.type == 'TEX_IMAGE']
	print("Material textures: " + str(textures))
	# populate material textures

	context = OvlContext()
	set_game(context, mod_game.value)
	# export the curve data
	fgm_root = FgmHeader(context)
	fgm_root.textures.data = Array(context, 0, None, (0,), fgm_root.textures.template)
	fgm_root.attributes.data = Array(context, 0, None, (0,), fgm_root.attributes.template)
	fgm_root.name_foreach_textures.data = Array(context, fgm_root.textures, None, (0,), fgm_root.name_foreach_textures.template)
	fgm_root.value_foreach_attributes.data = Array(context, fgm_root.attributes, None, (0,), fgm_root.value_foreach_attributes.template)

	# get shader from b_mat
	fgm_root.shader_name = b_mat.fgm.shader_name
	print(fgm_root.shader_name)
	generate_material_info(folder, mat_name, fgm_root, mod_game, fgm_root.shader_name)
	fgm_path = os.path.join(folder, mat_name + ".fgm")
	with FgmHeader.to_xml_file(fgm_root, fgm_path) as xml_root:
		pass


def textures_find_size(data):
	size = [0, 0]
	for tex in data:
		if type(tex) == type(None):
			return size

		print(str(type(tex)))
		if type(tex) is not list and type(tex) is not float:
			if size[0] == 0:
				size = tex.size
			else:
				if size[0] != tex.size[0] or size[1] != tex.size[1]:
					raise TypeError(tex.name + "size mismatch")
	return size


def is_power_of_two(value):
	if value == 0:
		return False
	return math.ceil(math.log2(value)) == math.floor(math.log2(value))


def is_allowed_size(size):
	return size[0] in range(1, 4096) and size[1] in range(1, 4096)


def validate_image(img):
	if not is_allowed_size(img.size):
		raise TypeError("TextureTooLarge")
	if not is_power_of_two(img.size[0]) or not is_power_of_two(img.size[1]):
		raise TypeError("TextureSizeInvalid")


def image_new(name, width, height, r, g, b, a):
	img = bpy.data.images.new(name, width=1, height=1)
	# assign pixels
	img.pixels = [r, g, b, a]
	img.update()
	img.scale(width, height)
	img.update()
	return img


def texture_save_or_generate(data, base_path, file_name, size):
	if size[0] == 0:
		return

	if type(data) is list:
		# Colour input as RGBA
		img = image_new(file_name, size[0], size[1], *data)
		img.file_format = 'PNG'
		img.save(filepath=os.path.join(base_path, file_name), quality=100)
		bpy.data.images.remove(img)
	elif type(data) is float:
		# Colour input as a single float value
		img = image_new(file_name, size[0], size[1], data, data, data, 255)
		img.file_format = 'PNG'
		img.save(filepath=os.path.join(base_path, file_name), quality=100)
		bpy.data.images.remove(img)
	else:
		# Colour input from another image
		img = data
		old_format = img.file_format
		img.file_format = 'PNG'
		img.save(filepath=os.path.join(base_path, file_name), quality=100)
		img.file_format = old_format


def save(filepath=""):
	folder, mat_name = os.path.split(filepath)
	b_mat = bpy.context.active_object.active_material
	mat_name = b_mat.name
	# get game from GUI dropdown
	context = Ms2Context()
	context.version = bpy.context.scene.cobra.version
	game_item = get_game(context)[0]
	# mod_game = bpy.data.collections["Collection"].mod.game
	# game_item = games[mod_game]
	print(game_item)

	export_fgm_at(folder, game_item, mat_name)
	return f"Finished FGM export",
