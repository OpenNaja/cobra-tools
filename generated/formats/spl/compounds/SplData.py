from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.spl.compounds.Key import Key
from generated.formats.spl.compounds.Vector3 import Vector3


class SplData(MemStruct):

	"""
	JWE2: 16 + n*16 bytes
	"""

	__name__ = 'SplData'

	_import_key = 'spl.compounds.SplData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.offset = Vector3(self.context, 0, None)
		self.scale = 0.0
		self.keys = Array(self.context, 0, None, (0,), Key)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('offset', Vector3, (0, None), (False, None), None)
		yield ('scale', Float, (0, None), (False, None), None)
		yield ('keys', Array, (0, None, (None,), Key), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'offset', Vector3, (0, None), (False, None)
		yield 'scale', Float, (0, None), (False, None)
		yield 'keys', Array, (0, None, (instance.arg,), Key), (False, None)


SplData.init_attributes()
