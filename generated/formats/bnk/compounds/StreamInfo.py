from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64


class StreamInfo(BaseStruct):

	"""
	Describes a wem file in an s type bank stream
	"""

	__name__ = 'StreamInfo'

	_import_key = 'bnk.compounds.StreamInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.offset = 0
		self.size = 0

		# referred to by the events aux file
		self.event_id = 0
		self.zero = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('offset', Uint64, (0, None), (False, None), None),
		('size', Uint64, (0, None), (False, None), None),
		('event_id', Uint, (0, None), (False, None), None),
		('zero', Uint, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'offset', Uint64, (0, None), (False, None)
		yield 'size', Uint64, (0, None), (False, None)
		yield 'event_id', Uint, (0, None), (False, None)
		yield 'zero', Uint, (0, None), (False, None)
