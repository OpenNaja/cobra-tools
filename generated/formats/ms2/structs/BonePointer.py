from generated.formats.ms2.imports import name_type_map
from generated.formats.ms2.structs.AbstractPointer import AbstractPointer


class BonePointer(AbstractPointer):

	__name__ = 'BonePointer'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into bones
		self.index = name_type_map['BonePointerIndex'].from_value(-1)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'index', name_type_map['BonePointerIndex'], (0, None), (False, -1), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'index', name_type_map['BonePointerIndex'], (0, None), (False, -1)
