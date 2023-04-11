from generated.formats.ms2.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class MeshDataWrap(MemStruct):

	__name__ = 'MeshDataWrap'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.mesh = name_type_map['ZtMeshData'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'mesh', name_type_map['BioMeshData'], (0, None), (False, None), (lambda context: context.version >= 47 and ((context.version == 51) or (context.version == 52)) and context.biosyn, None)
		yield 'mesh', name_type_map['NewMeshData'], (0, None), (False, None), (lambda context: context.version >= 47 and not (((context.version == 51) or (context.version == 52)) and context.biosyn), None)
		yield 'mesh', name_type_map['PcMeshData'], (0, None), (False, None), (lambda context: context.version == 32, None)
		yield 'mesh', name_type_map['ZtMeshData'], (0, None), (False, None), (lambda context: context.version == 13, None)
		yield 'mesh', name_type_map['ZtMeshData'], (0, None), (False, None), (lambda context: context.version == 7, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version >= 47 and ((instance.context.version == 51) or (instance.context.version == 52)) and instance.context.biosyn:
			yield 'mesh', name_type_map['BioMeshData'], (0, None), (False, None)
		if instance.context.version >= 47 and not (((instance.context.version == 51) or (instance.context.version == 52)) and instance.context.biosyn):
			yield 'mesh', name_type_map['NewMeshData'], (0, None), (False, None)
		if instance.context.version == 32:
			yield 'mesh', name_type_map['PcMeshData'], (0, None), (False, None)
		if instance.context.version == 13:
			yield 'mesh', name_type_map['ZtMeshData'], (0, None), (False, None)
		if instance.context.version == 7:
			yield 'mesh', name_type_map['ZtMeshData'], (0, None), (False, None)
