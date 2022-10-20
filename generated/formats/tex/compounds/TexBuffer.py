from generated.formats.base.basic import Int
from generated.formats.base.basic import Short
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class TexBuffer(MemStruct):

	"""
	Describes one buffer of a tex / texturestream file.
	24 bytes per texture buffer
	"""

	__name__ = 'TexBuffer'

	_import_key = 'tex.compounds.TexBuffer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# byte offset in the combined buffer
		self.offset = 0

		# byte size of this tex buffer
		self.size = 0

		# index of first mip used in this buffer
		self.first_mip = 0

		# amount of mip levels included in this buffer
		self.mip_count = 0
		self.padding_0 = 0
		self.padding_1 = 0
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('offset', Uint64, (0, None), (False, None), None),
		('size', Uint64, (0, None), (False, None), None),
		('first_mip', Ubyte, (0, None), (False, None), None),
		('mip_count', Ubyte, (0, None), (False, None), None),
		('padding_0', Short, (0, None), (True, 0), None),
		('padding_1', Int, (0, None), (True, 0), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'offset', Uint64, (0, None), (False, None)
		yield 'size', Uint64, (0, None), (False, None)
		yield 'first_mip', Ubyte, (0, None), (False, None)
		yield 'mip_count', Ubyte, (0, None), (False, None)
		yield 'padding_0', Short, (0, None), (True, 0)
		yield 'padding_1', Int, (0, None), (True, 0)
