import generated.formats.matcol.compounds.RootFrag
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MatcolRoot(MemStruct):

	"""
	root_entry data
	"""

	__name__ = MatcolRoot

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# always 1
		self.one = 0
		self.main = Pointer(self.context, 0, generated.formats.matcol.compounds.RootFrag.RootFrag)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.one = 0
		self.main = Pointer(self.context, 0, generated.formats.matcol.compounds.RootFrag.RootFrag)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.main = Pointer.from_stream(stream, instance.context, 0, generated.formats.matcol.compounds.RootFrag.RootFrag)
		instance.one = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.main, int):
			instance.main.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.main)
		Uint64.to_stream(stream, instance.one)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'main', Pointer, (0, generated.formats.matcol.compounds.RootFrag.RootFrag), (False, None)
		yield 'one', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'MatcolRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* main = {self.fmt_member(self.main, indent+1)}'
		s += f'\n	* one = {self.fmt_member(self.one, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
