from generated.array import Array
from generated.formats.bani.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class BanisRoot(MemStruct):

	"""
	older games: 40 bytes
	PC2: new structure, 4 pointers to keyframe data at start
	"""

	__name__ = 'BanisRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zeros = Array(self.context, 0, None, (0,), name_type_map['Uint'])

		# Size of BaniGpuAnimHeader block in bytes
		self.gpu_anim_headers_size = name_type_map['Uint'](self.context, 0, None)

		# Size of the first channels block in bytes
		self.channel_bones_size = name_type_map['Uint'](self.context, 0, None)

		# Size of the second channels block in bytes
		self.channel_bones_lod_size = name_type_map['Uint'](self.context, 0, None)

		# Size of the BaniKeys block in bytes
		self.keys_size = name_type_map['Uint'](self.context, 0, None)
		self.zeros = Array(self.context, 0, None, (0,), name_type_map['Uint64'])

		# bytes per bone * num bones
		self.bytes_per_frame = name_type_map['Uint'](self.context, 0, None)

		# 12 (v5-7 ushort[6]), 16 (v2 in PC1, ushort[8], apparently x,y,z,zero,x,y,z,w)
		self.bytes_per_bone = name_type_map['Uint'].from_value(12)

		# Number of frames for all bani files in banis buffer
		self.num_frames = name_type_map['Uint'](self.context, 0, None)

		# number of bones in data, must correspond to ms2
		self.num_bones = name_type_map['Uint'](self.context, 0, None)

		# For translation de-quantization
		self.quantization_info = name_type_map['QuantizationInfo'](self.context, 0, None)
		self.bani_count = name_type_map['Uint'](self.context, 0, None)
		self.zero_2 = name_type_map['Uint64'](self.context, 0, None)
		self.gpu_anim_headers = name_type_map['ArrayPointer'](self.context, self.bani_count, name_type_map['BaniGpuAnimHeader'])
		self.channel_bones = name_type_map['ForEachPointer'](self.context, self.gpu_anim_headers, name_type_map['BaniGpuChannels'])
		self.channel_bones_lod = name_type_map['ForEachPointer'](self.context, self.gpu_anim_headers, name_type_map['BaniGpuChannelsLod256'])

		# each bani can have different frame and bone counts from two different sources, so there's no way to get this mapping into the current xml syntax
		self.keys = name_type_map['Pointer'](self.context, self.keys_size, name_type_map['Blob'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'gpu_anim_headers', name_type_map['ArrayPointer'], (None, name_type_map['BaniGpuAnimHeader']), (False, None), (lambda context: context.version >= 7, None)
		yield 'channel_bones', name_type_map['ForEachPointer'], (None, name_type_map['BaniGpuChannels']), (False, None), (lambda context: context.version >= 7, None)
		yield 'channel_bones_lod', name_type_map['ForEachPointer'], (None, name_type_map['BaniGpuChannelsLod']), (False, None), (lambda context: context.version >= 7, True)
		yield 'channel_bones_lod', name_type_map['ForEachPointer'], (None, name_type_map['BaniGpuChannelsLod256']), (False, None), (lambda context: context.version >= 7, True)
		yield 'keys', name_type_map['Pointer'], (None, name_type_map['Blob']), (False, None), (lambda context: context.version >= 7, None)
		yield 'zeros', Array, (0, None, (3,), name_type_map['Uint']), (False, None), (lambda context: context.version >= 7, None)
		yield 'gpu_anim_headers_size', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 7, None)
		yield 'channel_bones_size', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 7, None)
		yield 'channel_bones_lod_size', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 7, None)
		yield 'keys_size', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 7, None)
		yield 'zeros', Array, (0, None, (2,), name_type_map['Uint64']), (False, None), (lambda context: context.version <= 5, None)
		yield 'bytes_per_frame', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'bytes_per_bone', name_type_map['Uint'], (0, None), (False, 12), (None, None)
		yield 'num_frames', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'num_bones', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'quantization_info', name_type_map['QuantizationInfo'], (0, None), (False, None), (lambda context: context.version <= 5, None)
		yield 'bani_count', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 7, None)
		yield 'zero_2', name_type_map['Uint64'], (0, None), (False, None), (lambda context: context.version >= 7, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version >= 7:
			yield 'gpu_anim_headers', name_type_map['ArrayPointer'], (instance.bani_count, name_type_map['BaniGpuAnimHeader']), (False, None)
			yield 'channel_bones', name_type_map['ForEachPointer'], (instance.gpu_anim_headers, name_type_map['BaniGpuChannels']), (False, None)
		if instance.context.version >= 7 and instance.channel_bones_size == instance.channel_bones_lod_size:
			yield 'channel_bones_lod', name_type_map['ForEachPointer'], (instance.gpu_anim_headers, name_type_map['BaniGpuChannelsLod']), (False, None)
		if instance.context.version >= 7 and instance.channel_bones_size != instance.channel_bones_lod_size:
			yield 'channel_bones_lod', name_type_map['ForEachPointer'], (instance.gpu_anim_headers, name_type_map['BaniGpuChannelsLod256']), (False, None)
		if instance.context.version >= 7:
			yield 'keys', name_type_map['Pointer'], (instance.keys_size, name_type_map['Blob']), (False, None)
			yield 'zeros', Array, (0, None, (3,), name_type_map['Uint']), (False, None)
			yield 'gpu_anim_headers_size', name_type_map['Uint'], (0, None), (False, None)
			yield 'channel_bones_size', name_type_map['Uint'], (0, None), (False, None)
			yield 'channel_bones_lod_size', name_type_map['Uint'], (0, None), (False, None)
			yield 'keys_size', name_type_map['Uint'], (0, None), (False, None)
		if instance.context.version <= 5:
			yield 'zeros', Array, (0, None, (2,), name_type_map['Uint64']), (False, None)
		yield 'bytes_per_frame', name_type_map['Uint'], (0, None), (False, None)
		yield 'bytes_per_bone', name_type_map['Uint'], (0, None), (False, 12)
		yield 'num_frames', name_type_map['Uint'], (0, None), (False, None)
		yield 'num_bones', name_type_map['Uint'], (0, None), (False, None)
		if instance.context.version <= 5:
			yield 'quantization_info', name_type_map['QuantizationInfo'], (0, None), (False, None)
		if instance.context.version >= 7:
			yield 'bani_count', name_type_map['Uint'], (0, None), (False, None)
			yield 'zero_2', name_type_map['Uint64'], (0, None), (False, None)
