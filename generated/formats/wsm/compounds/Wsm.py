import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.ovl_base.compounds.GenericHeader import GenericHeader
from generated.formats.wsm.compounds.WsmHeader import WsmHeader


class Wsm(GenericHeader):

	__name__ = 'Wsm'

	_import_key = 'wsm.compounds.Wsm'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.header = WsmHeader(self.context, 0, None)

		# xyz
		self.locs = Array(self.context, 0, None, (0,), Float)

		# xyzw
		self.quats = Array(self.context, 0, None, (0,), Float)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('header', WsmHeader, (0, None), (False, None), (None, None))
		yield ('locs', Array, (0, None, (None, 3,), Float), (False, None), (None, None))
		yield ('quats', Array, (0, None, (None, 4,), Float), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'header', WsmHeader, (0, None), (False, None)
		yield 'locs', Array, (0, None, (instance.header.frame_count, 3,), Float), (False, None)
		yield 'quats', Array, (0, None, (instance.header.frame_count, 4,), Float), (False, None)
