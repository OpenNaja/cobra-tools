from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte


class Triplet(BaseStruct):

	"""
	3 bytes - constant per mime and version
	"""

	__name__ = 'Triplet'

	_import_key = 'ovl.compounds.Triplet'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# ?
		self.a = 0

		# ?
		self.b = 0

		# ?
		self.c = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('a', Ubyte, (0, None), (False, None), None),
		('b', Ubyte, (0, None), (False, None), None),
		('c', Ubyte, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'a', Ubyte, (0, None), (False, None)
		yield 'b', Ubyte, (0, None), (False, None)
		yield 'c', Ubyte, (0, None), (False, None)

	def __eq__(self, other):
		if isinstance(other, Triplet):
			return self.a == other.a and self.b == other.b and self.c == other.c

