# START_GLOBALS
import logging
import traceback

from generated.context import ContextReference
from generated.formats.ms2.versions import is_old
from generated.formats.ms2.compound.Model import Model
from generated.formats.ms2.compound.BoneInfo import BoneInfo
from generated.formats.ms2.enum.CollisionType import CollisionType
from modules.formats.shared import get_padding_size, get_padding


# END_GLOBALS


class ModelReader:

	context = ContextReference()

	# START_CLASS

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.bone_infos = []
		if set_default:
			self.set_defaults()
		self.bone_info_start = 0

	def set_defaults(self):
		pass

	@classmethod
	def read_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		instance.bone_infos = []
		i = 0
		if instance.context.version < 47:
			#
			# start = instance.io_start
			start = instance.arg.io_start
			# meh, add it here even though it's really interleaved
			instance.bone_info_start = stream.tell()
			for model_info in instance.arg:
				# logging.debug(model_info)
				model_info.model = Model(instance.context, model_info)
				if model_info.num_objects:
					# instance.get_padding(stream, alignment=8) # 21346
					# instance.get_padding(stream)
					model_info.model.read(stream)
				# logging.debug(model_info.model)
				# alignment, not sure if really correct
				if model_info.increment_flag:
					model_info.model_padding = stream.read(get_padding_size(stream.tell() - start, alignment=16))
				else:
					model_info.model_padding = stream.read(get_padding_size(stream.tell() - start, alignment=8))
				# logging.debug(f"model padding {model_info.model_padding}")
				i = instance.assign_bone_info(i, model_info, stream)

		else:
			for model_info in instance.arg:
				# logging.debug(model_info)
				model_info.model = Model(instance.context, model_info)
				if model_info.num_objects:
					model_info.model.read(stream)
					# logging.debug(model_info.model)
			instance.bone_info_start = stream.tell()
			for model_info in instance.arg:
				try:
					i = instance.assign_bone_info(i, model_info, stream)
				except:
					raise AttributeError(f"Bone info {i} failed")
		instance.io_size = stream.tell() - instance.io_start

	def assign_bone_info(self, i, model_info, stream):
		if model_info.increment_flag:
			logging.debug(f"Reading bone info")
			model_info.bone_info = self.read_bone_info(stream, i)
			# logging.debug(model_info.bone_info)
			self.bone_infos.append(model_info.bone_info)
			i += 1
		else:
			logging.debug(f"Using previous bone info")
			if self.bone_infos:
				model_info.bone_info = self.bone_infos[-1]
			else:
				model_info.bone_info = None
		return i

	def get_hitchecks(self, bone_info):
		# collect all hitchecks in a flat list
		h = [hitcheck for joint in bone_info.joints.joint_infos for hitcheck in joint.hitchecks]
		return h

	def read_bone_info(self, stream, i):

		logging.debug(f"BONE INFO {i} starts at {stream.tell()}")
		# there's never padding before the first bone info, and after the last
		# if not is_old(self.context) and i == 0:
		if (not is_old(self.context)) and i:
			self.get_padding(stream)
		bone_info = BoneInfo(self.context)
		bone_info.read(stream)
		# logging.debug(bone_info)
		self.read_hitcheck_verts(bone_info, stream)
		logging.debug(f"end of bone info {i} at {stream.tell()}")

		# if bone_info.joints and is_old(self):
		# 	names_l = bone_info.joints.namespace_length
		# 	pad_l = len(bone_info.joints.joint_names_padding.data)
		# 	hits = sum(j.hitcheck_count for j in bone_info.joints.joint_infos_old)
		# 	logging.debug(f"names total len: {names_l + pad_l} names: {names_l} padding: {pad_l} hits: {hits} joints: {bone_info.joints.joint_count}")
		# 	if bone_info.joints.joint_infos_old:
		# 		j = bone_info.joints.joint_infos_old[0]
		# 		h = j.hitchecks[0]
		# 		for t, size in enumerate(
		# 				(h.io_start - self.buffer_1_offset,
		# 				h.io_start - bone_info.io_start,
		# 				h.io_start - bone_info.joints.io_start)
		# 			):
		# 			# any of those may not actually be padding
		# 			for sub in (range(pad_l)):
		# 				rel_size = size-sub
		# 				for al in (32, 40, 48, 64):
		# 					mod = rel_size % al
		# 					# logging.debug(f"rel_size: {rel_size} mod{al}: {mod}")
		# 					k = (t, sub, al)
		# 					# see if it modulos to 0
		# 					if not mod:
		# 						if k not in self.dic:
		# 							self.dic[k] = 0
		# 						self.dic[k] += 1
		return bone_info

	def get_padding(self, stream, alignment=16):
		abs_offset = stream.tell()
		relative_offset = abs_offset - self.bone_info_start
		# currently no other way to predict the padding, no correlation to joint count
		padding_len = get_padding_size(relative_offset, alignment=alignment)
		padding = stream.read(padding_len)
		if padding != b'\x00' * padding_len:
			logging.warning(f"Padding is nonzero {padding} at offset {abs_offset}")
		logging.debug(f"padding: {padding_len} aligned to {alignment}")

	def read_hitcheck_verts(self, bone_info, stream):
		logging.debug(f"Reading additional hitcheck data")
		for hitcheck in self.get_hitchecks(bone_info):
			if hitcheck.type in (CollisionType.ConvexHullPC, CollisionType.ConvexHull):
				logging.debug(f"Reading vertices for {hitcheck.type}")
				hitcheck.collider.vertices = stream.read_floats((hitcheck.collider.vertex_count, 3))

	def write_hitcheck_verts(self, bone_info, stream):
		logging.debug(f"Writing additional hitcheck data")
		for hitcheck in self.get_hitchecks(bone_info):
			if hitcheck.type in (CollisionType.ConvexHullPC, CollisionType.ConvexHull):
				logging.debug(f"Writing vertices for {hitcheck.type}")
				stream.write_floats(hitcheck.collider.vertices)

	@classmethod
	def write_fields(cls, stream, instance):
		instance.io_start = stream.tell()
		i = 0
		if instance.context.version < 47:
			raise NotImplementedError("Can't write old style mesh and bone info blocks")
		else:
			for model_info in instance.arg:
				model_info.model.write(stream)
			instance.bone_info_start = stream.tell()
			for model_info in instance.arg:
				if model_info.increment_flag:
					logging.debug(f"BONE INFO {i} starts at {stream.tell()}")
					model_info.bone_info.write(stream)
					instance.write_hitcheck_verts(model_info.bone_info, stream)
					if i + 1 < len(instance.bone_infos):
						relative_offset = stream.tell() - instance.bone_info_start
						padding = get_padding(relative_offset)
						logging.debug(f"Writing padding {padding}")
						stream.write(padding)
					i += 1
			instance.bone_info_size = stream.tell() - instance.bone_info_start
		instance.io_size = stream.tell() - instance.io_start

	def get_info_str(self):
		return f'Model [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		for model_info in self.arg:
			s += str(model_info.model)
			s += str(model_info.bone_info)
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
