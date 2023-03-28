import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class BanisRoot(MemStruct):

	"""
	40 bytes
	"""

	__name__ = 'BanisRoot'

	_import_key = 'bani.compounds.BanisRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zeros = Array(self.context, 0, None, (0,), Uint64)

		# bytes per bone * num bones
		self.bytes_per_frame = 0

		# how many bytes for each bone per frame
		self.bytes_per_bone = 0

		# Number of frames for all bani files in banis buffer
		self.num_frames = 0

		# matches number of bones parrot has
		self.num_bones = 0

		# translation range
		self.loc_scale = 0.0

		# translation range
		self.loc_offset = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('zeros', Array, (0, None, (2,), Uint64), (False, None), None)
		yield ('bytes_per_frame', Uint, (0, None), (False, None), None)
		yield ('bytes_per_bone', Uint, (0, None), (False, None), None)
		yield ('num_frames', Uint, (0, None), (False, None), None)
		yield ('num_bones', Uint, (0, None), (False, None), None)
		yield ('loc_scale', Float, (0, None), (False, None), None)
		yield ('loc_offset', Float, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'zeros', Array, (0, None, (2,), Uint64), (False, None)
		yield 'bytes_per_frame', Uint, (0, None), (False, None)
		yield 'bytes_per_bone', Uint, (0, None), (False, None)
		yield 'num_frames', Uint, (0, None), (False, None)
		yield 'num_bones', Uint, (0, None), (False, None)
		yield 'loc_scale', Float, (0, None), (False, None)
		yield 'loc_offset', Float, (0, None), (False, None)


BanisRoot.init_attributes()
