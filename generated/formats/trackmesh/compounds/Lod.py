from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Lod(MemStruct):

	"""
	PC: 16 bytes
	"""

	__name__ = 'Lod'

	_import_key = 'trackmesh.compounds.Lod'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = 0
		self.b = 0
		self.c = 0
		self.distance = 0.0
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('a', Uint, (0, None), (False, None), None),
		('b', Uint, (0, None), (False, None), None),
		('c', Uint, (0, None), (False, None), None),
		('distance', Float, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'a', Uint, (0, None), (False, None)
		yield 'b', Uint, (0, None), (False, None)
		yield 'c', Uint, (0, None), (False, None)
		yield 'distance', Float, (0, None), (False, None)
