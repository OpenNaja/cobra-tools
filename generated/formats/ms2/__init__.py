import os
import itertools
import struct
import io
import time
import traceback

from generated.array import Array
from generated.formats.ms2.compound.JointData import JointData
from generated.formats.ms2.compound.JointData import JointData
from generated.formats.ms2.compound.Ms2InfoHeader import Ms2InfoHeader
from generated.formats.ms2.compound.Mdl2InfoHeader import Mdl2InfoHeader
from generated.formats.ms2.compound.Ms2BoneInfo import Ms2BoneInfo
from generated.formats.ms2.compound.Ms2BoneInfoPc import Ms2BoneInfoPc
from generated.formats.ms2.compound.PcModel import PcModel
from generated.formats.ms2.compound.PcBuffer1 import PcBuffer1
from generated.formats.ms2.enum.CollisionType import CollisionType
from generated.formats.ovl.versions import *
from generated.formats.ms2.versions import *
from generated.io import IoFile, BinaryStream
from modules import walker
from modules.formats.shared import get_padding_size, assign_versions, get_versions


def findall(p, s):
	'''Yields all the positions of
	the pattern p in the string s.'''
	i = s.find(p)
	while i != -1:
		yield i
		i = s.find(p, i + 1)


def findall_diff(s, p0, p1):
	'''Yields all the positions of
	the pattern p in the string s.'''
	i = s.find(p0)
	while i != -1:
		if s[i + 20:i + 24] == p1:
			yield i
		i = s.find(p0, i + 1)


class Ms2File(Ms2InfoHeader, IoFile):

	def __init__(self, ):
		super().__init__()

	def read_all_bone_infos(self, stream, bone_info_cls):
		# functional for JWE detailobjects.ms2, if joint_data is read
		potential_start = stream.tell()
		print("mdl2 count", self.general_info.mdl_2_count)
		for i in range(self.general_info.mdl_2_count):
			print(f"BONE INFO {i} starts at {stream.tell()}")
			try:
				bone_info = bone_info_cls()
				bone_info.read(stream)
				# print(bone_info)
				print("end of bone info at", stream.tell())
				# last one has no padding, so stop here
				if stream.tell() >= potential_start + self.bone_info_size:
					print(f"Exhausted bone info buffer at {stream.tell()}")
					break
				relative_offset = stream.tell() - potential_start
				# currently no other way to predict the padding, no correlation to joint count
				padding_len = get_padding_size(relative_offset)
				# k = None
				# if bone_info.joint_count:
				# 	k = bone_info.joint_datas.joint_count
				print("padding", padding_len, stream.read(padding_len), "joint count", bone_info.joint_count)
			except Exception as err:
				traceback.print_exc()
				print("Bone info failed")
		stream.seek(potential_start)

	def get_bone_info(self, mdl2_index, stream, bone_info_cls, hack=True):
		bone_info = None
		potential_start = stream.tell()
		print("Start looking for bone info at", potential_start)
		if hack:
			# self.read_all_bone_infos(stream, bone_info_cls)
			# first get all bytes of the whole bone infos block
			self.bone_info_bytes = stream.read(self.bone_info_size)
			# find the start of each using this identifier
			zero_f = bytes.fromhex("00 00 00 00")
			one_f = bytes.fromhex("00 00 80 3F")
			# prefixes = (zero_f, one_f)
			prefixes = (zero_f,)
			# lion has a 1 instead of a 4
			bone_info_marker_1 = bytes.fromhex("FF FF 00 00 00 00 00 00 01")
			# this alone is not picky enough for mod_f_wl_unq_laboratory_corner_002_dst
			bone_info_marker_4 = bytes.fromhex("FF FF 00 00 00 00 00 00 04")
			# bone_info_marker =   bytes.fromhex("00 00 00 00 00 00 00 00 01")
			# bone_info_markerb =   bytes.fromhex("00 00 00 00 00 00 00 00 04")
			suffixes = (bone_info_marker_1, bone_info_marker_4,)
			# there's 8 bytes before this
			bone_info_starts = []
			for prefix in prefixes:
				for suffix in suffixes:
					bone_info_starts.extend(x - 4 for x in findall(prefix + suffix, self.bone_info_bytes))

			bone_info_starts = list(sorted(set(bone_info_starts)))
			print("bone_info_starts", bone_info_starts)

			if bone_info_starts:
				idx = mdl2_index
				if idx >= len(bone_info_starts):
					print("reset boneinfo index")
					idx = 0
				bone_info_address = potential_start + bone_info_starts[idx]
				print(f"using bone info {idx} of {len(bone_info_starts)} at address {bone_info_address}")
				stream.seek(bone_info_address)
			else:
				print("No bone info found")
		try:
			bone_info = bone_info_cls()
			bone_info.read(stream)
			for hitcheck in bone_info.joints.hitchecks_pc:
				if hitcheck.type == CollisionType.ConvexHull:
					hitcheck.collider.verts = stream.read_floats((hitcheck.collider.vertex_count, 3))
					print(hitcheck.collider.verts)
			# print(bone_info)
			end_of_bone_info = stream.tell()
			print("end of bone info at", end_of_bone_info)
		except Exception as err:
			traceback.print_exc()
			print("Bone info failed")
		if bone_info:
			try:
				self.bone_names = [self.names[i] for i in bone_info.name_indices]
			except:
				self.bone_names = []
				print("Names failed...")
			try:
				self.read_joints(bone_info)
			except:
				pass
		print(self.bone_names)
		return bone_info

	def read_joints(self, bone_info):

		for i, x in enumerate(bone_info.struct_7.unknown_list):
			print(i)
			print(self.bone_names[x.child], x.child)
			print(self.bone_names[x.parent], x.parent)
			assert x.zero == 0
			assert x.one == 1
		assert bone_info.one == 1
		assert bone_info.name_count == bone_info.bind_matrix_count == bone_info.bone_count == bone_info.bone_parents_count == bone_info.enum_count
		assert bone_info.zeros_count == 0 or bone_info.zeros_count == bone_info.name_count
		assert bone_info.unk_78_count == 0 and bone_info.unknown_88 == 0 and bone_info.unknownextra == 0
		joints = bone_info.joints
		for joint_info in joints.joint_info_list:
			joint_info.name = joints.joint_names.get_str_at(joint_info.name_offset)
			for hit in joint_info.hit_check:
				hit.name = joints.joint_names.get_str_at(hit.name_offset)
		# print(joints)

		for ix, li in enumerate((joints.first_list, joints.short_list, joints.long_list)):
			print(f"List {ix}")
			for i, x in enumerate(li):
				print(i)
				print(joints.joint_info_list[x.parent].name, x.parent)
				print(joints.joint_info_list[x.child].name, x.child)

		# if bone_info.joint_count:
		# 	for i, joint_info in zip(joints.joint_indices, joints.joint_info_list):
		# 		usually, this corresponds - does not do for speedtree but does not matter
		# 		if not self.bone_names[i] == joint_info.name:
		# 			print("WARNING NAMES DON'T MATCH", self.bone_names[i], joint_info.name)
		# if bone_info.joint_count:
		# 	for i, bone_name in zip(joints.bone_indices, self.bone_names):
		# 		print(i, bone_name)
		# 		if i > -1:
		# 			print(joints.joint_info_list[i].name)

	def load(self, filepath, mdl2, quick=False, map_bytes=False, read_bytes=False):
		start_time = time.time()
		# eof = super().load(filepath)

		# extra stuff
		self.bone_info = None
		with self.reader(filepath) as stream:
			self.read(stream)
			# buffer 0 (hashes and names) has been read by the header
			# so eoh = start of buffer 1
			self.eoh = stream.tell()
			print(self)
			print("end of header: ", self.eoh)
			if is_old(self):
				self.pc_buffer1 = stream.read_type(PcBuffer1, (self.general_info,))
				print(self.pc_buffer1)
				for i, model_info in enumerate(self.pc_buffer1.model_infos):
					print("\n\nMDL2", i)
					# print(model_info)
					model_info.pc_model = stream.read_type(PcModel, (model_info,))
					print(model_info.pc_model)
					if is_pc(self):
						model_info.pc_model_padding = stream.read(get_padding_size(stream.tell() - self.eoh))
					# try:
					# 	self.bone_info = stream.read_type(Ms2BoneInfo)
					# except Exception as err:
					# 	print("BONE INFO FAILED", err)
					self.bone_info = self.get_bone_info(0, stream, Ms2BoneInfo, hack=False)
					# print(self.bone_info)
					if i == mdl2.index:
						break
			else:
				self.bone_info = self.get_bone_info(mdl2.bone_info_index, stream, Ms2BoneInfo)

		# numpy chokes on bytes io objects
		with open(filepath, "rb") as stream:
			stream.seek(self.eoh + self.bone_info_size)
			# get the starting position of buffer #2, vertex & face array
			self.start_buffer2 = stream.tell()
			print("self.start_buffer2", self.start_buffer2)
			if is_ztuac(self):
				pass
			elif is_pc(self):
				print("PC model...")
				mdl2.models = Array()
				if not quick:
					# for model in self.pc_buffer1.model_infos:
					for model_data in model_info.pc_model.model_data:
						model_data.populate(self, stream, self.start_buffer2, self.bone_names, 512)
						mdl2.models.append(model_data)
					self.lookup_material(model_info.pc_model, mdl2.models)
			else:
				print("vert array start", self.start_buffer2)
				print("tri array start", self.start_buffer2 + self.buffer_info.vertexdatasize)

				if not quick:
					for model in mdl2.models:
						model.populate(self, stream, self.start_buffer2, self.bone_names, mdl2.model_info.pack_offset)

				if map_bytes:
					for model in mdl2.models:
						model.read_bytes_map(self.start_buffer2, stream)

				# store binary data for verts and tris on the model
				if read_bytes:
					for model in mdl2.models:
						model.read_bytes(self.start_buffer2, self.buffer_info.vertexdatasize, stream)

	def lookup_material(self, mdl2, models):
		for mat_1 in mdl2.materials_1:
			try:
				name = self.names[mdl2.materials_0[mat_1.material_index]]
				model = models[mat_1.model_index]
				model.material = name
			except:
				print(f"Couldn't match material {mat_1.material_index} to model {mat_1.model_index} - bug?")

	def save(self, filepath, mdl2):
		print("Writing verts and tris to temporary buffer")
		# write each model's vert & tri block to a temporary buffer
		temp_vert_writer = io.BytesIO()
		temp_tris_writer = io.BytesIO()
		vert_offset = 0
		tris_offset = 0

		with BinaryStream() as temp_bone_writer:
			assign_versions(temp_bone_writer, get_versions(self))
			temp_bone_writer.ms_2_version = self.general_info.ms_2_version
			self.bone_info.write(temp_bone_writer)
			bone_bytes = temp_bone_writer.getvalue()

		with open(filepath + "bonedump", "wb") as f:
			f.write(bone_bytes)

		for i, model in enumerate(mdl2.models):
			model.write_verts(temp_vert_writer)
			model.write_tris(temp_tris_writer)
			print("vert_offset", vert_offset)
			print("tris_offset", tris_offset)

			# update ModelData struct
			model.vertex_offset = vert_offset
			model.tri_offset = tris_offset
			model.vertex_count = len(model.verts)
			model.tri_index_count = len(model.tri_indices)

			# offsets for the next model
			vert_offset = temp_vert_writer.tell()
			tris_offset = temp_tris_writer.tell()

		# update lod fragment
		print("update lod fragment")
		for lod in mdl2.lods:
			# print(lod)
			lod_models = tuple(
				model for model in mdl2.models[lod.first_model_index:lod.last_model_index])
			# print(lod_models)
			lod.vertex_count = sum(model.vertex_count for model in lod_models)
			lod.tri_index_count = sum(model.tri_index_count for model in lod_models)
			print("lod.vertex_count", lod.vertex_count)
			print("lod.tri_index_count", lod.tri_index_count)
		print("Writing final output")
		# get original header and buffers 0 & 1

		# get bytes from IO object
		vert_bytes = temp_vert_writer.getvalue()
		tris_bytes = temp_tris_writer.getvalue()
		# modify buffer size
		self.buffer_info.vertexdatasize = len(vert_bytes)
		self.buffer_info.facesdatasize = len(tris_bytes)

		# write output ms2
		with self.writer(filepath) as f:
			self.write(f)
			print("new bone info length: ", len(bone_bytes))
			print("old bone info length: ", len(self.bone_info_bytes))
			# this is a hack
			if len(bone_bytes) < len(self.bone_info_bytes):
				f.write(bone_bytes)
				f.write(self.bone_info_bytes[len(bone_bytes):])
			elif len(bone_bytes) > len(self.bone_info_bytes):
				f.write(bone_bytes[:len(self.bone_info_bytes)])
			else:
				f.write(bone_bytes)
			f.write(vert_bytes)
			f.write(tris_bytes)


class Mdl2File(Mdl2InfoHeader, IoFile):

	def __init__(self, ):
		super().__init__()

	def load(self, filepath, quick=False, map_bytes=False, read_bytes=False):
		start_time = time.time()
		self.file = filepath
		self.dir, self.basename = os.path.split(filepath)
		self.file_no_ext = os.path.splitext(self.file)[0]
		print(f"Loading {self.basename}")
		# read the file
		eof = super().load(filepath)
		# print(self)

		self.ms2_path = os.path.join(self.dir, self.name)
		self.ms2_file = Ms2File()
		self.ms2_file.load(self.ms2_path, self, quick=quick, map_bytes=map_bytes, read_bytes=read_bytes)

		# set material links
		self.ms2_file.lookup_material(self, self.models)
		print(f"Finished reading in {time.time() - start_time:.2f} seconds!")

	def save(self, filepath):
		exp = "export"
		exp_dir = os.path.join(self.dir, exp)
		os.makedirs(exp_dir, exist_ok=True)

		mdl2_name = os.path.basename(filepath)

		# create name of output ms2
		new_ms2_name = mdl2_name.rsplit(".", 1)[0] + ".ms2"
		ms2_path = os.path.join(exp_dir, new_ms2_name)
		self.ms2_file.save(ms2_path, self)
		# set new ms2 name to mdl2 header
		self.name = new_ms2_name

		# write final mdl2
		mdl2_path = os.path.join(exp_dir, mdl2_name)
		eof = super().save(mdl2_path)


if __name__ == "__main__":
	m = Mdl2File()
	m.load("C:/Users/arnfi/Desktop/ele/africanelephant_child.mdl2")
	# m.load("C:/Users/arnfi/Desktop/ostrich/ugcres.mdl2")
	# m.load("C:/Users/arnfi/Desktop/ostrich/ugcres_hitcheck.mdl2")
	# m.load("C:/Users/arnfi/Desktop/anubis/cc_anubis_carf.mdl2")
	# m.load("C:/Users/arnfi/Desktop/anubis/cc_anubis_bogfl.mdl2")
	# m.load("C:/Users/arnfi/Desktop/anubis/cc_anubis_carf_hitcheck.mdl2")
	# m.load("C:/Users/arnfi/Desktop/gharial/gharial_male.mdl2")
	# m = Mdl2File()
	# # m.load("C:/Users/arnfi/Desktop/prim/models.ms2")
	# print(m)
	#
	# idir = "C:/Users/arnfi/Desktop/out"
	# # idir = "C:/Users/arnfi/Desktop/Coding/ovl/export_save/detailobjects"
	# dic = {}
	# name = "nat_grassdune_02.mdl2"
	# name = "nat_groundcover_searocket_patchy_01.mdl2"
	# indices = []
	#
	# for fp in walker.walk_type(idir, "mdl2"):
	# 	if "hitcheck" in fp or "skeleton" in fp or "airliftstraps" in fp:
	# 		continue
	# 	print(fp)
	# 	m.load(fp, quick=True)
# 	# indices.append(m.index)
# 	print(fp)
# 	# print(list(lod.bone_index for lod in m.lods))
# 	# print(m.model_info)
# 	# lod_indices = list(lod.bone_index for lod in m.lods)
# 	flags = list(mo.flag for mo in m.models)
# 	print(flags)
# 	# indices.extend(unk)
# # 		dic[file] = lod_indices
# # 		if file.lower() == name:
# # 			print(m.ms2_file.bone_info)
# # 		# print(m.ms2_file.bone_info)
# # 		print(m.ms2_file.bone_info.name_indices, lod_indices)
# # 		lod_names = [m.ms2_file.bone_names[i-1] for i in lod_indices]
# # 		print(lod_names)
# # print(dic)
# # # print(m.ms2_file.names)
# # for i, n in enumerate(m.ms2_file.names):
# # 	print(i,n)
# # l = dic[name]
# # print(l)
# # print(indices, max(indices))
# # fp = os.path.join(idir, name)
# # m.load(fp, quick=True)
#
# print(set(indices))
