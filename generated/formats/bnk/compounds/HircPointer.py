
import logging
from generated.base_struct import BaseStruct

from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class HircPointer(BaseStruct):

	__name__ = 'HircPointer'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.id = name_type_map['HircType'](self.context, 0, None)
		self.data = name_type_map['TypeOther'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'id', name_type_map['HircType'], (0, None), (False, None), (None, None)
		yield 'data', name_type_map['SoundSfxVoice'], (0, None), (False, None), (None, True)
		yield 'data', name_type_map['EventAction'], (0, None), (False, None), (None, True)
		yield 'data', name_type_map['Event'], (0, None), (False, None), (None, True)
		yield 'data', name_type_map['MusicTrack'], (0, None), (False, None), (None, True)
		yield 'data', name_type_map['TypeOther'], (0, None), (False, None), (None, True)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'id', name_type_map['HircType'], (0, None), (False, None)
		if instance.id == 2:
			yield 'data', name_type_map['SoundSfxVoice'], (0, None), (False, None)
		if instance.id == 3:
			yield 'data', name_type_map['EventAction'], (0, None), (False, None)
		if instance.id == 4:
			yield 'data', name_type_map['Event'], (0, None), (False, None)
		if instance.id == 11:
			yield 'data', name_type_map['MusicTrack'], (0, None), (False, None)
		if (instance.id != 2) and ((instance.id != 3) and ((instance.id != 4) and (instance.id != 11))):
			yield 'data', name_type_map['TypeOther'], (0, None), (False, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		# 4 bytes used on length that are not part of the size of the struct
		actual_size = instance.data.io_size - 4
		if actual_size != instance.data.length:
			logging.warning(f"HIRC block {instance.id.name} at offset {instance.io_start} expected {instance.data.length}, but read {actual_size} bytes")
			stream.seek(instance.data.io_start + 4 + instance.data.length)
