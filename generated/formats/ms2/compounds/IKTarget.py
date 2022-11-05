from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte


class IKTarget(BaseStruct):

	"""
	2 bytes, indices into bones list
	"""

	__name__ = 'IKTarget'

	_import_key = 'ms2.compounds.IKTarget'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ik_blend = 0
		self.ik_end = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('ik_blend', Ubyte, (0, None), (False, None), None),
		('ik_end', Ubyte, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ik_blend', Ubyte, (0, None), (False, None)
		yield 'ik_end', Ubyte, (0, None), (False, None)
