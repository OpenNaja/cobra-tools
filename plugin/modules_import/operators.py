import os
import bpy.utils.previews
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, EnumProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper

from plugin import import_banis, import_manis, import_matcol, import_fgm, import_ms2, import_spl, import_voxelskirt
from plugin.utils.matrix_util import report_messages


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


class ImportFgm(ImportOp):
	"""Import from Fgm file format (.fgm)"""
	bl_idname = "import_scene.cobra_fgm"
	bl_label = 'Import Fgm'
	filename_ext = ".fgm"
	filter_glob: StringProperty(default="*.fgm", options={'HIDDEN'})

	def execute(self, context):
		return report_messages(self, import_fgm.load, **self.kwargs)


class ImportMS2(ImportOp):
	"""Import from MS2 file format (.MS2)"""
	bl_idname = "import_scene.cobra_ms2"
	bl_label = 'Import MS2'
	filename_ext = ".ms2"
	filter_glob: StringProperty(default="*.ms2", options={'HIDDEN'})
	use_custom_normals: BoolProperty(name="Use MS2 Normals",
									 description="Applies MS2 normals as custom normals to preserve the original shading. May crash on some meshes due to a blender bug",
									 default=False)
	mirror_mesh: BoolProperty(name="Mirror Meshes", description="Mirrors models. Careful, sometimes bones don't match",
							  default=False)

	def execute(self, context):
		return report_messages(self, import_ms2.load, **self.kwargs)


class ImportSPL(ImportOp):
	"""Import from spline file format (.spl)"""
	bl_idname = "import_scene.cobra_spl"
	bl_label = 'Import SPL'
	filename_ext = ".spl"
	filter_glob: StringProperty(default="*.spl", options={'HIDDEN'})

	def execute(self, context):
		return report_messages(self, import_spl.load, **self.kwargs)


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
