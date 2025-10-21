from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.physmat.imports import name_type_map


class PhysmatRoot(MemStruct):

	__name__ = 'PhysmatRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.all_surfaces_count = name_type_map['Uint'](self.context, 0, None)
		self.surface_res_count = name_type_map['Uint'](self.context, 0, None)
		self.classnames_count = name_type_map['Uint'](self.context, 0, None)
		self.stringbuffer_size = name_type_map['Uint'](self.context, 0, None)
		self.pointers = Array(self.context, 0, None, (0,), name_type_map['Uint64'])
		self.all_surfaces_flags = Array(self.context, 0, None, (0,), name_type_map['Uint64'])
		self.surface_res_indices = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.all_surfaces_names = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.surface_res_names = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.classnames_names = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.classnames_indices = Array(self.context, 0, None, (0,), name_type_map['Ubyte'])
		self.names = name_type_map['ZStringBuffer'](self.context, self.stringbuffer_size, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'all_surfaces_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'surface_res_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'classnames_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'stringbuffer_size', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'pointers', Array, (0, None, (5,), name_type_map['Uint64']), (False, None), (None, None)
		yield 'all_surfaces_flags', Array, (0, None, (None,), name_type_map['Uint64']), (False, None), (None, None)
		yield 'surface_res_indices', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (None, None)
		yield 'all_surfaces_names', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (None, None)
		yield 'surface_res_names', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (None, None)
		yield 'classnames_names', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (None, None)
		yield 'classnames_indices', Array, (0, None, (None,), name_type_map['Ubyte']), (False, None), (None, None)
		yield 'names', name_type_map['ZStringBuffer'], (None, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'all_surfaces_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'surface_res_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'classnames_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'stringbuffer_size', name_type_map['Uint'], (0, None), (False, None)
		yield 'pointers', Array, (0, None, (5,), name_type_map['Uint64']), (False, None)
		yield 'all_surfaces_flags', Array, (0, None, (instance.all_surfaces_count,), name_type_map['Uint64']), (False, None)
		yield 'surface_res_indices', Array, (0, None, (instance.surface_res_count,), name_type_map['Uint']), (False, None)
		yield 'all_surfaces_names', Array, (0, None, (instance.all_surfaces_count,), name_type_map['Uint']), (False, None)
		yield 'surface_res_names', Array, (0, None, (instance.surface_res_count,), name_type_map['Uint']), (False, None)
		yield 'classnames_names', Array, (0, None, (instance.classnames_count,), name_type_map['Uint']), (False, None)
		yield 'classnames_indices', Array, (0, None, (instance.classnames_count,), name_type_map['Ubyte']), (False, None)
		yield 'names', name_type_map['ZStringBuffer'], (instance.stringbuffer_size, None), (False, None)
