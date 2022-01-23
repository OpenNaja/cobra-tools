# START_GLOBALS
import logging
import traceback

from generated.context import ContextReference
from generated.formats.ms2.versions import is_old
from generated.formats.ms2.compound.Model import Model
from generated.formats.ms2.compound.BoneInfo import BoneInfo
from generated.formats.ms2.enum.CollisionType import CollisionType
from modules.formats.shared import get_padding_size

# END_GLOBALS


class ModelReader:

	context = ContextReference()

	# START_CLASS

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.bone_infos = []
		self.set_defaults()

	def set_defaults(self):
		pass

	def read(self, stream):
		self.io_start = stream.tell()
		self.bone_infos = []
		for model_info in self.arg:
			logging.debug(model_info)
			model_info.model = Model(self.context, model_info)
			if model_info.num_objects:
				model_info.model.read(stream)
				logging.debug(model_info.model)
		i = 0
		self.bone_info_start = stream.tell()
		for model_info in self.arg:
			if model_info.increment_flag:
				logging.debug(f"Reading bone info")
				model_info.bone_info = self.read_bone_info(stream, i)
				self.bone_infos.append(model_info.bone_info)
				i += 1
			else:
				logging.debug(f"Using previous bone info")
				if self.bone_infos:
					model_info.bone_info = self.bone_infos[-1]
				else:
					model_info.bone_info = None
		self.io_size = stream.tell() - self.io_start

		# todo - implement PC style, with this padding between model and bone_info
		# # alignment is probably wrong
		# if model_info.increment_flag:
		# 	model_info.pc_model_padding = stream.read(get_padding_size(stream.tell() - self.buffer_1_offset, alignment=16))
		# else:
		# 	model_info.pc_model_padding = stream.read(get_padding_size(stream.tell() - self.buffer_1_offset, alignment=8))
		# logging.debug(f"model padding {model_info.pc_model_padding}")

	def get_hitchecks(self, bone_info):
		# collect all hitchecks in a flat list
		h = [hitcheck for joint in bone_info.joints.joint_infos for hitcheck in joint.hitchecks]
		return h

	def read_bone_info(self, stream, i):

		logging.debug(f"BONE INFO {i} starts at {stream.tell()}")
		if i:
			abs_offset = stream.tell()
			relative_offset = abs_offset - self.bone_info_start
			# currently no other way to predict the padding, no correlation to joint count
			padding_len = get_padding_size(relative_offset)
			padding = stream.read(padding_len)
			if padding != b'\x00' * padding_len:
				logging.warning(f"Padding is nonzero {padding} at offset {abs_offset}")
			logging.debug(f"padding: {padding_len}")
		bone_info = BoneInfo(self.context)
		bone_info.read(stream)
		# self.assign_bone_names(bone_info)
		# try:
		# 	self.assign_joints(bone_info)
		# except:
		# 	logging.error(f"Joints {i} failed...")
		# 	traceback.print_exc()
		logging.debug(bone_info)
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

	def write(self, stream):
		self.io_start = stream.tell()

		self.io_size = stream.tell() - self.io_start

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
