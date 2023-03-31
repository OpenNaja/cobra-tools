import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Int
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class AttribData(MemStruct):

	__name__ = 'AttribData'

	_import_key = 'fgm.compounds.AttribData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.value = Array(self.context, 0, None, (0,), Int)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('value', Array, (0, None, (1,), Float), (False, None), (None, True))
		yield ('value', Array, (0, None, (2,), Float), (False, None), (None, True))
		yield ('value', Array, (0, None, (3,), Float), (False, None), (None, True))
		yield ('value', Array, (0, None, (4,), Float), (False, None), (None, True))
		yield ('value', Array, (0, None, (1,), Int), (False, None), (None, True))
		yield ('value', Array, (0, None, (1,), Int), (False, None), (None, True))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.arg.dtype == 0:
			yield 'value', Array, (0, None, (1,), Float), (False, None)
		if instance.arg.dtype == 1:
			yield 'value', Array, (0, None, (2,), Float), (False, None)
		if instance.arg.dtype == 2:
			yield 'value', Array, (0, None, (3,), Float), (False, None)
		if instance.arg.dtype == 3:
			yield 'value', Array, (0, None, (4,), Float), (False, None)
		if instance.arg.dtype == 5:
			yield 'value', Array, (0, None, (1,), Int), (False, None)
		if instance.arg.dtype == 6:
			yield 'value', Array, (0, None, (1,), Int), (False, None)


AttribData.init_attributes()
