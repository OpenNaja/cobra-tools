from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ushort


class PoolGroup(BaseStruct):

	"""
	Located at start of deflated archive stream
	"""

	__name__ = 'PoolGroup'

	_import_path = 'generated.formats.ovl.compounds.PoolGroup'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# Type of the pools that follow
		self.type = 0

		# Amount of pools of that type that follow the pool types block
		self.num_pools = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.type = 0
		self.num_pools = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.type = Ushort.from_stream(stream, instance.context, 0, None)
		instance.num_pools = Ushort.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Ushort.to_stream(stream, instance.type)
		Ushort.to_stream(stream, instance.num_pools)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'type', Ushort, (0, None), (False, None)
		yield 'num_pools', Ushort, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'PoolGroup [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* type = {self.fmt_member(self.type, indent+1)}'
		s += f'\n	* num_pools = {self.fmt_member(self.num_pools, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
