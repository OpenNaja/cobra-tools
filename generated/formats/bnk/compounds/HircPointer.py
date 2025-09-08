
import logging
from generated.base_struct import BaseStruct

from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class HircPointer(BaseStruct):

	__name__ = 'HircPointer'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.id = name_type_map['HircType'](self.context, 0, None)

		# length of the following data block
		self.length = name_type_map['Uint'](self.context, 0, None)
		self.data = name_type_map['TypeOther'](self.context, self.length, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'id', name_type_map['HircType'], (0, None), (False, None), (None, None)
		yield 'length', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'data', name_type_map['Sound'], (None, None), (False, None), (None, True)
		yield 'data', name_type_map['EventAction'], (None, None), (False, None), (None, True)
		yield 'data', name_type_map['Event'], (None, None), (False, None), (None, True)
		yield 'data', name_type_map['RandomOrSequenceContainer'], (None, None), (False, None), (None, True)
		yield 'data', name_type_map['MusicTrack'], (None, None), (False, None), (None, True)
		yield 'data', name_type_map['TypeOther'], (None, None), (False, None), (None, True)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'id', name_type_map['HircType'], (0, None), (False, None)
		yield 'length', name_type_map['Uint'], (0, None), (False, None)
		if instance.id == 2:
			yield 'data', name_type_map['Sound'], (instance.length, None), (False, None)
		if instance.id == 3:
			yield 'data', name_type_map['EventAction'], (instance.length, None), (False, None)
		if instance.id == 4:
			yield 'data', name_type_map['Event'], (instance.length, None), (False, None)
		if instance.id == 5:
			yield 'data', name_type_map['RandomOrSequenceContainer'], (instance.length, None), (False, None)
		if instance.id == 11:
			yield 'data', name_type_map['MusicTrack'], (instance.length, None), (False, None)
		if (instance.id != 2) and ((instance.id != 3) and ((instance.id != 4) and ((instance.id != 5) and (instance.id != 11)))):
			yield 'data', name_type_map['TypeOther'], (instance.length, None), (False, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		if instance.data.io_size != instance.length:
			logging.warning(f"HIRC block {instance.id.name} at offset {instance.io_start} expected {instance.length}, but read {instance.data.io_size} bytes")
			stream.seek(instance.data.io_start + instance.length)
