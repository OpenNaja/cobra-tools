from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ushort


class PoolGroup(BaseStruct):

	"""
	Located at start of deflated archive stream
	"""

	__name__ = 'PoolGroup'

	_import_key = 'ovl.compounds.PoolGroup'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Type of the pools that follow
		self.type = 0

		# Amount of pools of that type that follow the pool types block
		self.num_pools = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('type', Ushort, (0, None), (False, None), (None, None))
		yield ('num_pools', Ushort, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'type', Ushort, (0, None), (False, None)
		yield 'num_pools', Ushort, (0, None), (False, None)
