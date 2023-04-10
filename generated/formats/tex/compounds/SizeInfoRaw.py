from generated.array import Array
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.tex.imports import name_type_map


class SizeInfoRaw(MemStruct):

	"""
	Data struct for headers of type 7
	"""

	__name__ = 'SizeInfoRaw'

	_import_key = 'tex.compounds.SizeInfoRaw'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# zero
		self.zero = 0

		# total dds buffer size
		self.data_size = 0

		# x size in pixels
		self.width = 0

		# y size in pixels
		self.height = 0

		# may be depth
		self.depth = 1
		self.num_tiles = 1

		# amount of mip map levels
		self.num_mips = 0

		# only found in PZ and JWE2
		self.unk_pz = 0

		# info about mip levels
		self.mip_maps = Array(self.context, 0, None, (0,), name_type_map['Mipmap'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('zero', name_type_map['Uint64'], (0, None), (True, 0), (None, None))
		yield ('data_size', name_type_map['Uint'], (0, None), (False, None), (None, None))
		yield ('width', name_type_map['Uint'], (0, None), (False, None), (None, None))
		yield ('height', name_type_map['Uint'], (0, None), (False, None), (None, None))
		yield ('depth', name_type_map['Uint'], (0, None), (True, 1), (None, None))
		yield ('num_tiles', name_type_map['Uint'], (0, None), (True, 1), (None, None))
		yield ('num_mips', name_type_map['Uint'], (0, None), (False, None), (None, None))
		yield ('unk_pz', name_type_map['Uint64'], (0, None), (True, 0), (lambda context: context.version >= 20, None))
		yield ('mip_maps', Array, (0, None, (None,), name_type_map['Mipmap']), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'zero', name_type_map['Uint64'], (0, None), (True, 0)
		yield 'data_size', name_type_map['Uint'], (0, None), (False, None)
		yield 'width', name_type_map['Uint'], (0, None), (False, None)
		yield 'height', name_type_map['Uint'], (0, None), (False, None)
		yield 'depth', name_type_map['Uint'], (0, None), (True, 1)
		yield 'num_tiles', name_type_map['Uint'], (0, None), (True, 1)
		yield 'num_mips', name_type_map['Uint'], (0, None), (False, None)
		if instance.context.version >= 20:
			yield 'unk_pz', name_type_map['Uint64'], (0, None), (True, 0)
		yield 'mip_maps', Array, (0, None, (instance.num_mips,), name_type_map['Mipmap']), (False, None)
