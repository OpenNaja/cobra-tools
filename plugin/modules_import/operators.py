import os
import bpy.utils.previews
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper

from plugin import import_banis, import_manis, import_matcol, import_fgm, import_ms2, import_spl, import_voxelskirt
from plugin.utils.blender_util import report_messages


class ImportOp(bpy.types.Operator, ImportHelper):
	bl_options = {'UNDO'}

	@property
	def kwargs(self) -> dict:
		return self.as_keywords(ignore=("axis_forward", "axis_up", "filter_glob"))


class ImportBanis(ImportOp):
	"""Import from Cobra baked animations file format (.banis)"""
	bl_idname = "import_scene.cobra_banis"
	bl_label = 'Import Banis'
	filename_ext = ".banis"
	filter_glob: StringProperty(default="*.banis", options={'HIDDEN'})
	files: CollectionProperty(type=bpy.types.PropertyGroup)

	# set_fps = BoolProperty(name="Adjust FPS", description="Set the scene to FPS used by BANI", default=True)

	def execute(self, context):
		return report_messages(self, import_banis.load, **self.kwargs)


class ImportManis(ImportOp):
	"""Import from Cobra animations file format (.manis)"""
	bl_idname = "import_scene.cobra_manis"
	bl_label = 'Import Manis'
	filename_ext = ".manis"
	filter_glob: StringProperty(default="*.manis", options={'HIDDEN'})
	files: CollectionProperty(type=bpy.types.PropertyGroup)
	disable_ik: BoolProperty(name="Disable IK", description="Disable IK constraints on armature to enable jitter-free playback of baked animations", default=True)
	# set_fps: BoolProperty(name="Adjust FPS", description="Set the scene to FPS used by BANI", default=True)

	def execute(self, context):
		return report_messages(self, import_manis.load, **self.kwargs)


class ImportMatcol(ImportOp):
	"""Import from Matcol file format (.matcol, .dinosaurmateriallayers)"""
	bl_idname = "import_scene.cobra_matcol"
	bl_label = 'Import Matcol'
	filename_ext = ".dinosaurmateriallayers"

	# filter_glob: StringProperty(default="*.matcol", options={'HIDDEN'})
	# filter_glob: StringProperty(default="*.matcol;*.materialcollection;*.dinosaurmateriallayers", options={'HIDDEN'})

	def execute(self, context):
		return report_messages(self, import_matcol.load, **self.kwargs)


# ref: https://stackoverflow.com/questions/63299327/importing-multiple-files-in-blender-import-plugin
class ImportFgm(ImportOp):
	"""Import from Fgm file format (.fgm), allows importing multiple files"""
	bl_idname = "import_scene.cobra_fgms"  
	bl_label = "Import Fgm(s)"

	# ImportHelper mixin class uses this
	filename_ext = ".fgm"

	filter_glob: StringProperty(
		default="*.fgm",
		options={'HIDDEN'},
		maxlen=255,  # Max internal buffer length, longer would be clamped.
	)

	# List of operator properties, the attributes will be assigned
	# to the class instance from the operator settings before calling.
	replace: BoolProperty(
		name="Replace existing materials",
		description="If a material exists in the scene, it will be replaced with this one",
		default=True,
	)

	# necessary to support multi-file import
	files: CollectionProperty(
		type=bpy.types.OperatorFileListElement,
		options={'HIDDEN', 'SKIP_SAVE'},
	)

	# necessary to support multi-file import
	directory: StringProperty(
		subtype='DIR_PATH',
	)

	def execute(self, context):
		error_count = 0
		for current_file in self.files:
			filepath = os.path.join(self.directory, current_file.name)
			result = report_messages(self, import_fgm.load, filepath, self.replace)
			if 'CANCELLED' in result:
				error_count += 1

		if len(self.files)>1:
			self.report({'INFO'}, f"Attempt to import {len(self.files)} materials, {error_count} errors found.")
			return {'FINISHED'}

		# return only material result
		return result


class ImportMS2(ImportOp):
	"""Import from MS2 file format (.MS2), multiple files allowed"""
	bl_idname = "import_scene.cobra_ms2"
	bl_label = 'Import MS2(s)'
	filename_ext = ".ms2"
	filter_glob: StringProperty(default="*.ms2", options={'HIDDEN'})

	# necessary to support multi-file import
	files: CollectionProperty(
		type=bpy.types.OperatorFileListElement,
		options={'HIDDEN', 'SKIP_SAVE'},
	)

	# necessary to support multi-file import
	directory: StringProperty(
		subtype='DIR_PATH',
	)

	use_custom_normals: BoolProperty(name="Use MS2 Normals",
									 description="Applies MS2 normals as custom normals to preserve the original shading. May crash on some meshes due to a blender bug",
									 default=False)
	mirror_mesh: BoolProperty(name="Mirror Meshes", description="Mirrors models. Careful, sometimes bones don't match",
							  default=False)

	#def execute(self, context):
	#	return report_messages(self, import_ms2.load, **self.kwargs)

	def execute(self, context):
		error_count = 0
		for current_file in self.files:
			filepath = os.path.join(self.directory, current_file.name)
			result = report_messages(self, import_ms2.load, filepath, self.use_custom_normals, self.mirror_mesh)
			if 'CANCELLED' in result:
				error_count += 1

		if len(self.files)>1:
			self.report({'INFO'}, f"Attempt to import {len(self.files)} MS2, {error_count} errors found.")
			return {'FINISHED'}

		# return only ms2 result
		return result


class ImportSPL(ImportOp):
	"""Import from spline file format (.spl), multiple files allowed"""
	bl_idname = "import_scene.cobra_spl"
	bl_label = 'Import SPL(s)'
	filename_ext = ".spl"
	filter_glob: StringProperty(default="*.spl", options={'HIDDEN'})

	# necessary to support multi-file import
	files: CollectionProperty(
		type=bpy.types.OperatorFileListElement,
		options={'HIDDEN', 'SKIP_SAVE'},
	)

	# necessary to support multi-file import
	directory: StringProperty(
		subtype='DIR_PATH',
	)

	def execute(self, context):
		error_count = 0
		for current_file in self.files:
			filepath = os.path.join(self.directory, current_file.name)
			result = report_messages(self, import_spl.load, filepath)
			if 'CANCELLED' in result:
				error_count += 1

		if len(self.files)>1:
			self.report({'INFO'}, f"Attempt to import {len(self.files)} SPL, {error_count} errors found.")
			return {'FINISHED'}

		# return only spline result
		return result


class ImportVoxelskirt(ImportOp):
	"""Import from Voxelskirt file format (.voxelskirt)"""
	bl_idname = "import_scene.cobra_voxelskirt"
	bl_label = 'Import Voxelskirt'
	filename_ext = ".voxelskirt"
	filter_glob: StringProperty(default="*.voxelskirt", options={'HIDDEN'})

	def execute(self, context):
		return report_messages(self, import_voxelskirt.load, **self.kwargs)


class ImportMS2FromBrowser(bpy.types.Operator):
	"""Imports ms2 content as new scenes from the file browser"""
	bl_idname = "ct_wm.import_ms2"
	bl_label = "Import ms2"

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		folder = context.space_data.params.directory.decode('ascii')
		file = context.space_data.params.filename
		filepath = os.path.join(folder, file).replace("\\", "/")
		print("Importing: " + filepath)
		report_messages(self, import_ms2.load, filepath=filepath)
		return {'FINISHED'}


class ImportFGMFromBrowser(bpy.types.Operator):
	"""Imports fgm as a new material from the file browser"""
	bl_idname = "ct_wm.import_fgm"
	bl_label = "Import fgm"

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		folder = context.space_data.params.directory.decode('ascii')
		file = context.space_data.params.filename
		filepath = os.path.join(folder, file).replace("\\", "/")
		print("Importing: " + filepath)
		report_messages(self, import_fgm.load, filepath=filepath)
		return {'FINISHED'}
