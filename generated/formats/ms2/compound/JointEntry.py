from generated.formats.base.basic import fmt_member
from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.Vector3 import Vector3
from generated.struct import StructBase


class JointEntry(StructBase):

	"""
	Describes a joint in armature space.
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# the rotation of the joint, inverted
		self.rot = 0

		# the location of the joint
		self.loc = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.rot = Matrix33(self.context, 0, None)
		self.loc = Vector3(self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.rot = Matrix33.from_stream(stream, instance.context, 0, None)
		instance.loc = Vector3.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Matrix33.to_stream(stream, instance.rot)
		Vector3.to_stream(stream, instance.loc)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('rot', Matrix33, (0, None))
		yield ('loc', Vector3, (0, None))

	def get_info_str(self, indent=0):
		return f'JointEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* rot = {fmt_member(self.rot, indent+1)}'
		s += f'\n	* loc = {fmt_member(self.loc, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
