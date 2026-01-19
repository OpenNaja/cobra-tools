import os
import bpy.utils.previews
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper

from plugin import import_banis, import_manis, import_matcol, import_fgm, import_ms2, import_spl, import_voxelskirt
from plugin.utils.operators import BaseOp


class ImportOp(BaseOp, ImportHelper):

	def execute(self, context):
		return self.report_messages(self.target, filepath=self.filepath, **self.kwargs)


class BulkImportOp(ImportOp):
	# ref: https://stackoverflow.com/questions/63299327/importing-multiple-files-in-blender-import-plugin

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
		if self.files:
			for current_file in self.files:
				filepath = os.path.join(self.directory, current_file.name)
				result = self.report_messages(self.target, filepath=filepath, **self.kwargs)
				if 'CANCELLED' in result:
					error_count += 1
				self.report({'INFO'},
							f"Attempt to import {len(self.files)} {self.filename_ext}s, {error_count} errors found.")
		# return only material result
		return {'FINISHED'}


class ImportBanis(BulkImportOp):
	"""Import from Cobra baked animations file format (.banis)"""
	bl_idname = "import_scene.cobra_banis"
	bl_label = 'Import Banis'
	filename_ext = ".banis"
	filter_glob: StringProperty(default="*.banis", options={'HIDDEN'})
	files: CollectionProperty(type=bpy.types.PropertyGroup)
	# set_fps = BoolProperty(name="Adjust FPS", description="Set the scene to FPS used by BANI", default=True)
	target = import_banis.load


class ImportManis(BulkImportOp):
	"""Import from Cobra animations file format (.manis)"""
	bl_idname = "import_scene.cobra_manis"
	bl_label = 'Import Manis'
	filename_ext = ".manis"
	filter_glob: StringProperty(default="*.manis", options={'HIDDEN'})
	files: CollectionProperty(type=bpy.types.PropertyGroup)
	disable_ik: BoolProperty(name="Disable IK",
							 description="Disable IK constraints on armature to enable jitter-free playback of baked animations",
							 default=True)
	# set_fps: BoolProperty(name="Adjust FPS", description="Set the scene to FPS used by BANI", default=True)
	target = import_manis.load


class ImportMatcol(ImportOp):
	"""Import from Matcol file format (.matcol, .dinosaurmateriallayers)"""
	bl_idname = "import_scene.cobra_matcol"
	bl_label = 'Import Matcol'
	filename_ext = ".dinosaurmateriallayers"
	# filter_glob: StringProperty(default="*.matcol", options={'HIDDEN'})
	# filter_glob: StringProperty(default="*.matcol;*.materialcollection;*.dinosaurmateriallayers", options={'HIDDEN'})
	target = import_matcol.load


class ImportFgm(BulkImportOp):
	"""Import from Fgm file format (.fgm), allows importing multiple files"""
	bl_idname = "import_scene.cobra_fgm"
	bl_label = "Import Fgm(s)"
	filename_ext = ".fgm"
	target = import_fgm.load

	filter_glob: StringProperty(
		default="*.fgm",
		options={'HIDDEN'},
		maxlen=255,  # Max internal buffer length, longer would be clamped.
	)
	replace: BoolProperty(
		name="Replace existing materials",
		description="If a material exists in the scene, it will be replaced with this one",
		default=True,
	)


class ImportMS2(BulkImportOp):
	"""Import from MS2 file format (.MS2), multiple files allowed"""
	bl_idname = "import_scene.cobra_ms2"
	bl_label = 'Import MS2(s)'
	filename_ext = ".ms2"
	target = import_ms2.load
	filter_glob: StringProperty(default="*.ms2", options={'HIDDEN'})
	use_custom_normals: BoolProperty(
		name="Use MS2 Normals",
		description="Applies MS2 normals as custom normals to preserve the original shading. May crash on some meshes due to a blender bug",
		default=True)
	quadrify: BoolProperty(
		name="Quadrify Tris",
		description="Convert tris to quads for easier editing. May change edges in quads, so turn this off when a regular edge grid matters (some cases of hard surface modeling).",
		default=True)
	mirror_mesh: BoolProperty(
		name="Mirror Meshes",
		description="Mirrors models. Careful, sometimes bones don't match",
		default=False)
	merge_vertices: BoolProperty(
		name="Merge Vertices",
		description="Merge vertices without breaking custom normals data. Turn off for meshes with double sided geometry sharing vertices, and turn on backface culling in the material settings",
		default=True)
	load_libraries: BoolProperty(
		name="Load from Libraries",
		description="Check Blender's asset libraries for materials; may be very slow",
		default=False)


class ImportSPL(BulkImportOp):
	"""Import from spline file format (.spl), multiple files allowed"""
	bl_idname = "import_scene.cobra_spl"
	bl_label = 'Import SPL(s)'
	filename_ext = ".spl"
	target = import_spl.load
	filter_glob: StringProperty(default="*.spl", options={'HIDDEN'})


class ImportVoxelskirt(ImportOp):
	"""Import from Voxelskirt file format (.voxelskirt)"""
	bl_idname = "import_scene.cobra_voxelskirt"
	bl_label = 'Import Voxelskirt'
	filename_ext = ".voxelskirt"
	target = import_voxelskirt.load
	filter_glob: StringProperty(default="*.voxelskirt", options={'HIDDEN'})


class BrowserImportOp(ImportOp):

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	# @property
	def get_filepath(self, context) -> str:
		folder = context.space_data.params.directory.decode('ascii')
		file = context.space_data.params.filename
		filepath = os.path.join(folder, file).replace("\\", "/")
		print(f"Importing: {filepath}")
		return filepath

	def execute(self, context):
		return self.report_messages(self.target, filepath=self.get_filepath(context), **self.kwargs)


class ImportMS2FromBrowser(BrowserImportOp):
	"""Imports ms2 content as new scenes from the file browser"""
	bl_idname = "ct_wm.import_ms2"
	bl_label = "Import ms2"
	target = import_ms2.load


class ImportFGMFromBrowser(BrowserImportOp):
	"""Imports fgm as a new material from the file browser"""
	bl_idname = "ct_wm.import_fgm"
	bl_label = "Import fgm"
	target = import_fgm.load


if hasattr(bpy.types, 'FileHandler'):
	class MS2_FH_script_import(bpy.types.FileHandler):
		bl_idname = "MS2_FH_script_import"
		bl_label = "File handler for ms2 script node import"
		bl_import_operator = "import_scene.cobra_ms2"
		bl_file_extensions = ".ms2"

		@classmethod
		def poll_drop(cls, context):
			return context.area and context.area.type == 'VIEW_3D'


	class FGM_FH_script_import(bpy.types.FileHandler):
		bl_idname = "FGM_FH_script_import"
		bl_label = "File handler for fgm script node import"
		bl_import_operator = "import_scene.cobra_fgm"
		bl_file_extensions = ".fgm"

		@classmethod
		def poll_drop(cls, context):
			return (context.area and context.area.type == 'VIEW_3D') or (
						context.region and context.region.type == 'WINDOW'
						and context.area and context.area.ui_type == 'ShaderNodeTree'
						and context.object and context.object.type == 'MESH'
						and context.material)
