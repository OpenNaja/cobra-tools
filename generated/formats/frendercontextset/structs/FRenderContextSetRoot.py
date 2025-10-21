from generated.formats.frendercontextset.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class FRenderContextSetRoot(MemStruct):

	__name__ = 'FRenderContextSetRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ptr_1_count = name_type_map['Uint64'](self.context, 0, None)
		self.render_layers_count = name_type_map['Uint64'](self.context, 0, None)
		self.render_features_count = name_type_map['Uint64'](self.context, 0, None)
		self.ptr_1_list = name_type_map['ArrayPointer'](self.context, self.ptr_1_count, name_type_map['ContextSet1Item'])
		self.render_layers = name_type_map['ArrayPointer'](self.context, self.render_layers_count, name_type_map['RenderLayer'])
		self.render_features = name_type_map['ArrayPointer'](self.context, self.render_features_count, name_type_map['RenderFeature'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ptr_1_list', name_type_map['ArrayPointer'], (None, name_type_map['ContextSet1Item']), (False, None), (None, None)
		yield 'ptr_1_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'render_layers', name_type_map['ArrayPointer'], (None, name_type_map['RenderLayer']), (False, None), (None, None)
		yield 'render_layers_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'render_features', name_type_map['ArrayPointer'], (None, name_type_map['RenderFeature']), (False, None), (None, None)
		yield 'render_features_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ptr_1_list', name_type_map['ArrayPointer'], (instance.ptr_1_count, name_type_map['ContextSet1Item']), (False, None)
		yield 'ptr_1_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'render_layers', name_type_map['ArrayPointer'], (instance.render_layers_count, name_type_map['RenderLayer']), (False, None)
		yield 'render_layers_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'render_features', name_type_map['ArrayPointer'], (instance.render_features_count, name_type_map['RenderFeature']), (False, None)
		yield 'render_features_count', name_type_map['Uint64'], (0, None), (False, None)
