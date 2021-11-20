from generated.array import Array
from generated.context import ContextReference
from generated.formats.base.basic import ZString
from generated.formats.matcol.compound.MaterialInfo import MaterialInfo


class VariantWrapper:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.info = MaterialInfo(self.context, None, None)
		self.materials = Array((self.info.material_count), ZString, self.context, None, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.info = MaterialInfo(self.context, None, None)
		self.materials = Array((self.info.material_count), ZString, self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.info = stream.read_type(MaterialInfo, (self.context, None, None))
		self.materials = stream.read_zstrings((self.info.material_count))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.info)
		stream.write_zstrings(self.materials)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'VariantWrapper [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* info = {self.info.__repr__()}'
		s += f'\n	* materials = {self.materials.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
