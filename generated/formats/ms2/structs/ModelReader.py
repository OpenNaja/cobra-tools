import logging
from io import BytesIO

from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.structs.PadAlign import get_padding_size, get_padding
from generated.formats.ms2.structs.BufferInfo import BufferInfo
from generated.formats.ms2.structs.ModelInfo import ModelInfo
from generated.formats.ms2.versions import is_pc, is_jwe
from generated.formats.ms2.structs.MeshCollisionData import MeshCollisionData
from generated.formats.ms2.structs.Model import Model
from generated.formats.ms2.structs.BoneInfo import BoneInfo
from generated.formats.ms2.enums.CollisionType import CollisionType
from generated.base_struct import BaseStruct
from generated.formats.ovl_base.structs.SmartPadding import SmartPadding


from generated.base_struct import BaseStruct


class ModelReader(BaseStruct):

	"""
	This reads and assigns models to each model_info that is passed to it
	"""

	__name__ = 'ModelReader'


	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	def __init__(self, context, arg=None, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.bone_infos = []
		self.buffer_1_start = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		pass

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		for name, model_info in zip(instance.arg.mdl_2_names, instance.arg.model_infos):
			model_info.name = name
			model_info.bone_info = None
		instance.bone_infos = []
		logging.debug(f"ModelReader starts at {instance.io_start}")
		i = 0
		specials = []
		if instance.context.version < 47:
			# buffer 1 starts at buffer_infos
			instance.start_of_buffer = instance.arg.buffer_infos.io_start
			instance.buffer_1_start = instance.start_of_buffer
			for model_info in instance.arg.model_infos:
				# DLA and ZTUAC don't go into shifts
				instance.get_padding(stream, alignment=8)
				s = stream.tell()
				logging.debug(f"Model {model_info.name} at {s}")
				# this little patch solves reading all of PC anubis models
				for shift in (0, 16, 12, 8, 4, -4, -8, -12, -16):
					stream.seek(s+shift)
					model_info.shift = shift
					try:
						model_info.model = Model.from_stream(stream, instance.context, model_info)
					except:
						logging.exception(f"Failed reading model for model_info {model_info}")

					if instance.context.version == 32 and model_info.model.lods:
						# logging.debug(f"Model with shifted distance {model_info.model.lods[0]}")
						# janitor 4.0, genie 1600.0, FR_HSwing 14400.0, FR_Sream 25600.0, FR_Victory 3600.0,
						# ST_Stone 4900.0, 2500.0 PR_Kraken, 22500.0+40000 PC_Archway, 10000.0+7225 FR_Orb
						if model_info.model.lods[0].distance in (
								40000.0, 25600.0, 22500.0, 14400.0, 10000.0, 4900.0, 3600.0, 7225.0, 2500.0, 1600.0, 900.0, 4.0):
							if shift:
								logging.debug(f"{model_info.name}: ok at {model_info.model.lods[0].io_start} (shift={shift})")
							break
						else:
							specials.append(i)
							logging.warning(f"{model_info.name}: Distance is wrong at {model_info.model.lods[0].io_start} (shift={shift})")
							# logging.warning(f"Distance is wrong at {model_info.model.lods[0].io_start}")
							# logging.warning(f"last bone info {instance.bone_infos[-1]}")
							# logging.debug(f"Model with original distance {model_info.model.lods[0]}")
					else:
						break

				logging.debug(f"Model {i} ends at {stream.tell()}")
				# logging.debug(f"Model {i} {model_info.model}")
				# alignment, not sure if really correct
				# test for FR_GrandCarousel.ovl
				if model_info.model.io_size == 0 and model_info.increment_flag:
					model_info.model.padding = SmartPadding.from_stream(stream, instance.context)
					# logging.warning(model_info.model)
				i = instance.assign_bone_info(i, model_info, stream)

		else:
			for model_info in instance.arg.model_infos:
				# logging.debug(model_info)
				model_info.model = Model.from_stream(stream, instance.context, model_info)
				# logging.debug(f"Model {i} {model_info.model}")
			instance.buffer_1_start = stream.tell()
			# the models are not part of the buffer
			instance.start_of_buffer = stream.tell()
			for model_info in instance.arg.model_infos:
				try:
					i = instance.assign_bone_info(i, model_info, stream)
				except:
					logging.exception(f"Assigning bone info {i} failed")
					raise
		if specials:
			logging.debug(f"Specials {specials}")
		instance.io_size = stream.tell() - instance.io_start

	def assign_bone_info(self, i, model_info, stream):
		if model_info.increment_flag:
			logging.debug(f"Reading bone info {i} at {stream.tell()}")
			try:
				model_info.bone_info = self.read_bone_info(stream, i)
				model_info.bone_info.name = f"{model_info.name}_armature"
				logging.debug(model_info.bone_info)
				self.bone_infos.append(model_info.bone_info)
			except:
				logging.warning(f"Bone info {i} failed for model_info")
				logging.warning(model_info)
				logging.warning(model_info.model)
				logging.warning(f"here's the bone info before:")
				logging.warning(self.bone_infos[-1])
				raise
			i += 1
		else:
			logging.debug(f"Using previous bone info")
			if self.bone_infos:
				model_info.bone_info = self.bone_infos[-1]
			else:
				model_info.bone_info = None
		return i

	def get_hitchecks(self, bone_info):
		"""Collect all hitchecks in a flat list"""
		# need to handle bone infos that have no joints
		if hasattr(bone_info, "joints") and bone_info.joints:
			h = [hitcheck for joint in bone_info.joints.joint_infos for hitcheck in joint.hitchecks]
			return h
		return []

	def read_bone_info(self, stream, i):
		logging.debug(f"BONE INFO {i} starts at {stream.tell()}")
		# 22-05: in PC anubis, we do have padding here
		self.get_padding(stream)
		bone_info = BoneInfo.from_stream(stream, self.context)
		# logging.info(bone_info)
		self.read_hitcheck_verts(bone_info, stream)
		logging.debug(f"end of bone info {i} at {stream.tell()}")
		return bone_info

	def get_padding(self, stream, alignment=16, rel=None):
		if rel is None:
			rel = self.start_of_buffer
		abs_offset = stream.tell()
		relative_offset = abs_offset - rel
		padding_len = get_padding_size(relative_offset, alignment=alignment)
		# logging.debug(f"abs {abs_offset} rel {relative_offset}")
		logging.debug(f"Aligning to {alignment} from {abs_offset} to {abs_offset+padding_len} ({padding_len} bytes)")
		padding = stream.read(padding_len)
		if padding != b'\x00' * padding_len:
			# logging.warning(f"Padding is nonzero {padding} at offset {abs_offset}")
			raise AttributeError(f"Padding is nonzero {padding} at offset {abs_offset}, expected {padding_len}")

	def align_to(self, stream, alignment=16, rel=None):
		if rel is None:
			rel = self.start_of_buffer
		abs_offset = stream.tell()
		relative_offset = abs_offset - rel
		padding_len = get_padding_size(relative_offset, alignment=alignment)
		logging.debug(f"Aligning to {alignment} from {abs_offset} to {abs_offset+padding_len} ({padding_len} bytes)")
		stream.write(b'\x00' * padding_len)

	def read_hitcheck_verts(self, bone_info, stream):
		try:
			start = stream.tell()
			logging.debug(f"Reading additional hitcheck data at {start}")
			for hitcheck in self.get_hitchecks(bone_info):
				if hitcheck.dtype in (CollisionType.CONVEX_HULL_P_C, CollisionType.CONVEX_HULL):
					if is_pc(self.context):
						# 2023-10-22: there is alignment for PC, notable in CC_riv
						self.get_padding(stream, alignment=16)
					if is_jwe(self.context):
						# 2025-05-16: not sure how accurate this is, but helps PDLC6_BLDG_PowerStationGeo, which is a limited sample
						# perhaps different anchor for alignment compared to PC
						stream.read(8)
					logging.debug(f"Reading vertices for {hitcheck.dtype.name} at {stream.tell()}")
					hitcheck.collider.vertices = Array.from_stream(stream, self.context, 0, None, (hitcheck.collider.vertex_count, 3), Float)
					# logging.debug(f"End of vertices at {stream.tell()}")
				elif hitcheck.dtype in (CollisionType.MESH_COLLISION,):
					self.get_padding(stream, alignment=16)
					logging.debug(f"Reading vertices for {hitcheck.dtype.name} at {stream.tell()}")
					# logging.debug(f"Hitcheck {hitcheck.collider}")
					# logging.debug(f"Hitcheck {hitcheck}")
					hitcheck.collider.data = MeshCollisionData.from_stream(stream, self.context, hitcheck.collider, None)
					# logging.debug(hitcheck.collider.data)
					# logging.debug(f"End of vertices at {stream.tell()}")
		except:
			logging.exception(f"Reading hitchecks failed")

	def write_hitcheck_verts(self, bone_info, stream):
		logging.debug(f"Writing additional hitcheck data")
		for hitcheck in self.get_hitchecks(bone_info):
			if hitcheck.dtype in (CollisionType.CONVEX_HULL_P_C, CollisionType.CONVEX_HULL):
				if is_pc(self.context):
					self.align_to(stream, alignment=16)
				Array.to_stream(hitcheck.collider.vertices, stream, self.context, dtype=Float)
			elif hitcheck.dtype in (CollisionType.MESH_COLLISION,):
				self.align_to(stream, alignment=16)
				MeshCollisionData.to_stream(hitcheck.collider.data, stream, self.context)

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		previous_bone_info = None
		if instance.context.version < 47:
			# buffer 1 starts at buffer_infos
			instance.start_of_buffer = instance.arg.buffer_infos.io_start
			# logging.debug(f"instance.start_of_buffer = {instance.start_of_buffer}")
			# io_start is not valid until buffer_infos + model_infos has been loaded/written
			# this could throw off the padding, especially for more complex models
			# so a dummy dump to ensure that
			b = instance.arg.buffer_infos
			m = instance.arg.model_infos
			with BytesIO() as dummy_stream:
				b.write(dummy_stream)
				m.write(dummy_stream)
			offset_in_buffer_1 = b.io_size + m.io_size
			# logging.debug(f"offset_in_buffer_1 = {offset_in_buffer_1}")
			# meh, add it here even though it's really interleaved
			instance.buffer_1_start = stream.tell() - offset_in_buffer_1
			for model_info in instance.arg.model_infos:
				# DLA and ZTUAC don't go into shifts
				instance.align_to(stream, alignment=8)
				s = stream.tell()
				logging.debug(f"Model {model_info.name} at {s}")
				# write padding or seek back
				if hasattr(model_info, "shift"):
					if model_info.shift > 0:
						stream.write(b"\x00" * model_info.shift)
					elif model_info.shift < 0:
						stream.seek(s+model_info.shift)
				model_info.model.to_stream(model_info.model, stream, instance.context)
				logging.debug(f"Model ends at {stream.tell()}")
				# test for FR_GrandCarousel.ovl
				if model_info.model.io_size == 0 and model_info.increment_flag and hasattr(model_info.model, "padding"):
					SmartPadding.to_stream(model_info.model.padding, stream, instance.context)
				previous_bone_info = cls.write_bone_info(instance, model_info, previous_bone_info, stream)
		else:
			for model_info in instance.arg.model_infos:
				model_info.model.to_stream(model_info.model, stream, instance.context)
			instance.buffer_1_start = stream.tell()
			# the models are not part of the buffer
			instance.start_of_buffer = stream.tell()
			for model_info in instance.arg.model_infos:
				previous_bone_info = cls.write_bone_info(instance, model_info, previous_bone_info, stream)
		# 2024-09-10: PC is definitely not aligned to 16, but 8 if anything
		# instance.align_to(stream, alignment=8)
		instance.align_to(stream, alignment=16)
		instance.bone_info_size = stream.tell() - instance.buffer_1_start
		logging.debug(f"instance.bone_info_size = {instance.bone_info_size}")
		instance.io_size = stream.tell() - instance.io_start

	@classmethod
	def write_bone_info(cls, instance, model_info, previous_bone_info, stream):
		"""check if they have a different bone info"""
		if previous_bone_info is not model_info.bone_info:
			logging.debug(f"{model_info.name} has its own bone_info")
			model_info.increment_flag = 1
			logging.debug(f"BONE INFO starts at {stream.tell()}")
			instance.align_to(stream, alignment=16)
			model_info.bone_info.to_stream(model_info.bone_info, stream, instance.context)
			instance.write_hitcheck_verts(model_info.bone_info, stream)
			logging.debug(f"BONE INFO ends at {stream.tell()}")
			# instance.align_to(stream, alignment=16)
		else:
			logging.debug(f"{model_info.name} reuses previous bone_info")
			model_info.increment_flag = 0
		return model_info.bone_info

	@classmethod
	def get_fields_str(cls, instance, indent=0):
		s = ''
		for model_info in instance.arg.model_infos:
			s += str(model_info.model)
			s += str(model_info.bone_info)
		return s

