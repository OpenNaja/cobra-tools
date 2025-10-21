from generated.formats.janitorsettings.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class JanitorPreCount(MemStruct):

	"""
	and here comes the actual data part
	PZ has 13 floats (maybe some ints) before the counts
	PC has 11
	"""

	__name__ = 'JanitorPreCount'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_0 = name_type_map['Float'].from_value(0.9)
		self.unk_1 = name_type_map['Float'].from_value(1.1)
		self.unk_2 = name_type_map['Float'].from_value(0.25)
		self.extra_f_pz_1 = name_type_map['Float'](self.context, 0, None)
		self.extra_f_pz_2 = name_type_map['Float'](self.context, 0, None)
		self.unk_3 = name_type_map['Float'].from_value(-0.02)
		self.unk_4 = name_type_map['Float'](self.context, 0, None)
		self.unk_5 = name_type_map['Float'](self.context, 0, None)
		self.unk_6 = name_type_map['Float'](self.context, 0, None)
		self.unk_7 = name_type_map['Float'](self.context, 0, None)
		self.unk_8 = name_type_map['Uint'](self.context, 0, None)
		self.unk_9 = name_type_map['Float'](self.context, 0, None)
		self.unk_10 = name_type_map['Float'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'unk_0', name_type_map['Float'], (0, None), (False, 0.9), (None, None)
		yield 'unk_1', name_type_map['Float'], (0, None), (False, 1.1), (None, None)
		yield 'unk_2', name_type_map['Float'], (0, None), (False, 0.25), (None, None)
		yield 'extra_f_pz_1', name_type_map['Float'], (0, None), (False, None), (lambda context: (not context.user_version.use_djb) and (context.version >= 19), None)
		yield 'extra_f_pz_2', name_type_map['Float'], (0, None), (False, None), (lambda context: (not context.user_version.use_djb) and (context.version >= 19), None)
		yield 'unk_3', name_type_map['Float'], (0, None), (False, -0.02), (None, None)
		yield 'unk_4', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_5', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_6', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_7', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_8', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_9', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_10', name_type_map['Float'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_0', name_type_map['Float'], (0, None), (False, 0.9)
		yield 'unk_1', name_type_map['Float'], (0, None), (False, 1.1)
		yield 'unk_2', name_type_map['Float'], (0, None), (False, 0.25)
		if (not instance.context.user_version.use_djb) and (instance.context.version >= 19):
			yield 'extra_f_pz_1', name_type_map['Float'], (0, None), (False, None)
			yield 'extra_f_pz_2', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_3', name_type_map['Float'], (0, None), (False, -0.02)
		yield 'unk_4', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_5', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_6', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_7', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_8', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_9', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_10', name_type_map['Float'], (0, None), (False, None)
