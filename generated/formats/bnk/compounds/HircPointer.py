from generated.base_struct import BaseStruct
from generated.formats.bnk.compounds.MusicTrack import MusicTrack
from generated.formats.bnk.compounds.SoundSfxVoice import SoundSfxVoice
from generated.formats.bnk.compounds.TypeOther import TypeOther
from generated.formats.bnk.enums.HircType import HircType


class HircPointer(BaseStruct):

	__name__ = 'HircPointer'

	_import_key = 'bnk.compounds.HircPointer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.id = HircType(self.context, 0, None)
		self.data = TypeOther(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('id', HircType, (0, None), (False, None), None)
		yield ('data', SoundSfxVoice, (0, None), (False, None), True)
		yield ('data', MusicTrack, (0, None), (False, None), True)
		yield ('data', TypeOther, (0, None), (False, None), True)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'id', HircType, (0, None), (False, None)
		if instance.id == 2:
			yield 'data', SoundSfxVoice, (0, None), (False, None)
		if instance.id == 11:
			yield 'data', MusicTrack, (0, None), (False, None)
		if (instance.id != 2) and (instance.id != 11):
			yield 'data', TypeOther, (0, None), (False, None)


HircPointer.init_attributes()
