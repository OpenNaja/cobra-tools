from generated.formats.ms2.compounds.BioMeshData import BioMeshData
from generated.formats.ms2.compounds.NewMeshData import NewMeshData
from generated.formats.ms2.compounds.PcMeshData import PcMeshData
from generated.formats.ms2.compounds.ZtMeshData import ZtMeshData
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class MeshDataWrap(MemStruct):

	__name__ = 'MeshDataWrap'

	_import_path = 'generated.formats.ms2.compounds.MeshDataWrap'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.mesh = ZtMeshData(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		if self.context.version >= 47 and (self.context.version == 51) and self.context.biosyn:
			self.mesh = BioMeshData(self.context, 0, None)
		if self.context.version >= 47 and not ((self.context.version == 51) and self.context.biosyn):
			self.mesh = NewMeshData(self.context, 0, None)
		if self.context.version == 32:
			self.mesh = PcMeshData(self.context, 0, None)
		if self.context.version == 13:
			self.mesh = ZtMeshData(self.context, 0, None)
		if self.context.version == 7:
			self.mesh = ZtMeshData(self.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version >= 47 and (instance.context.version == 51) and instance.context.biosyn:
			yield 'mesh', BioMeshData, (0, None), (False, None)
		if instance.context.version >= 47 and not ((instance.context.version == 51) and instance.context.biosyn):
			yield 'mesh', NewMeshData, (0, None), (False, None)
		if instance.context.version == 32:
			yield 'mesh', PcMeshData, (0, None), (False, None)
		if instance.context.version == 13:
			yield 'mesh', ZtMeshData, (0, None), (False, None)
		if instance.context.version == 7:
			yield 'mesh', ZtMeshData, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'MeshDataWrap [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
