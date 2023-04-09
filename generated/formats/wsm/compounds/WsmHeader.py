import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class WsmHeader(MemStruct):

	"""
	56 bytes for JWE2
	"""

	__name__ = 'WsmHeader'

	_import_key = 'wsm.compounds.WsmHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.duration = 0.0

		# likely
		self.frame_count = 0

		# unk
		self.unknowns = Array(self.context, 0, None, (0,), Float)
		self.locs = ArrayPointer(self.context, self.frame_count, WsmHeader._import_map["wsm.compounds.Vector3"])
		self.quats = ArrayPointer(self.context, self.frame_count, WsmHeader._import_map["wsm.compounds.Vector4"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('duration', Float, (0, None), (False, None), (None, None))
		yield ('frame_count', Uint, (0, None), (False, None), (None, None))
		yield ('unknowns', Array, (0, None, (8,), Float), (False, None), (None, None))
		yield ('locs', ArrayPointer, (None, WsmHeader._import_map["wsm.compounds.Vector3"]), (False, None), (None, None))
		yield ('quats', ArrayPointer, (None, WsmHeader._import_map["wsm.compounds.Vector4"]), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'duration', Float, (0, None), (False, None)
		yield 'frame_count', Uint, (0, None), (False, None)
		yield 'unknowns', Array, (0, None, (8,), Float), (False, None)
		yield 'locs', ArrayPointer, (instance.frame_count, WsmHeader._import_map["wsm.compounds.Vector3"]), (False, None)
		yield 'quats', ArrayPointer, (instance.frame_count, WsmHeader._import_map["wsm.compounds.Vector4"]), (False, None)
