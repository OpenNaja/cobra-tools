from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort


class MaterialName(BaseStruct):

	__name__ = 'MaterialName'

	_import_key = 'ms2.compounds.MaterialName'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into ms2 names array
		self.name_index = 0

		# unknown, nonzero in PZ flamingo juvenile, might be junk (padding)
		self.some_index = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version >= 47:
			yield 'name_index', Uint, (0, None), (False, None)
		if instance.context.version <= 32:
			yield 'name_index', Ushort, (0, None), (False, None)
		if instance.context.version >= 47:
			yield 'some_index', Uint, (0, None), (False, None)
		if instance.context.version <= 32:
			yield 'some_index', Ushort, (0, None), (False, None)
