from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.path.compounds.SupportAttach import SupportAttach


class SupportAttachExtra(SupportAttach):

	__name__ = 'SupportAttachExtra'

	_import_key = 'path.compounds.SupportAttachExtra'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_float_1 = 0.0
		self.unk_int_3 = 0
		self.padding = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'unk_float_1', Float, (0, None), (False, None)
		yield 'unk_int_3', Uint, (0, None), (False, None)
		yield 'padding', Uint64, (0, None), (True, 0)
