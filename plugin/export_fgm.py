import logging

import bpy
import math

import numpy as np
import os

from plugin.utils import texture_settings
from constants import ConstantsProvider
from generated.array import Array
from generated.formats.fgm.structs.AttribData import AttribData
from generated.formats.fgm.structs.AttribInfo import AttribInfo
from generated.formats.fgm.structs.FgmHeader import FgmHeader
from generated.formats.fgm.structs.TexIndex import TexIndex
from generated.formats.fgm.structs.TextureData import TextureData
from generated.formats.fgm.structs.TextureInfo import TextureInfo
from generated.formats.fgm.enums.FgmDtype import FgmDtype
from generated.formats.ms2 import Ms2Version, get_game, Ms2Context
from generated.formats.ovl import set_game, games
from generated.formats.ovl_base import OvlContext
from generated.formats.tex.structs.SizeInfo import SizeInfo
from generated.formats.tex.structs.TexHeader import TexHeader
from plugin.utils.texture_settings import tex_slots


def get_object_names(col):
	obj_names = [o.name for o in bpy.data.collections[col.name].objects if
				 '_Hitcheck' not in o.name and o.hide_render == False]
	return obj_names


def get_object_material_names(ob):
	mats = []
	if ob.type == "MESH":
		for mat_slot in ob.material_slots:
			if mat_slot.material:
				b_mat = mat_slot.material
				mats.append(b_mat.name)
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
		b_mat = bpy.data.materials[mat_name]
		if b_mat.users > 1:
			materials.append(mat_name)
	return materials


def export_textures(b_mat, folder, mat_name, fgm_root, game, shader_name, constants):
	# populate colours from main shader
	main_shader = b_mat.node_tree.nodes.get("MainShader")
	inv_tex_slots = {v: k for k, v in tex_slots.items()}
	defaults = {}

	if not main_shader:
		return
		
	for socket in main_shader.inputs:
		long_name = socket.name
		# determine type of input from name
		if long_name.startswith("p"):
			defaults[long_name] = socket.default_value
		else:
			try:
				identifier = inv_tex_slots[long_name]
			except KeyError:
				logging.warning(f"Found no identifier for '{long_name}'")
				continue
			defaults[identifier] = socket.default_value
	# populate material textures, first from texture node labels
	texture_info = {x.label: x.image for x in b_mat.node_tree.nodes if x.type == 'TEX_IMAGE' and x.label}
	# now add color inputs and fallback defaults
	for slot, slot_desc in texture_settings.tex_slots.items():
		if slot not in texture_info:
			texture_info[slot] = defaults.get(slot, None)

	tex_channel_map = texture_settings.get_tex_channel_map(constants, game, shader_name)
	# export each texture
	for tex_name, tex_channels in tex_channel_map.items():
		tex = TextureInfo(fgm_root.context)
		tex.name = tex_name
		dep = TextureData(fgm_root.context, arg=tex)

		# purpose might be empty if channel appears to be unused, skip those
		raw_entries = [texture_info[purpose] for purpose in tex_channels.values() if purpose]
		print(tex_name, raw_entries)
		# does this texture export as an image or RGBA?
		if any(isinstance(k, bpy.types.Image) for k in raw_entries):
			# texture needs to be used or generated
			tex.dtype = FgmDtype.TEXTURE
			tex.reset_field("value")
			tex_index = TexIndex(fgm_root.context)
			tex.value[:] = [tex_index]
			dep.dependency_name.data = f'{mat_name}.{tex_name}.tex'
			size = textures_find_size(raw_entries)
			logging.debug(f"size: {size}")
			for channel, purpose in tex_channels.items():
				channel_suffix = f"_{channel}" if channel else ""
				png_name = f'{mat_name}.{tex_name}{channel_suffix}.png'
				try:
					texture_save_or_generate(texture_info[purpose], folder, png_name, size)
				except:
					logging.exception(f"Saving {png_name} failed")
			tex_path = os.path.join(folder, f'{mat_name}.{tex_name}.tex')
			# pick suitable DDS compression
			comp = "BC7_UNORM"
			if tex_name == "pNormalTexture" and len(tex_channels) == 1:
				comp = "BC5_UNORM"
			tex_file = TexHeader(tex.context)
			# pick reasonable stream count
			tex_file.stream_count = 1
			tex_file.size_info.data = SizeInfo(tex_file.context)
			size_info = tex_file.size_info.data.data
			# pick empty MIP setting so that they are filled by the plugin
			size_info.num_mips = 0
			# pick the member of the correct DdsType enum for PC vs later games
			tex_file.compression_type = type(tex_file.compression_type)[comp]
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


def export_attributes(b_mat, folder, mat_name, fgm_root, game, shader_name, constants):
	try:
		textures, attrib_dic = constants[game]["shaders"][shader_name]
	except:
		logging.warning(f"No attributes for shader '{shader_name}' in game {game}")
		raise
	for att_name, attr_data in attrib_dic.items():
		att = AttribInfo(fgm_root.context)
		att.dtype = FgmDtype.from_value(attr_data[0])
		att.name = att_name

		data = AttribData(fgm_root.context, arg=att)
		# get data from blender when set
		b_val = getattr(b_mat.fgm, att_name, None)
		if b_val:
			default = b_val
		else:
			# Assign default value from attributes dict
			default = attr_data[1][0][0]
		data.value = np.array(default, data.value.dtype)
		fgm_root.attributes.data.append(att)
		fgm_root.value_foreach_attributes.data.append(data)


def export_fgm_at(folder, game, mat_name):
	fgm_path = os.path.join(folder, mat_name + ".fgm")
	logging.info(f"Exporting Material: {fgm_path}")
	b_mat = bpy.data.materials[mat_name]

	# ignore saving for materials linked from a library, we might not have all the data available.
	# TODO: Alternatively, retrieve the missing information from the asset library
	if b_mat.asset_data and b_mat['AssetPackageName']:
		logging.info(f"Material {mat_name} belongs to library: {str(b_mat.library)}, exporting aborted")
		return

	logging.debug(f"Shader type: {b_mat.blend_method}")
	logging.debug(f"Material textures: {[x.image.name for x in b_mat.node_tree.nodes if x.type == 'TEX_IMAGE']}")
	# populate material textures
	context = OvlContext()
	set_game(context, game)
	# export the curve data
	fgm_root = FgmHeader(context)
	fgm_root.textures.data = Array(context, 0, None, (0,), fgm_root.textures.template)
	fgm_root.attributes.data = Array(context, 0, None, (0,), fgm_root.attributes.template)
	fgm_root.name_foreach_textures.data = Array(context, fgm_root.textures, None, (0,), fgm_root.name_foreach_textures.template)
	fgm_root.value_foreach_attributes.data = Array(context, fgm_root.attributes, None, (0,), fgm_root.value_foreach_attributes.template)

	# get shader from b_mat
	fgm_root.shader_name = b_mat.fgm.shader_name
	constants = ConstantsProvider(("shaders", "textures", "texchannels"))
	logging.info(f"Shader: {fgm_root.shader_name}")
	export_textures(b_mat, folder, mat_name, fgm_root, game, fgm_root.shader_name, constants)
	export_attributes(b_mat, folder, mat_name, fgm_root, game, fgm_root.shader_name, constants)

	with FgmHeader.to_xml_file(fgm_root, fgm_path) as xml_root:
		pass


def textures_find_size(data):
	size = [0, 0]
	for tex in data:
		if isinstance(tex, bpy.types.Image):
			tex_size = list(tex.size)
			if size[0] == 0:
				size = tex_size
			elif size != tex_size:
				raise TypeError(f"{tex.name} size mismatch {size} vs {tex_size}")
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
	if isinstance(data, bpy.types.Image):
		# Colour input from another image
		img = data
		old_format = img.file_format
		img.file_format = 'PNG'
		img.save(filepath=os.path.join(base_path, file_name), quality=100)
		img.file_format = old_format
	else:
		if len(data) == 4:
			# Colour input as RGBA
			img = image_new(file_name, size[0], size[1], *data)
		elif len(data) == 3:
			# Colour input as RGB
			img = image_new(file_name, size[0], size[1], *data, 255)
		else:
			# Colour input as a single float value
			img = image_new(file_name, size[0], size[1], data[0], data[0], data[0], 255)
		img.file_format = 'PNG'
		img.save(filepath=os.path.join(base_path, file_name), quality=100)
		bpy.data.images.remove(img)


def save(reporter, filepath=""):
	folder, mat_name = os.path.split(filepath)
	mat_name, ext = os.path.splitext(mat_name)
	# get game from GUI dropdown
	game = bpy.context.scene.cobra.game
	export_fgm_at(folder, game, mat_name)
	reporter.show_info(f"Exported {mat_name}")
