from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.ms2.compounds.Vector3 import Vector3
from generated.formats.ms2.compounds.Vector4 import Vector4


class Bone(BaseStruct):

	"""
	32 bytes
	bones, rot first
	"""

	__name__ = 'Bone'

	_import_path = 'generated.formats.ms2.compounds.Bone'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.loc = Vector3(self.context, 0, None)
		self.scale = 0.0
		self.rot = Vector4(self.context, 0, None)
		self.loc = Vector3(self.context, 0, None)
		self.scale = 0.0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		if self.context.version <= 47:
			self.loc = Vector3(self.context, 0, None)
			self.scale = 0.0
			self.rot = Vector4(self.context, 0, None)
		if self.context.version >= 48:
			self.rot = Vector4(self.context, 0, None)
			self.loc = Vector3(self.context, 0, None)
			self.scale = 0.0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		if instance.context.version <= 47:
			instance.loc = Vector3.from_stream(stream, instance.context, 0, None)
			instance.scale = Float.from_stream(stream, instance.context, 0, None)
			instance.rot = Vector4.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 48:
			instance.rot = Vector4.from_stream(stream, instance.context, 0, None)
			instance.loc = Vector3.from_stream(stream, instance.context, 0, None)
			instance.scale = Float.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.context.version <= 47:
			Vector3.to_stream(stream, instance.loc)
			Float.to_stream(stream, instance.scale)
			Vector4.to_stream(stream, instance.rot)
		if instance.context.version >= 48:
			Vector4.to_stream(stream, instance.rot)
			Vector3.to_stream(stream, instance.loc)
			Float.to_stream(stream, instance.scale)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version <= 47:
			yield 'loc', Vector3, (0, None), (False, None)
			yield 'scale', Float, (0, None), (False, None)
			yield 'rot', Vector4, (0, None), (False, None)
		if instance.context.version >= 48:
			yield 'rot', Vector4, (0, None), (False, None)
			yield 'loc', Vector3, (0, None), (False, None)
			yield 'scale', Float, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Bone [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def set_bone(self, matrix):
		pos, quat, sca = matrix.decompose()
		self.loc.x, self.loc.y, self.loc.z = pos.x, pos.y, pos.z
		self.rot.x, self.rot.y, self.rot.z, self.rot.w = quat.x, quat.y, quat.z, quat.w
		self.scale = sca.x

