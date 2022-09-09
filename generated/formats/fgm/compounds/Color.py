from generated.formats.base.basic import Ubyte
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Color(MemStruct):

	"""
	4 bytes
	"""

	__name__ = 'Color'

	_import_path = 'generated.formats.fgm.compounds.Color'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.r = 0
		self.g = 0
		self.b = 0
		self.a = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'r', Ubyte, (0, None), (False, None)
		yield 'g', Ubyte, (0, None), (False, None)
		yield 'b', Ubyte, (0, None), (False, None)
		yield 'a', Ubyte, (0, None), (False, None)
