# START_GLOBALS
from generated.formats.ms2.compounds.HitCheckEntry import HitCheckEntry
from generated.base_struct import BaseStruct

# END_GLOBALS

class HitcheckReader(BaseStruct):


	# START_CLASS

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

	def get_info_str(self):
		return f'HitcheckReader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		for jointinfo in self.arg:
			s += str(jointinfo.hitchecks)
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
