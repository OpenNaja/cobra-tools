from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ParticleAtlasHeader(MemStruct):

	__name__ = 'ParticleAtlasHeader'

	_import_path = 'generated.formats.particle.compounds.ParticleAtlasHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# matches number in tex file name
		self.id = 0
		self.zero = 0
		self.tex_name = Pointer(self.context, 0, ZString)
		self.gfr_name = Pointer(self.context, 0, ZString)

		# tex file used by atlas
		self.dependency_name = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.id = 0
		self.zero = 0
		self.tex_name = Pointer(self.context, 0, ZString)
		self.gfr_name = Pointer(self.context, 0, ZString)
		self.dependency_name = Pointer(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.tex_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.gfr_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.id = Uint.from_stream(stream, instance.context, 0, None)
		instance.zero = Uint.from_stream(stream, instance.context, 0, None)
		instance.dependency_name = Pointer.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.tex_name, int):
			instance.tex_name.arg = 0
		if not isinstance(instance.gfr_name, int):
			instance.gfr_name.arg = 0
		if not isinstance(instance.dependency_name, int):
			instance.dependency_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.tex_name)
		Pointer.to_stream(stream, instance.gfr_name)
		Uint.to_stream(stream, instance.id)
		Uint.to_stream(stream, instance.zero)
		Pointer.to_stream(stream, instance.dependency_name)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'tex_name', Pointer, (0, ZString), (False, None)
		yield 'gfr_name', Pointer, (0, ZString), (False, None)
		yield 'id', Uint, (0, None), (False, None)
		yield 'zero', Uint, (0, None), (False, None)
		yield 'dependency_name', Pointer, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'ParticleAtlasHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* tex_name = {self.fmt_member(self.tex_name, indent+1)}'
		s += f'\n	* gfr_name = {self.fmt_member(self.gfr_name, indent+1)}'
		s += f'\n	* id = {self.fmt_member(self.id, indent+1)}'
		s += f'\n	* zero = {self.fmt_member(self.zero, indent+1)}'
		s += f'\n	* dependency_name = {self.fmt_member(self.dependency_name, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
