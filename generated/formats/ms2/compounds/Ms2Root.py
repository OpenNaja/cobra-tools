import numpy
from generated.array import Array
from generated.formats.base.basic import Short
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Ms2Root(MemStruct):

	"""
	root header of the ms2
	48 bytes
	"""

	__name__ = 'Ms2Root'

	_import_key = 'ms2.compounds.Ms2Root'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# see version tag
		self.version = 0

		# total count of vertex buffers, including streamed buffers
		self.vertex_buffer_count = 0
		self.mdl_2_count = 0

		# count of names in ms2 buffer0
		self.name_count = 0

		# -1 if there is no vertex buffer at all; else count of static buffers
		self.stream_count = 0
		self.zeros = Array(self.context, 0, None, (0,), Uint)

		# ms2's static buffer_info or empty (if no buffers)
		self.buffer_infos = ArrayPointer(self.context, self.vertex_buffer_count, Ms2Root._import_map["ms2.compounds.BufferInfo"])

		# one for each mdl2
		self.model_infos = ArrayPointer(self.context, self.mdl_2_count, Ms2Root._import_map["ms2.compounds.ModelInfo"])

		# data as in get_buffer_presence()
		self.buffers_presence = ArrayPointer(self.context, self.vertex_buffer_count, Ms2Root._import_map["ms2.compounds.BufferPresence"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'version', Uint, (0, None), (False, None)
		yield 'vertex_buffer_count', Ushort, (0, None), (False, None)
		yield 'mdl_2_count', Ushort, (0, None), (False, None)
		yield 'name_count', Ushort, (0, None), (False, None)
		yield 'stream_count', Short, (0, None), (False, None)
		yield 'zeros', Array, (0, None, (3,), Uint), (False, None)
		yield 'buffer_infos', ArrayPointer, (instance.vertex_buffer_count, Ms2Root._import_map["ms2.compounds.BufferInfo"]), (False, None)
		yield 'model_infos', ArrayPointer, (instance.mdl_2_count, Ms2Root._import_map["ms2.compounds.ModelInfo"]), (False, None)
		yield 'buffers_presence', ArrayPointer, (instance.vertex_buffer_count, Ms2Root._import_map["ms2.compounds.BufferPresence"]), (False, None)
