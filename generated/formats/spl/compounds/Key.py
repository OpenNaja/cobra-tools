from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.spl.compounds.ByteVector3 import ByteVector3
from generated.formats.spl.compounds.ShortVector3 import ShortVector3


class Key(MemStruct):

	"""
	JWE2: 16 bytes
	"""

	__name__ = 'Key'

	_import_key = 'spl.compounds.Key'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.pos = ShortVector3(self.context, 0, None)
		self.handle_left = ByteVector3(self.context, 0, None)
		self.handle_right = ByteVector3(self.context, 0, None)
		self.handle_scale = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('pos', ShortVector3, (0, None), (False, None), (None, None))
		yield ('handle_left', ByteVector3, (0, None), (False, None), (None, None))
		yield ('handle_right', ByteVector3, (0, None), (False, None), (None, None))
		yield ('handle_scale', Float, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'pos', ShortVector3, (0, None), (False, None)
		yield 'handle_left', ByteVector3, (0, None), (False, None)
		yield 'handle_right', ByteVector3, (0, None), (False, None)
		yield 'handle_scale', Float, (0, None), (False, None)
