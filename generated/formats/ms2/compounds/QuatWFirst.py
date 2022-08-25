from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float


class QuatWFirst(BaseStruct):

	__name__ = 'QuatWFirst'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.w = 1.0
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.w = 1.0
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.w = Float.from_stream(stream, instance.context, 0, None)
		instance.x = Float.from_stream(stream, instance.context, 0, None)
		instance.y = Float.from_stream(stream, instance.context, 0, None)
		instance.z = Float.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Float.to_stream(stream, instance.w)
		Float.to_stream(stream, instance.x)
		Float.to_stream(stream, instance.y)
		Float.to_stream(stream, instance.z)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'w', Float, (0, None), (False, 1.0)
		yield 'x', Float, (0, None), (False, 0.0)
		yield 'y', Float, (0, None), (False, 0.0)
		yield 'z', Float, (0, None), (False, 0.0)

	def __repr__(self):
		return f"[ {self.x:6.3f} {self.y:6.3f} {self.z:6.3f} {self.w:6.3f} ]"

