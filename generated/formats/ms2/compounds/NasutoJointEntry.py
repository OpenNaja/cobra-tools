from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ms2.compounds.Matrix33 import Matrix33
from generated.formats.ms2.compounds.Vector4 import Vector4


class NasutoJointEntry(BaseStruct):

	"""
	60 bytes
	"""

	__name__ = 'NasutoJointEntry'

	_import_path = 'generated.formats.ms2.compounds.NasutoJointEntry'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# index into bone list
		self.child = 0

		# index into bone list
		self.parent = 0

		# 0
		self.zero = 0

		# no clue what space this is in
		self.matrix = Matrix33(self.context, 0, None)

		# seems to be degrees of freedom or something like that, possibly an ellipsoid
		self.vector = Vector4(self.context, 0, None)

		# 1
		self.one = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'child', Ubyte, (0, None), (False, None)
		yield 'parent', Ubyte, (0, None), (False, None)
		yield 'zero', Ushort, (0, None), (False, None)
		yield 'matrix', Matrix33, (0, None), (False, None)
		yield 'vector', Vector4, (0, None), (False, None)
		yield 'one', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'NasutoJointEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
