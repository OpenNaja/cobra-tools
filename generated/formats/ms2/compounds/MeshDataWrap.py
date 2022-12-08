from generated.formats.ms2.compounds.BioMeshData import BioMeshData
from generated.formats.ms2.compounds.NewMeshData import NewMeshData
from generated.formats.ms2.compounds.PcMeshData import PcMeshData
from generated.formats.ms2.compounds.ZtMeshData import ZtMeshData
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class MeshDataWrap(MemStruct):

	__name__ = 'MeshDataWrap'

	_import_key = 'ms2.compounds.MeshDataWrap'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.mesh = ZtMeshData(self.context, 0, None)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('mesh', BioMeshData, (0, None), (False, None), True),
		('mesh', NewMeshData, (0, None), (False, None), True),
		('mesh', PcMeshData, (0, None), (False, None), True),
		('mesh', ZtMeshData, (0, None), (False, None), True),
		('mesh', ZtMeshData, (0, None), (False, None), True),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version >= 47 and ((instance.context.version == 51) or (instance.context.version == 52)) and instance.context.biosyn:
			yield 'mesh', BioMeshData, (0, None), (False, None)
		if instance.context.version >= 47 and not (((instance.context.version == 51) or (instance.context.version == 52)) and instance.context.biosyn):
			yield 'mesh', NewMeshData, (0, None), (False, None)
		if instance.context.version == 32:
			yield 'mesh', PcMeshData, (0, None), (False, None)
		if instance.context.version == 13:
			yield 'mesh', ZtMeshData, (0, None), (False, None)
		if instance.context.version == 7:
			yield 'mesh', ZtMeshData, (0, None), (False, None)
