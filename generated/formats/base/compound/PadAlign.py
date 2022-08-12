
from generated.io import MAX_LEN
from generated.struct import StructBase
from modules.formats.shared import get_padding_size

ZERO = b"\x00"


from generated.formats.base.basic import fmt_member
from generated.struct import StructBase


class PadAlign(StructBase):

	"""
	Grabs 00 bytes only
	"""

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		pass

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)

	def __init__(self, context, arg=0, template=None):
		# template is reference object
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.data = b""

	def read(self, stream):
		self.read_fields(stream, self)

	def write(self, stream):
		self.write_fields(stream, self)

	def get_pad(self, stream):
		distance = stream.tell() - self.template.io_start
		return get_padding_size(distance, alignment=self.arg)

	def __repr__(self):
		return f"{self.data} Size: {len(self.data)}"

	@classmethod
	def read_fields(cls, stream, instance):
		instance.data = stream.read(instance.get_pad(stream))

	@classmethod
	def write_fields(cls, stream, instance):
		instance.data = ZERO * instance.get_pad(stream)
		stream.write(instance.data)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template)
		instance.read(stream)
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.write(stream)
		return instance

