import logging

from generated.formats.ms2 import is_pz
from generated.formats.ms2.structs.MaterialName import MaterialName
from plugin.utils.blender_util import strip_duplicate_suffix
from plugin.utils.object import get_property
from plugin.utils.shell import is_fin_mat, is_shell_mat


def export_material(model_info, b_mat, reporter):
	mat = MaterialName(model_info.context)
	try:
		# use some_index from existing meshes
		mat.blend_mode = get_property(b_mat, "some_index")
	except KeyError:
		mat.blend_mode = get_property(b_mat, "blend_mode", default=get_blend_mode(b_mat, model_info))
	mat.name = strip_duplicate_suffix(b_mat.name, "Material", reporter)
	model_info.model.materials.append(mat)


def get_blend_mode(b_mat, model_info):
	logging.info(f"Determining blend mode for {b_mat.name}")
	if is_fin_mat(b_mat):
		return 7
	elif is_shell_mat(b_mat):
		if is_pz(model_info.context):
			return 263
		else:
			return 6
	return 0
