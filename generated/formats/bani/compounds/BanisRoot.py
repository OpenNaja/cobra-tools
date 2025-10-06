from generated.array import Array
from generated.formats.bani.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class BanisRoot(MemStruct):

	"""
	older games: 40 bytes
	PC2: new structure, 4 pointers to keyframe data at start
	"""

	__name__ = 'BanisRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zeros = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.count_a = name_type_map['Uint'](self.context, 0, None)
		self.count_b_0 = name_type_map['Uint'](self.context, 0, None)
		self.count_b_1 = name_type_map['Uint'](self.context, 0, None)
		self.keys_size = name_type_map['Uint'](self.context, 0, None)
		self.zeros = Array(self.context, 0, None, (0,), name_type_map['Uint64'])

		# bytes per bone * num bones
		self.bytes_per_frame = name_type_map['Uint'](self.context, 0, None)

		# seen 12 (PC2 pigeon), 16 (PC1 pigeon)
		self.bytes_per_bone = name_type_map['Uint'](self.context, 0, None)

		# Number of frames for all bani files in banis buffer
		self.num_frames = name_type_map['Uint'](self.context, 0, None)

		# number of bones in data, must correspond to ms2
		self.num_bones = name_type_map['Uint'](self.context, 0, None)

		# scale for translation range
		self.loc_scale = name_type_map['Float'](self.context, 0, None)

		# related to minimum of scaled translations, offsets everything ingame the same across all axes
		self.loc_min = name_type_map['Float'](self.context, 0, None)
		self.bani_count = name_type_map['Uint'](self.context, 0, None)
		self.zero_2 = name_type_map['Uint64'](self.context, 0, None)
		self.bani_data = name_type_map['ArrayPointer'](self.context, self.bani_count, name_type_map['BaniData'])
		self.bones_foreach_bani_data = name_type_map['ForEachPointer'](self.context, self.bani_data, name_type_map['BaniBones'])
		self.bones_2_foreach_bani_data = name_type_map['ForEachPointer'](self.context, self.bani_data, name_type_map['BaniBones'])
		self.keys = name_type_map['Pointer'](self.context, (self.num_frames, self.num_bones), name_type_map['Keys'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'bani_data', name_type_map['ArrayPointer'], (None, name_type_map['BaniData']), (False, None), (lambda context: context.version >= 7, None)
		yield 'bones_foreach_bani_data', name_type_map['ForEachPointer'], (None, name_type_map['BaniBones']), (False, None), (lambda context: context.version >= 7, None)
		yield 'bones_2_foreach_bani_data', name_type_map['ForEachPointer'], (None, name_type_map['BaniBones']), (False, None), (lambda context: context.version >= 7, None)
		yield 'keys', name_type_map['Pointer'], (None, name_type_map['Keys']), (False, None), (lambda context: context.version >= 7, None)
		yield 'zeros', Array, (0, None, (3,), name_type_map['Uint']), (False, None), (lambda context: context.version >= 7, None)
		yield 'count_a', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 7, None)
		yield 'count_b_0', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 7, None)
		yield 'count_b_1', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 7, None)
		yield 'keys_size', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 7, None)
		yield 'zeros', Array, (0, None, (2,), name_type_map['Uint64']), (False, None), (lambda context: context.version <= 5, None)
		yield 'bytes_per_frame', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'bytes_per_bone', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'num_frames', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'num_bones', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'loc_scale', name_type_map['Float'], (0, None), (False, None), (lambda context: context.version <= 5, None)
		yield 'loc_min', name_type_map['Float'], (0, None), (False, None), (lambda context: context.version <= 5, None)
		yield 'bani_count', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 7, None)
		yield 'zero_2', name_type_map['Uint64'], (0, None), (False, None), (lambda context: context.version >= 7, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version >= 7:
			yield 'bani_data', name_type_map['ArrayPointer'], (instance.bani_count, name_type_map['BaniData']), (False, None)
			yield 'bones_foreach_bani_data', name_type_map['ForEachPointer'], (instance.bani_data, name_type_map['BaniBones']), (False, None)
			yield 'bones_2_foreach_bani_data', name_type_map['ForEachPointer'], (instance.bani_data, name_type_map['BaniBones']), (False, None)
			yield 'keys', name_type_map['Pointer'], ((instance.num_frames, instance.num_bones), name_type_map['Keys']), (False, None)
			yield 'zeros', Array, (0, None, (3,), name_type_map['Uint']), (False, None)
			yield 'count_a', name_type_map['Uint'], (0, None), (False, None)
			yield 'count_b_0', name_type_map['Uint'], (0, None), (False, None)
			yield 'count_b_1', name_type_map['Uint'], (0, None), (False, None)
			yield 'keys_size', name_type_map['Uint'], (0, None), (False, None)
		if instance.context.version <= 5:
			yield 'zeros', Array, (0, None, (2,), name_type_map['Uint64']), (False, None)
		yield 'bytes_per_frame', name_type_map['Uint'], (0, None), (False, None)
		yield 'bytes_per_bone', name_type_map['Uint'], (0, None), (False, None)
		yield 'num_frames', name_type_map['Uint'], (0, None), (False, None)
		yield 'num_bones', name_type_map['Uint'], (0, None), (False, None)
		if instance.context.version <= 5:
			yield 'loc_scale', name_type_map['Float'], (0, None), (False, None)
			yield 'loc_min', name_type_map['Float'], (0, None), (False, None)
		if instance.context.version >= 7:
			yield 'bani_count', name_type_map['Uint'], (0, None), (False, None)
			yield 'zero_2', name_type_map['Uint64'], (0, None), (False, None)
