from generated.formats.ovl_base.compounds.GenericHeader import GenericHeader
from generated.formats.voxelskirt.compounds.SizedStrData import SizedStrData


class Header(GenericHeader):

	"""
	Found at the beginning of every OVL file
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# always = 0
		self.info = SizedStrData(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.info = SizedStrData(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.info = SizedStrData.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		SizedStrData.to_stream(stream, instance.info)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'info', SizedStrData, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Header [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* info = {self.fmt_member(self.info, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
