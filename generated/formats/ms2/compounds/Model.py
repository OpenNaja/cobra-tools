from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.compounds.PadAlign import PadAlign
from generated.formats.ms2.compounds.DLAPreBones import DLAPreBones
from generated.formats.ms2.compounds.FloatsY import FloatsY
from generated.formats.ms2.compounds.LodInfo import LodInfo
from generated.formats.ms2.compounds.MaterialName import MaterialName
from generated.formats.ms2.compounds.MeshDataWrap import MeshDataWrap
from generated.formats.ms2.compounds.Object import Object
from generated.formats.ms2.compounds.ZTPreBones import ZTPreBones
from generated.formats.ovl_base.compounds.Empty import Empty


class Model(BaseStruct):

	__name__ = 'Model'

	_import_key = 'ms2.compounds.Model'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.start_ref = Empty(self.context, 0, None)

		# name pointers for each material
		self.materials = Array(self.context, 0, None, (0,), MaterialName)

		# lod info for each level, only present if models are present (despite the count sometimes saying otherwise!)
		self.lods = Array(self.context, 0, None, (0,), LodInfo)

		# instantiate the meshes with materials
		self.objects = Array(self.context, 0, None, (0,), Object)
		self.mesh_aligner = PadAlign(self.context, 8, self.start_ref)

		# mesh data blocks for this model
		self.meshes = Array(self.context, 0, None, (0,), MeshDataWrap)

		# ?
		self.pre_bones = DLAPreBones(self.context, 0, None)

		# see if it is a flag for ztuac too, so might be totally wrong here
		self.floatsy = Array(self.context, 0, None, (0,), FloatsY)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('start_ref', Empty, (0, None), (False, None), (None, None))
		yield ('materials', Array, (0, None, (None,), MaterialName), (False, None), (None, None))
		yield ('lods', Array, (0, None, (None,), LodInfo), (False, None), (None, None))
		yield ('objects', Array, (0, None, (None,), Object), (False, None), (None, None))
		yield ('mesh_aligner', PadAlign, (8, None), (False, None), (lambda context: context.version <= 32, None))
		yield ('meshes', Array, (0, None, (None,), MeshDataWrap), (False, None), (None, None))
		yield ('pre_bones', ZTPreBones, (0, None), (False, None), (lambda context: context.version == 13, True))
		yield ('pre_bones', DLAPreBones, (0, None), (False, None), (lambda context: context.version == 7, True))
		yield ('floatsy', Array, (0, None, (None,), FloatsY), (False, None), (lambda context: context.version <= 32, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'start_ref', Empty, (0, None), (False, None)
		yield 'materials', Array, (0, None, (instance.arg.num_materials,), MaterialName), (False, None)
		yield 'lods', Array, (0, None, (instance.arg.num_lods,), LodInfo), (False, None)
		yield 'objects', Array, (0, None, (instance.arg.num_objects,), Object), (False, None)
		if instance.context.version <= 32:
			yield 'mesh_aligner', PadAlign, (8, instance.start_ref), (False, None)
		yield 'meshes', Array, (0, None, (instance.arg.num_meshes,), MeshDataWrap), (False, None)
		if instance.context.version == 13 and instance.arg.last_count:
			yield 'pre_bones', ZTPreBones, (0, None), (False, None)
		if instance.context.version == 7 and instance.arg.last_count:
			yield 'pre_bones', DLAPreBones, (0, None), (False, None)
		if instance.context.version <= 32:
			yield 'floatsy', Array, (0, None, (instance.arg.render_flag,), FloatsY), (False, None)


Model.init_attributes()
