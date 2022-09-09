import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint


class SoundSfxVoice(BaseStruct):

	__name__ = 'SoundSfxVoice'

	_import_path = 'generated.formats.bnk.compounds.SoundSfxVoice'

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

	def __init__(self, context, arg=0, template=None, set_default=True):
		self._context = context
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of this section
		self.length = 0

		# id of this Sound SFX object
		self.sfx_id = 0

		# ?
		self.const_a = 0

		# ?
		self.const_b = 0

		# ?
		self.didx_id = 0

		# ?
		self.wem_length = 0

		# include this here so that numpy doesn't choke
		# self.extra = numpy.zeros((self.length - 17), dtype='byte')

