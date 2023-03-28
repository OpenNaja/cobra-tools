from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TrackData(MemStruct):

	"""
	PC: 48 bytes
	"""

	__name__ = 'TrackData'

	_import_key = 'trackmesh.compounds.TrackData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = 0
		self.b = 0
		self.c = 0
		self.d = 0
		self.place_id = Pointer(self.context, 0, ZString)
		self.file = Pointer(self.context, 0, ZString)
		self.offset_id = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('place_id', Pointer, (0, ZString), (False, None), (None, None))
		yield ('file', Pointer, (0, ZString), (False, None), (None, None))
		yield ('a', Uint, (0, None), (False, None), (None, None))
		yield ('b', Uint, (0, None), (False, None), (None, None))
		yield ('c', Uint64, (0, None), (False, None), (None, None))
		yield ('offset_id', Pointer, (0, ZString), (False, None), (None, None))
		yield ('d', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'place_id', Pointer, (0, ZString), (False, None)
		yield 'file', Pointer, (0, ZString), (False, None)
		yield 'a', Uint, (0, None), (False, None)
		yield 'b', Uint, (0, None), (False, None)
		yield 'c', Uint64, (0, None), (False, None)
		yield 'offset_id', Pointer, (0, ZString), (False, None)
		yield 'd', Uint64, (0, None), (False, None)


TrackData.init_attributes()
