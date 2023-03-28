from generated.formats.base.basic import Ubyte
from generated.formats.ms2.compounds.AbstractPointer import AbstractPointer


class BonePointer(AbstractPointer):

	__name__ = 'BonePointer'

	_import_key = 'ms2.compounds.BonePointer'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into bones
		self.index = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('index', Ubyte, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'index', Ubyte, (0, None), (False, None)


BonePointer.init_attributes()
