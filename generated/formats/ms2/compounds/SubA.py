from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte


class SubA(BaseStruct):

	__name__ = 'SubA'

	_import_key = 'ms2.compounds.SubA'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# increases, starting at 1
		self.index = 0

		# ?
		self.a = 240

		# ?
		self.b = 237

		# ?
		self.c = 254
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('index', Ubyte, (0, None), (False, None), None),
		('a', Ubyte, (0, None), (False, 240), None),
		('b', Ubyte, (0, None), (False, 237), None),
		('c', Ubyte, (0, None), (False, 254), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'index', Ubyte, (0, None), (False, None)
		yield 'a', Ubyte, (0, None), (False, 240)
		yield 'b', Ubyte, (0, None), (False, 237)
		yield 'c', Ubyte, (0, None), (False, 254)
