
from generated.context import ContextReference
from generated.formats.ms2.compound.HitCheckEntry import HitCheckEntry

from generated.context import ContextReference


class HitcheckReader:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.set_defaults()

	def set_defaults(self):
		pass

	def read(self, stream):
		self.io_start = stream.tell()
		for jointinfo in self.arg:
			jointinfo.hit_check = []
			for i in range(jointinfo.hitcheck_count):
				hc = HitCheckEntry(self.context)
				hc.read(stream)
				jointinfo.hit_check.append(hc)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'HitcheckReader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		for jointinfo in self.arg:
			s += str(jointinfo.hit_check)
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s

