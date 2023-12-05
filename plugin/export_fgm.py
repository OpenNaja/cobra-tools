import logging

import bpy
import math
from bpy_types import bpy_types
import os
from string import Template
import base64

from constants import ConstantsProvider
from generated.array import Array
from generated.formats.fgm.compounds.FgmHeader import FgmHeader
from generated.formats.fgm.compounds.TexIndex import TexIndex
from generated.formats.fgm.compounds.TextureData import TextureData
from generated.formats.fgm.compounds.TextureInfo import TextureInfo
from generated.formats.fgm.enums.FgmDtype import FgmDtype
from generated.formats.ovl import set_game
from generated.formats.ovl_base import OvlContext
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
		if slot_key in textures:
			texture_info[slot] = bpy.data.images[slot_key]
		else:
			texture_info[slot] = defaults.get(slot, None)

	c = ConstantsProvider(("shaders", "textures"))
	try:
		# print(c[mod_game])
		tex_channel_map = c[mod_game]["textures"][shader_name]
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
			# todo - pick reasonable MIP setting
			# todo - pick reasonable stream count
			tex_file = TexHeader(tex.context)
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
	mat = bpy.data.materials[mat_name]
	print("Shader type: " + mat.blend_method)
	textures = [x.image.name for x in mat.node_tree.nodes if x.type == 'TEX_IMAGE']
	print("Material textures: " + str(textures))
	# populate material textures

	context = OvlContext()
	set_game(context, mod_game)
	# export the curve data
	fgm_root = FgmHeader(context)
	fgm_root.textures.data = Array(context, 0, None, (0,), fgm_root.textures.template)
	fgm_root.attributes.data = Array(context, 0, None, (0,), fgm_root.attributes.template)
	fgm_root.name_foreach_textures.data = Array(context, fgm_root.textures, None, (0,), fgm_root.name_foreach_textures.template)
	fgm_root.value_foreach_attributes.data = Array(context, fgm_root.attributes, None, (0,), fgm_root.value_foreach_attributes.template)

	fgm_root.shader_name = "Metallic_Roughness_Opaque_EmissiveLightType_Weather"
	if mod_game in ("Jurassic World Evolution", "Jurassic World Evolution 2", ):
		fgm_root.shader_name = "Metallic_Roughness_Opaque_Emissive"
	generate_material_info(folder, mat_name, fgm_root, mod_game, fgm_root.shader_name)
	# generate_material_textures(mat.name, texture_info)
	# fgm_root.game = mod_game
	fgm_path = os.path.join(folder, mat_name + ".fgm")
	with FgmHeader.to_xml_file(fgm_root, fgm_path) as xml_root:
		pass


## process texture_info to create textures

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
	pixels = [None] * 1 * 1
	for x in range(1):
		for y in range(1):
			# assign RGBA to something useful
			pixels[(y * 1) + x] = [r, g, b, a]

	# flatten list
	pixels = [chan for px in pixels for chan in px]

	# assign pixels
	img.pixels = pixels
	img.update()
	img.scale(width, height)
	img.update()
	return img


def texture_save_or_generate(data, base_path, file_name, size):
	if size[0] == 0:
		return

	if type(data) is list:
		# Colour input as RGBA
		img = image_new(file_name, size[0], size[1], data[0], data[1], data[2], data[3])
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
		pass


def export_tex_at(folder, mod_game, mat_name):
	print("\nExporting Textures: " + os.path.join(folder, mat_name + '.*'))

	print("\nExporting Material: " + os.path.join(folder, mat_name + '.fgm'))
	mat = bpy.data.materials[mat_name]
	print("Shader type: " + mat.blend_method)
	textures = [x.image.name for x in mat.node_tree.nodes if x.type == 'TEX_IMAGE']
	print("Material textures: " + str(textures))

	# todo integrate into new code
	# pBaseColourTexture
	if type(data['_BC']) is list and type(data['_CA']) is list:
		# print('ADD BASECOLOUR AS COLOURS ONLY\n')
		pass
	else:
		size = textures_find_size([data['_BC'], data['_CA']])
		print('pBaseColourSize = ' + str(size[0]) + " " + str(size[0]))
		texture_save_or_generate(data['_BC'], folder, mat_name + '.pBaseColourTexture_RGB.png', size)
		texture_save_or_generate(data['_CA'], folder, mat_name + '.pBaseColourTexture_A.png', size)
		# DdsType.BC1_UNORM_SRGB
		if size[0] > 0:
			texture_data = base64.b64decode(
				'PFRleEhlYWRlciBjb21wcmVzc2lvbl90eXBlPSJEZHNUeXBlLkJDMV9VTk9STV9TUkdCIiBvbmVfMD0iMCIgc3RyZWFtX2NvdW50PSIyIiBzdHJlYW1fY291bnRfcmVwZWF0PSIyIiBnYW1lPSJHYW1lcy5QTEFORVRfWk9PIj4NCgk8YnVmZmVyX2luZm9zIHBvb2xfdHlwZT0iMyI+DQoJCTx0ZXhidWZmZXIgb2Zmc2V0PSIwIiBzaXplPSIxNjM4NDAiIGZpcnN0X21pcD0iMCIgbWlwX2NvdW50PSIyIiAvPg0KCQk8dGV4YnVmZmVyIG9mZnNldD0iMTYzODQwIiBzaXplPSIxNzQwOCIgZmlyc3RfbWlwPSIyIiBtaXBfY291bnQ9IjgiIC8+DQoJPC9idWZmZXJfaW5mb3M+DQoJPHNpemVfaW5mbyBwb29sX3R5cGU9IjQiPg0KCQk8ZGF0YSBkYXRhX3NpemU9IjE4MTI0OCIgd2lkdGg9IjUxMiIgaGVpZ2h0PSI1MTIiIG51bV9taXBzPSIxMCI+DQoJCQk8bWlwX21hcHM+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjAiIHNpemU9IjEzMTA3MiIgc2l6ZV9hcnJheT0iMTMxMDcyIiBzaXplX3NjYW49IjEwMjQiIHNpemVfZGF0YT0iMTMxMDcyIiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIxMzEwNzIiIHNpemU9IjMyNzY4IiBzaXplX2FycmF5PSIzMjc2OCIgc2l6ZV9zY2FuPSI1MTIiIHNpemVfZGF0YT0iMzI3NjgiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjE2Mzg0MCIgc2l6ZT0iODE5MiIgc2l6ZV9hcnJheT0iODE5MiIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iODE5MiIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMTcyMDMyIiBzaXplPSI0MDk2IiBzaXplX2FycmF5PSI0MDk2IiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSI0MDk2IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIxNzYxMjgiIHNpemU9IjIwNDgiIHNpemVfYXJyYXk9IjIwNDgiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjIwNDgiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjE3ODE3NiIgc2l6ZT0iMTAyNCIgc2l6ZV9hcnJheT0iMTAyNCIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iMTAyNCIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMTc5MjAwIiBzaXplPSI1MTIiIHNpemVfYXJyYXk9IjUxMiIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iNTEyIiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIxNzk3MTIiIHNpemU9IjUxMiIgc2l6ZV9hcnJheT0iNTEyIiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSIyNTYiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjE4MDIyNCIgc2l6ZT0iNTEyIiBzaXplX2FycmF5PSI1MTIiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjI1NiIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMTgwNzM2IiBzaXplPSI1MTIiIHNpemVfYXJyYXk9IjUxMiIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iMjU2IiAvPg0KCQkJPC9taXBfbWFwcz4NCgkJPC9kYXRhPg0KCQk8cGFkZGluZz4wIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDA8L3BhZGRpbmc+DQoJPC9zaXplX2luZm8+DQo8L1RleEhlYWRlcj4=').decode(
				'utf-8')
			write_file(os.path.join(folder, mat_name + ".pBaseColourTexture.tex"), texture_data, True)

	# pNormalTexture
	if mod_game in ('PLANET_ZOO', 'PLANET_COASTER'):
		if type(data['_NM']) is list:
			# print('ADD NORMAL AS COLOURS ONLY\n')
			pass
		else:
			size = textures_find_size([data['_NM']])
			print('pNormalSize = ' + str(size[0]) + " " + str(size[0]))
			texture_save_or_generate(data['_NM'], folder, mat_name + '.pNormalTexture_RG.png', size)
			# DdsType.BC5_UNORM
			if size[0] > 0:
				texture_data = base64.b64decode(
					'PFRleEhlYWRlciBjb21wcmVzc2lvbl90eXBlPSJEZHNUeXBlLkJDNV9VTk9STSIgb25lXzA9IjAiIHN0cmVhbV9jb3VudD0iMiIgc3RyZWFtX2NvdW50X3JlcGVhdD0iMiIgZ2FtZT0iR2FtZXMuUExBTkVUX1pPTyI+DQoJPGJ1ZmZlcl9pbmZvcyBwb29sX3R5cGU9IjMiPg0KCQk8dGV4YnVmZmVyIG9mZnNldD0iMCIgc2l6ZT0iMzI3NjgwIiBmaXJzdF9taXA9IjAiIG1pcF9jb3VudD0iMiIgLz4NCgkJPHRleGJ1ZmZlciBvZmZzZXQ9IjMyNzY4MCIgc2l6ZT0iMjU2MDAiIGZpcnN0X21pcD0iMiIgbWlwX2NvdW50PSI4IiAvPg0KCTwvYnVmZmVyX2luZm9zPg0KCTxzaXplX2luZm8gcG9vbF90eXBlPSI0Ij4NCgkJPGRhdGEgZGF0YV9zaXplPSIzNTMyODAiIHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiBudW1fbWlwcz0iMTAiPg0KCQkJPG1pcF9tYXBzPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIwIiBzaXplPSIyNjIxNDQiIHNpemVfYXJyYXk9IjI2MjE0NCIgc2l6ZV9zY2FuPSIyMDQ4IiBzaXplX2RhdGE9IjI2MjE0NCIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMjYyMTQ0IiBzaXplPSI2NTUzNiIgc2l6ZV9hcnJheT0iNjU1MzYiIHNpemVfc2Nhbj0iMTAyNCIgc2l6ZV9kYXRhPSI2NTUzNiIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMzI3NjgwIiBzaXplPSIxNjM4NCIgc2l6ZV9hcnJheT0iMTYzODQiIHNpemVfc2Nhbj0iNTEyIiBzaXplX2RhdGE9IjE2Mzg0IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIzNDQwNjQiIHNpemU9IjQwOTYiIHNpemVfYXJyYXk9IjQwOTYiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjQwOTYiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjM0ODE2MCIgc2l6ZT0iMjA0OCIgc2l6ZV9hcnJheT0iMjA0OCIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iMjA0OCIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMzUwMjA4IiBzaXplPSIxMDI0IiBzaXplX2FycmF5PSIxMDI0IiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSIxMDI0IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIzNTEyMzIiIHNpemU9IjUxMiIgc2l6ZV9hcnJheT0iNTEyIiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSI1MTIiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjM1MTc0NCIgc2l6ZT0iNTEyIiBzaXplX2FycmF5PSI1MTIiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjI1NiIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMzUyMjU2IiBzaXplPSI1MTIiIHNpemVfYXJyYXk9IjUxMiIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iMjU2IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIzNTI3NjgiIHNpemU9IjUxMiIgc2l6ZV9hcnJheT0iNTEyIiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSIyNTYiIC8+DQoJCQk8L21pcF9tYXBzPg0KCQk8L2RhdGE+DQoJCTxwYWRkaW5nPjAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMDwvcGFkZGluZz4NCgk8L3NpemVfaW5mbz4NCjwvVGV4SGVhZGVyPg==').decode(
					'utf-8')
				write_file(os.path.join(folder, mat_name + ".pNormalTexture.tex"), texture_data, True)
	else:  # JURASSIC_WORLD_2 and JURASSIC_WORLD
		if type(data['_NM']) is list:
			# print('ADD NORMAL AS COLOURS ONLY\n')
			pass
		else:
			size = textures_find_size([data['_NM']])
			print('pNormalSize = ' + str(size[0]) + " " + str(size[0]))
			texture_save_or_generate(data['_NM'], folder, mat_name + '.pNormalTexture_RGB.png', size)
			# DdsType.BC7_UNORM
			if size[0] > 0:
				texture_data = base64.b64decode(
					'PFRleEhlYWRlciBjb21wcmVzc2lvbl90eXBlPSJEZHNUeXBlLkJDN19VTk9STSIgb25lXzA9IjAiIHN0cmVhbV9jb3VudD0iMiIgc3RyZWFtX2NvdW50X3JlcGVhdD0iMiIgZ2FtZT0iR2FtZXMuUExBTkVUX1pPTyI+DQoJPGJ1ZmZlcl9pbmZvcyBwb29sX3R5cGU9IjMiPg0KCQk8dGV4YnVmZmVyIG9mZnNldD0iMCIgc2l6ZT0iMzI3NjgwIiBmaXJzdF9taXA9IjAiIG1pcF9jb3VudD0iMiIgLz4NCgkJPHRleGJ1ZmZlciBvZmZzZXQ9IjMyNzY4MCIgc2l6ZT0iMjU2MDAiIGZpcnN0X21pcD0iMiIgbWlwX2NvdW50PSI4IiAvPg0KCTwvYnVmZmVyX2luZm9zPg0KCTxzaXplX2luZm8gcG9vbF90eXBlPSI0Ij4NCgkJPGRhdGEgZGF0YV9zaXplPSIzNTMyODAiIHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiBudW1fbWlwcz0iMTAiPg0KCQkJPG1pcF9tYXBzPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIwIiBzaXplPSIyNjIxNDQiIHNpemVfYXJyYXk9IjI2MjE0NCIgc2l6ZV9zY2FuPSIyMDQ4IiBzaXplX2RhdGE9IjI2MjE0NCIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMjYyMTQ0IiBzaXplPSI2NTUzNiIgc2l6ZV9hcnJheT0iNjU1MzYiIHNpemVfc2Nhbj0iMTAyNCIgc2l6ZV9kYXRhPSI2NTUzNiIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMzI3NjgwIiBzaXplPSIxNjM4NCIgc2l6ZV9hcnJheT0iMTYzODQiIHNpemVfc2Nhbj0iNTEyIiBzaXplX2RhdGE9IjE2Mzg0IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIzNDQwNjQiIHNpemU9IjQwOTYiIHNpemVfYXJyYXk9IjQwOTYiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjQwOTYiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjM0ODE2MCIgc2l6ZT0iMjA0OCIgc2l6ZV9hcnJheT0iMjA0OCIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iMjA0OCIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMzUwMjA4IiBzaXplPSIxMDI0IiBzaXplX2FycmF5PSIxMDI0IiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSIxMDI0IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIzNTEyMzIiIHNpemU9IjUxMiIgc2l6ZV9hcnJheT0iNTEyIiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSI1MTIiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjM1MTc0NCIgc2l6ZT0iNTEyIiBzaXplX2FycmF5PSI1MTIiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjI1NiIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMzUyMjU2IiBzaXplPSI1MTIiIHNpemVfYXJyYXk9IjUxMiIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iMjU2IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIzNTI3NjgiIHNpemU9IjUxMiIgc2l6ZV9hcnJheT0iNTEyIiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSIyNTYiIC8+DQoJCQk8L21pcF9tYXBzPg0KCQk8L2RhdGE+DQoJCTxwYWRkaW5nPjAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMDwvcGFkZGluZz4NCgk8L3NpemVfaW5mbz4NCjwvVGV4SGVhZGVyPg==').decode(
					'utf-8')
				write_file(os.path.join(folder, mat_name + ".pNormalTexture.tex"), texture_data, True)

	# pAOTexture
	if mod_game == 'PLANET_ZOO' or mod_game == 'PLANET_COASTER':
		if type(data['_AO']) is list:
			# print('ADD NORMAL AS COLOURS ONLY\n')
			pass
		else:
			size = textures_find_size([data['_AO']])
			print('pAOSize = ' + str(size[0]) + " " + str(size[0]))
			texture_save_or_generate(data['_AO'], folder, mat_name + '.pAOTexture.png', size)
			# DdsType.BC4_UNORM
			if size[0] > 0:
				texture_data = base64.b64decode(
					'PFRleEhlYWRlciBjb21wcmVzc2lvbl90eXBlPSJEZHNUeXBlLkJDNF9VTk9STSIgb25lXzA9IjAiIHN0cmVhbV9jb3VudD0iMiIgc3RyZWFtX2NvdW50X3JlcGVhdD0iMiIgZ2FtZT0iR2FtZXMuUExBTkVUX1pPTyI+DQoJPGJ1ZmZlcl9pbmZvcyBwb29sX3R5cGU9IjMiPg0KCQk8dGV4YnVmZmVyIG9mZnNldD0iMCIgc2l6ZT0iMTYzODQwIiBmaXJzdF9taXA9IjAiIG1pcF9jb3VudD0iMiIgLz4NCgkJPHRleGJ1ZmZlciBvZmZzZXQ9IjE2Mzg0MCIgc2l6ZT0iMTc0MDgiIGZpcnN0X21pcD0iMiIgbWlwX2NvdW50PSI4IiAvPg0KCTwvYnVmZmVyX2luZm9zPg0KCTxzaXplX2luZm8gcG9vbF90eXBlPSI0Ij4NCgkJPGRhdGEgZGF0YV9zaXplPSIxODEyNDgiIHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiBudW1fbWlwcz0iMTAiPg0KCQkJPG1pcF9tYXBzPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIwIiBzaXplPSIxMzEwNzIiIHNpemVfYXJyYXk9IjEzMTA3MiIgc2l6ZV9zY2FuPSIxMDI0IiBzaXplX2RhdGE9IjEzMTA3MiIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMTMxMDcyIiBzaXplPSIzMjc2OCIgc2l6ZV9hcnJheT0iMzI3NjgiIHNpemVfc2Nhbj0iNTEyIiBzaXplX2RhdGE9IjMyNzY4IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIxNjM4NDAiIHNpemU9IjgxOTIiIHNpemVfYXJyYXk9IjgxOTIiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjgxOTIiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjE3MjAzMiIgc2l6ZT0iNDA5NiIgc2l6ZV9hcnJheT0iNDA5NiIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iNDA5NiIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMTc2MTI4IiBzaXplPSIyMDQ4IiBzaXplX2FycmF5PSIyMDQ4IiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSIyMDQ4IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIxNzgxNzYiIHNpemU9IjEwMjQiIHNpemVfYXJyYXk9IjEwMjQiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjEwMjQiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjE3OTIwMCIgc2l6ZT0iNTEyIiBzaXplX2FycmF5PSI1MTIiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjUxMiIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMTc5NzEyIiBzaXplPSI1MTIiIHNpemVfYXJyYXk9IjUxMiIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iMjU2IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIxODAyMjQiIHNpemU9IjUxMiIgc2l6ZV9hcnJheT0iNTEyIiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSIyNTYiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjE4MDczNiIgc2l6ZT0iNTEyIiBzaXplX2FycmF5PSI1MTIiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjI1NiIgLz4NCgkJCTwvbWlwX21hcHM+DQoJCTwvZGF0YT4NCgkJPHBhZGRpbmc+MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwPC9wYWRkaW5nPg0KCTwvc2l6ZV9pbmZvPg0KPC9UZXhIZWFkZXI+').decode(
					'utf-8')
				write_file(os.path.join(folder, mat_name + ".pAOTexture.tex"), texture_data, True)
	else:
		# NOTE, THIS REQUIRES WE ARE SAVING NORMAL MAP FOR JWE2
		if type(data['_AO']) is list:
			# print('ADD NORMAL AS COLOURS ONLY\n')
			pass
		else:
			size = textures_find_size([data['_AO']])
			print('pAOSize = ' + str(size[0]) + " " + str(size[0]))
			texture_save_or_generate(data['_AO'], folder, mat_name + '.pNormalTexture_A.png', size)

		# pEmissiveTexture
	if type(data['_EM']) is list or type(data['_EM']) == None:
		# print('ADD NORMAL AS COLOURS ONLY\n')
		pass
	else:
		size = textures_find_size([data['_EM']])
		print('pEmissiveSize = ' + str(size[0]) + " " + str(size[0]))
		texture_save_or_generate(data['_EM'], folder, mat_name + '.pEmissiveTexture.png', size)
		# DdsType.BC7_UNORM_SRGB
		if size[0] > 0:
			texture_data = base64.b64decode(
				'PFRleEhlYWRlciBjb21wcmVzc2lvbl90eXBlPSJEZHNUeXBlLkJDN19VTk9STV9TUkdCIiBvbmVfMD0iMCIgc3RyZWFtX2NvdW50PSIyIiBzdHJlYW1fY291bnRfcmVwZWF0PSIyIiBnYW1lPSJHYW1lcy5QTEFORVRfWk9PIj4NCgk8YnVmZmVyX2luZm9zIHBvb2xfdHlwZT0iMyI+DQoJCTx0ZXhidWZmZXIgb2Zmc2V0PSIwIiBzaXplPSIzMjc2OCIgZmlyc3RfbWlwPSIwIiBtaXBfY291bnQ9IjEiIC8+DQoJCTx0ZXhidWZmZXIgb2Zmc2V0PSIzMjc2OCIgc2l6ZT0iMTM4MjQiIGZpcnN0X21pcD0iMSIgbWlwX2NvdW50PSI4IiAvPg0KCTwvYnVmZmVyX2luZm9zPg0KCTxzaXplX2luZm8gcG9vbF90eXBlPSI0Ij4NCgkJPGRhdGEgZGF0YV9zaXplPSI0NjU5MiIgd2lkdGg9IjI1NiIgaGVpZ2h0PSIxMjgiIG51bV9taXBzPSI5Ij4NCgkJCTxtaXBfbWFwcz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMCIgc2l6ZT0iMzI3NjgiIHNpemVfYXJyYXk9IjMyNzY4IiBzaXplX3NjYW49IjEwMjQiIHNpemVfZGF0YT0iMzI3NjgiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjMyNzY4IiBzaXplPSI4MTkyIiBzaXplX2FycmF5PSI4MTkyIiBzaXplX3NjYW49IjUxMiIgc2l6ZV9kYXRhPSI4MTkyIiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSI0MDk2MCIgc2l6ZT0iMjA0OCIgc2l6ZV9hcnJheT0iMjA0OCIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iMjA0OCIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iNDMwMDgiIHNpemU9IjEwMjQiIHNpemVfYXJyYXk9IjEwMjQiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjEwMjQiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjQ0MDMyIiBzaXplPSI1MTIiIHNpemVfYXJyYXk9IjUxMiIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iNTEyIiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSI0NDU0NCIgc2l6ZT0iNTEyIiBzaXplX2FycmF5PSI1MTIiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjI1NiIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iNDUwNTYiIHNpemU9IjUxMiIgc2l6ZV9hcnJheT0iNTEyIiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSIyNTYiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjQ1NTY4IiBzaXplPSI1MTIiIHNpemVfYXJyYXk9IjUxMiIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iMjU2IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSI0NjA4MCIgc2l6ZT0iNTEyIiBzaXplX2FycmF5PSI1MTIiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjI1NiIgLz4NCgkJCTwvbWlwX21hcHM+DQoJCTwvZGF0YT4NCgkJPHBhZGRpbmc+MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMDwvcGFkZGluZz4NCgk8L3NpemVfaW5mbz4NCjwvVGV4SGVhZGVyPg==').decode(
				'utf-8')
			write_file(os.path.join(folder, mat_name + ".pEmissiveTexture.tex"), texture_data, True)

	# pFlexicolourMasksTexture
	if type(data['_F1']) is list and type(data['_F2']) is list and type(data['_F3']) is list and type(
			data['_F4']) is list:
		# print('ADD NORMAL AS COLOURS ONLY\n')
		pass
	else:
		size = textures_find_size([data['_F1'], data['_F2'], data['_F3'], data['_F4']])
		print('pFlexicolourMasksTextureSize = ' + str(size[0]) + " " + str(size[0]))
		texture_save_or_generate(data['_F1'], folder, mat_name + '.pFlexicolourMasksTexture_R.png', size)
		texture_save_or_generate(data['_F2'], folder, mat_name + '.pFlexicolourMasksTexture_G.png', size)
		texture_save_or_generate(data['_F3'], folder, mat_name + '.pFlexicolourMasksTexture_B.png', size)
		texture_save_or_generate(data['_F4'], folder, mat_name + '.pFlexicolourMasksTexture_A.png', size)
		# DdsType.BC7_UNORM
		if size[0] > 0:
			texture_data = base64.b64decode(
				'PFRleEhlYWRlciBjb21wcmVzc2lvbl90eXBlPSJEZHNUeXBlLkJDN19VTk9STSIgb25lXzA9IjAiIHN0cmVhbV9jb3VudD0iMiIgc3RyZWFtX2NvdW50X3JlcGVhdD0iMiIgZ2FtZT0iR2FtZXMuUExBTkVUX1pPTyI+DQoJPGJ1ZmZlcl9pbmZvcyBwb29sX3R5cGU9IjMiPg0KCQk8dGV4YnVmZmVyIG9mZnNldD0iMCIgc2l6ZT0iMzI3NjgwIiBmaXJzdF9taXA9IjAiIG1pcF9jb3VudD0iMiIgLz4NCgkJPHRleGJ1ZmZlciBvZmZzZXQ9IjMyNzY4MCIgc2l6ZT0iMjU2MDAiIGZpcnN0X21pcD0iMiIgbWlwX2NvdW50PSI4IiAvPg0KCTwvYnVmZmVyX2luZm9zPg0KCTxzaXplX2luZm8gcG9vbF90eXBlPSI0Ij4NCgkJPGRhdGEgZGF0YV9zaXplPSIzNTMyODAiIHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiBudW1fbWlwcz0iMTAiPg0KCQkJPG1pcF9tYXBzPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIwIiBzaXplPSIyNjIxNDQiIHNpemVfYXJyYXk9IjI2MjE0NCIgc2l6ZV9zY2FuPSIyMDQ4IiBzaXplX2RhdGE9IjI2MjE0NCIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMjYyMTQ0IiBzaXplPSI2NTUzNiIgc2l6ZV9hcnJheT0iNjU1MzYiIHNpemVfc2Nhbj0iMTAyNCIgc2l6ZV9kYXRhPSI2NTUzNiIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMzI3NjgwIiBzaXplPSIxNjM4NCIgc2l6ZV9hcnJheT0iMTYzODQiIHNpemVfc2Nhbj0iNTEyIiBzaXplX2RhdGE9IjE2Mzg0IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIzNDQwNjQiIHNpemU9IjQwOTYiIHNpemVfYXJyYXk9IjQwOTYiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjQwOTYiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjM0ODE2MCIgc2l6ZT0iMjA0OCIgc2l6ZV9hcnJheT0iMjA0OCIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iMjA0OCIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMzUwMjA4IiBzaXplPSIxMDI0IiBzaXplX2FycmF5PSIxMDI0IiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSIxMDI0IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIzNTEyMzIiIHNpemU9IjUxMiIgc2l6ZV9hcnJheT0iNTEyIiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSI1MTIiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjM1MTc0NCIgc2l6ZT0iNTEyIiBzaXplX2FycmF5PSI1MTIiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjI1NiIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMzUyMjU2IiBzaXplPSI1MTIiIHNpemVfYXJyYXk9IjUxMiIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iMjU2IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIzNTI3NjgiIHNpemU9IjUxMiIgc2l6ZV9hcnJheT0iNTEyIiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSIyNTYiIC8+DQoJCQk8L21pcF9tYXBzPg0KCQk8L2RhdGE+DQoJCTxwYWRkaW5nPjAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMDwvcGFkZGluZz4NCgk8L3NpemVfaW5mbz4NCjwvVGV4SGVhZGVyPg==').decode(
				'utf-8')
			write_file(os.path.join(folder, mat_name + ".pFlexicolourMasksTexture.tex"), texture_data, True)

	# pRoughnessPackedTexture
	if type(data['_MT']) is list and type(data['_SP']) is list and type(data['_RN']) is list and type(
			data['_FO']) is list:
		# print('ADD NORMAL AS COLOURS ONLY\n')
		pass
	else:
		size = textures_find_size([data['_MT'], data['_SP'], data['_RN'], data['_FO']])
		print('pRoughnessPackedTextureSize = ' + str(size[0]) + " " + str(size[0]))
		texture_save_or_generate(data['_MT'], folder, mat_name + '.pRoughnessPackedTexture_R.png', size)
		texture_save_or_generate(data['_SP'], folder, mat_name + '.pRoughnessPackedTexture_G.png', size)
		texture_save_or_generate(data['_RN'], folder, mat_name + '.pRoughnessPackedTexture_B.png', size)
		texture_save_or_generate(data['_FO'], folder, mat_name + '.pRoughnessPackedTexture_A.png', size)
		# DdsType.BC7_UNORM
		if size[0] > 0:
			texture_data = base64.b64decode(
				'PFRleEhlYWRlciBjb21wcmVzc2lvbl90eXBlPSJEZHNUeXBlLkJDN19VTk9STSIgb25lXzA9IjAiIHN0cmVhbV9jb3VudD0iMiIgc3RyZWFtX2NvdW50X3JlcGVhdD0iMiIgZ2FtZT0iR2FtZXMuUExBTkVUX1pPTyI+DQoJPGJ1ZmZlcl9pbmZvcyBwb29sX3R5cGU9IjMiPg0KCQk8dGV4YnVmZmVyIG9mZnNldD0iMCIgc2l6ZT0iMzI3NjgwIiBmaXJzdF9taXA9IjAiIG1pcF9jb3VudD0iMiIgLz4NCgkJPHRleGJ1ZmZlciBvZmZzZXQ9IjMyNzY4MCIgc2l6ZT0iMjU2MDAiIGZpcnN0X21pcD0iMiIgbWlwX2NvdW50PSI4IiAvPg0KCTwvYnVmZmVyX2luZm9zPg0KCTxzaXplX2luZm8gcG9vbF90eXBlPSI0Ij4NCgkJPGRhdGEgZGF0YV9zaXplPSIzNTMyODAiIHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiBudW1fbWlwcz0iMTAiPg0KCQkJPG1pcF9tYXBzPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIwIiBzaXplPSIyNjIxNDQiIHNpemVfYXJyYXk9IjI2MjE0NCIgc2l6ZV9zY2FuPSIyMDQ4IiBzaXplX2RhdGE9IjI2MjE0NCIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMjYyMTQ0IiBzaXplPSI2NTUzNiIgc2l6ZV9hcnJheT0iNjU1MzYiIHNpemVfc2Nhbj0iMTAyNCIgc2l6ZV9kYXRhPSI2NTUzNiIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMzI3NjgwIiBzaXplPSIxNjM4NCIgc2l6ZV9hcnJheT0iMTYzODQiIHNpemVfc2Nhbj0iNTEyIiBzaXplX2RhdGE9IjE2Mzg0IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIzNDQwNjQiIHNpemU9IjQwOTYiIHNpemVfYXJyYXk9IjQwOTYiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjQwOTYiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjM0ODE2MCIgc2l6ZT0iMjA0OCIgc2l6ZV9hcnJheT0iMjA0OCIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iMjA0OCIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMzUwMjA4IiBzaXplPSIxMDI0IiBzaXplX2FycmF5PSIxMDI0IiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSIxMDI0IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIzNTEyMzIiIHNpemU9IjUxMiIgc2l6ZV9hcnJheT0iNTEyIiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSI1MTIiIC8+DQoJCQkJPG1pcG1hcCBvZmZzZXQ9IjM1MTc0NCIgc2l6ZT0iNTEyIiBzaXplX2FycmF5PSI1MTIiIHNpemVfc2Nhbj0iMjU2IiBzaXplX2RhdGE9IjI1NiIgLz4NCgkJCQk8bWlwbWFwIG9mZnNldD0iMzUyMjU2IiBzaXplPSI1MTIiIHNpemVfYXJyYXk9IjUxMiIgc2l6ZV9zY2FuPSIyNTYiIHNpemVfZGF0YT0iMjU2IiAvPg0KCQkJCTxtaXBtYXAgb2Zmc2V0PSIzNTI3NjgiIHNpemU9IjUxMiIgc2l6ZV9hcnJheT0iNTEyIiBzaXplX3NjYW49IjI1NiIgc2l6ZV9kYXRhPSIyNTYiIC8+DQoJCQk8L21pcF9tYXBzPg0KCQk8L2RhdGE+DQoJCTxwYWRkaW5nPjAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMDwvcGFkZGluZz4NCgk8L3NpemVfaW5mbz4NCjwvVGV4SGVhZGVyPg==').decode(
				'utf-8')
			write_file(os.path.join(folder, mat_name + ".pRoughnessPackedTexture.tex"), texture_data, True)


def save(filepath=""):
	folder, mat_name = os.path.split(filepath)
	b_mat = bpy.context.active_object.active_material
	mat_name = b_mat.name
	mod_game = "Jurassic World Evolution 2"

	export_fgm_at(folder, mod_game, mat_name)
	return f"Finished FGM export",
