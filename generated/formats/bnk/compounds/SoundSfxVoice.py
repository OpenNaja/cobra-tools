import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint


class SoundSfxVoice(BaseStruct):

	__name__ = 'SoundSfxVoice'

	_import_key = 'bnk.compounds.SoundSfxVoice'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# length of this section
		self.length = 0

		# id of this Sound SFX object
		self.id = 0

		# ?
		self.const_a = 0

		# ?
		self.const_b = 0

		# ?
		self.didx_id = 0

		# ?
		self.wem_length = 0

		# ?
		self.extra = Array(self.context, 0, None, (0,), Byte)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('length', Uint, (0, None), (False, None), None)
		yield ('id', Uint, (0, None), (False, None), None)
		yield ('const_a', Uint, (0, None), (False, None), None)
		yield ('const_b', Byte, (0, None), (False, None), None)
		yield ('didx_id', Uint, (0, None), (False, None), None)
		yield ('wem_length', Uint, (0, None), (False, None), None)
		yield ('extra', Array, (0, None, (None,), Byte), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'length', Uint, (0, None), (False, None)
		yield 'id', Uint, (0, None), (False, None)
		yield 'const_a', Uint, (0, None), (False, None)
		yield 'const_b', Byte, (0, None), (False, None)
		yield 'didx_id', Uint, (0, None), (False, None)
		yield 'wem_length', Uint, (0, None), (False, None)
		yield 'extra', Array, (0, None, (instance.length - 17,), Byte), (False, None)


SoundSfxVoice.init_attributes()
