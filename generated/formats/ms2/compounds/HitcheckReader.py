
from generated.formats.ms2.compounds.HitCheckEntry import HitCheckEntry
from generated.base_struct import BaseStruct

from generated.base_struct import BaseStruct


class HitcheckReader(BaseStruct):

	"""
	This reads and assigns hitchecks to each jointinfo that is passed to it
	"""

	__name__ = 'HitcheckReader'

	_import_key = 'ms2.compounds.HitcheckReader'

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		pass

	@classmethod
	def read_fields(cls, stream, instance):
		for jointinfo in instance.arg:
			jointinfo.hitchecks = []
			for i in range(jointinfo.hitcheck_count):
				hc = HitCheckEntry(instance.context)
				hc.read(stream)
				jointinfo.hitchecks.append(hc)

	@classmethod
	def write_fields(cls, stream, instance):
		pass

	@classmethod
	def get_fields_str(cls, instance, indent=0):
		s = ''
		for jointinfo in instance.arg:
			s += str(jointinfo.hitchecks)
		return s


