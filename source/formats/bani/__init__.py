import math

from generated.array import Array
from generated.formats.bani.structs.BaniGpuAnimHeader import BaniGpuAnimHeader
from generated.formats.bani.structs.BaniGpuChannelBones import BaniGpuChannelBones
from generated.formats.bani.structs.BaniGpuChannels import BaniGpuChannels
from generated.formats.bani.structs.BaniGpuChannelsLod import BaniGpuChannelsLod
from generated.formats.bani.structs.BaniGpuChannelsLod256 import BaniGpuChannelsLod256
from generated.formats.bani.structs.BanisInfoHeader import BanisInfoHeader
from generated.formats.base.structs.Blob import Blob
from generated.io import IoFile
import os
import logging

import numpy as np


class BanisFile(BanisInfoHeader, IoFile):
	QUAT_SCALE = 0.00004315927
	QUAT_BIAS = 0.7071067

	dt_packed = np.dtype([
		("quats", np.uint16, (3,)),
		("locs", np.uint16, (3,)),
	])

	dt_float = np.dtype([
		("quat", np.float32, (4,)),
		("loc", np.float32, (3,)),
	])

	def __init__(self):
		super().__init__(self)

	def decompress_keyframes(self, packed_keys, quantization_info):
		"""Applies the Smallest-3 decompression, de-quantization"""
		quats = packed_keys["quats"]
		locs = packed_keys["locs"]
		c0 = quats[:, :, 0] & 0x7FFF
		c1 = quats[:, :, 1] & 0x7FFF
		c2 = quats[:, :, 2] & 0x7FFF

		# Remap [0, 32767] to [-0.7071067, 0.7071067]
		v0 = c0 * self.QUAT_SCALE - self.QUAT_BIAS
		v1 = c1 * self.QUAT_SCALE - self.QUAT_BIAS
		v2 = c2 * self.QUAT_SCALE - self.QUAT_BIAS
		
		sq_sum = v0**2 + v1**2 + v2**2
		w = np.sqrt(np.clip(1.0 - sq_sum, 0.0, 1.0))
		
		drop_idx = ((quats[:, :, 0] >> 14) & 2) | ((quats[:, :, 1] >> 15) & 1)
		
		quats = np.empty(quats.shape[:-1] + (4,), dtype=np.float32)
		# where is faster than stacking masked arrays and take_along_axis
		# drop_idx refers to Frontier's XYZW quaternion, but we already change it to blender's WXYZ order here
		quats[..., 0] = np.where(drop_idx == 3, w, v2)
		quats[..., 1] = np.where(drop_idx == 0, w, v0)
		quats[..., 2] = np.where(drop_idx == 1, w, np.where(drop_idx == 0, v0, v1))
		quats[..., 3] = np.where(drop_idx == 2, w, np.where(drop_idx == 3, v2, v1))
		# Force invalid padding bytes to be clean Identity Quaternions
		quats[sq_sum > 1.0] = [1.0, 0.0, 0.0, 0.0]

		# De-quantize translation
		loc_game = locs.astype(np.float32)
		loc_game = (loc_game * quantization_info.scale) + quantization_info.bias
		return quats, loc_game

	def compress_keyframes(self, quats, loc_game, quantization_info):
		"""Reverses the Smallest-3 decompression and quantization
		Pack into the final uint16 structured array"""

		packed_keys = np.empty(quats.shape[:2], dtype=BanisFile.dt_packed)
		# Ensure quaternions are valid and normalized
		quats = np.asarray(quats, dtype=np.float32)
		norms = np.linalg.norm(quats, axis=-1, keepdims=True)
		norms[norms == 0] = 1.0  # Prevent div by zero
		quats = quats / norms

		# Find the largest absolute component
		max_idx = np.argmax(np.abs(quats), axis=-1)

		# The decompression mathematically assumes the dropped component is positive.
		# If our dropped component is negative, we must invert the entire quaternion 
		# which represents the exact same 3D rotation.
		max_vals = np.take_along_axis(quats, max_idx[..., np.newaxis], axis=-1)[..., 0]
		quats = quats * np.where(max_vals < 0, -1.0, 1.0)[..., np.newaxis]

		# Map the dropped component to the engine's 2-bit 'drop_idx'
		# (max_idx 1->0, max_idx 2->1, max_idx 3->2, max_idx 0->3)
		drop_idx = (max_idx - 1) % 4

		# Extract the remaining 3 components to compress
		v0 = np.empty_like(quats[..., 0])
		v1 = np.empty_like(quats[..., 0])
		v2 = np.empty_like(quats[..., 0])

		m0 = (drop_idx == 0); v0[m0], v1[m0], v2[m0] = quats[m0, 2], quats[m0, 3], quats[m0, 0]
		m1 = (drop_idx == 1); v0[m1], v1[m1], v2[m1] = quats[m1, 1], quats[m1, 3], quats[m1, 0]
		m2 = (drop_idx == 2); v0[m2], v1[m2], v2[m2] = quats[m2, 1], quats[m2, 2], quats[m2, 0]
		m3 = (drop_idx == 3); v0[m3], v1[m3], v2[m3] = quats[m3, 1], quats[m3, 2], quats[m3, 3]

		# Quantize the components back to [0, 32767] space
		c0 = np.clip(np.round((v0 + self.QUAT_BIAS) / self.QUAT_SCALE), 0, 32767).astype(np.uint16)
		c1 = np.clip(np.round((v1 + self.QUAT_BIAS) / self.QUAT_SCALE), 0, 32767).astype(np.uint16)
		c2 = np.clip(np.round((v2 + self.QUAT_BIAS) / self.QUAT_SCALE), 0, 32767).astype(np.uint16)

		# Pack the 2-bit drop_idx into the MSBs (bit 15) of c0 and c1
		# drop_idx bit 1 goes to c0; drop_idx bit 0 goes to c1
		c0_packed = c0 | ((drop_idx >> 1) << 15).astype(np.uint16)
		c1_packed = c1 | ((drop_idx & 1) << 15).astype(np.uint16)
		c2_packed = c2

		packed_keys["quats"] = np.stack((c0_packed, c1_packed, c2_packed), axis=-1)

		# Calculate translation scale and bias to spread range across 0 - 65535
		self.set_quantization_params(loc_game, quantization_info)
		# Compress translation
		if quantization_info.scale > 1e-8:
			loc_raw_float = (loc_game - quantization_info.bias) / quantization_info.scale
		else:
			loc_raw_float = np.zeros_like(loc_game)
		
		packed_keys["locs"] = np.clip(np.round(loc_raw_float), 0, 65535).astype(np.uint16)
		return packed_keys

	def load(self, filepath):
		self.file = filepath
		self.dir, self.basename = os.path.split(filepath)
		self.path_no_ext = os.path.splitext(self.file)[0]

		with open(filepath, "rb") as stream:
			# Read standard headers
			self.read_fields(stream, self)

			is_pc2 = self.context.version >= 7

			if is_pc2:
				pos_after_header = stream.tell()
				metadata_gap_size = self.data.gpu_anim_headers_size + self.data.channel_bones_size + self.data.channel_bones_lod_size
				keys_start_pos = pos_after_header + metadata_gap_size
				
				logging.debug("FILE ALIGNMENT DIAGNOSTICS")
				logging.debug(f"  Pos after header   : {pos_after_header}")
				logging.debug(f"  Keys Start Pos     : {keys_start_pos}")
				logging.debug(f"  Header gpu_anim_headers_size     : {self.data.gpu_anim_headers_size}")
				logging.debug(f"  Header channel_bones_size   : {self.data.channel_bones_size}")
				logging.debug(f"  Header channel_bones_lod_size   : {self.data.channel_bones_lod_size}")
				logging.debug(f"  Metadata Gap Size  : {metadata_gap_size}")

				# Read GPU Headers
				self.data.gpu_anim_headers.data = Array.from_stream(stream, self.context, arg=0, template=None, shape=(self.data.bani_count, ), dtype=BaniGpuAnimHeader)
				# for gpu_header_index, gpu_header in enumerate(self.data.gpu_anim_headers.data):
				# 	gpu_header_pos = pos_after_header + (gpu_header_index * 16)
				# 	channels_pos = gpu_header_pos + (gpu_header.packed_offset_bones.bone_channels_offset * 16)
				for bani in sorted(self.anims, key=lambda b: b.data.gpu_header_index):
					bani_header = bani.data
					gpu_header = self.data.gpu_anim_headers.data[bani_header.gpu_header_index]
					assert bani_header.gpu_header_index * self.get_header_alignment() == bani_header.gpu_header_offset
					assert gpu_header.packed_offset_bones.num_bones == bani_header.num_bones
					print(f"gpu_header_index = {bani_header.gpu_header_index}, gpu_header_offset = {bani_header.gpu_header_offset}, num_bones = {bani_header.num_bones}, "
						  f"bone_channels_offset = {gpu_header.packed_offset_bones.bone_channels_offset}, keyframes_offset = {gpu_header.keyframes_offset}")

				self.data.channel_bones.data = Array(self.context, 0, None, (len(self.data.gpu_anim_headers.data),), BaniGpuChannels, set_default=False)
				self.data.channel_bones.data[:] = [BaniGpuChannels.from_stream(stream, self.context, arg) for arg in self.data.gpu_anim_headers.data]

				lod_dtype = BaniGpuChannelsLod if self.data.channel_bones_size == self.data.channel_bones_lod_size else BaniGpuChannelsLod256
				self.data.channel_bones_lod.data = Array(self.context, 0, None, (len(self.data.gpu_anim_headers.data),), lod_dtype, set_default=False)
				self.data.channel_bones_lod.data[:] = [lod_dtype.from_stream(stream, self.context, arg) for arg in self.data.gpu_anim_headers.data]

				assert stream.tell() == keys_start_pos
				self.data.keys.data = Blob(self.context)
				self.data.keys.data.data = self.read_keys_bytes(stream)
				# PC2 keys are read directly from disk below
			else:
				# For older versions, read directly into a structured array
				self.keys_bytes = self.read_keys_bytes(stream)
				all_packed_keys = self.read_packed_keys(stream, self.data.num_frames, self.data.num_bones)

			num_global_bones = self.data.num_bones

			for anim_idx, bani in enumerate(self.anims):
				num_frames = bani.data.num_frames
				self.init_uncompressed_arrays(bani, num_frames, num_global_bones)
				bani.animated_bone_indices = []

				if is_pc2:
					# Use the GPU index stored in the CPU header
					gpu_header_index = bani.data.gpu_header_index
					gpu_header = self.data.gpu_anim_headers.data[gpu_header_index]
					channel_map = self.data.channel_bones.data[gpu_header_index].data

					num_local_bones = gpu_header.packed_offset_bones.num_bones

					# Calculate absolute keys offset using the GPU index
					gpu_header_pos = pos_after_header + (gpu_header_index * 16)
					keys_base_disk_offset = gpu_header_pos + (gpu_header.keyframes_offset * 16)
					# Skip currently unread LOD channels
					keys_base_disk_offset += self.data.channel_bones_lod_size
					keys_pos_absolute = keys_base_disk_offset + (bani.data.read_start_frame * 12)

					# Read keys from disk
					stream.seek(keys_pos_absolute)
					packed_keys = self.read_packed_keys(stream, num_frames, num_local_bones)

					logging.debug(f"\n[DEBUG] --- Animation {anim_idx}: {bani.name} ---")
					logging.debug(f"  Mode : {bani.data.mode}")
					logging.debug(f"  keyframes_offset : {gpu_header.keyframes_offset}")
					logging.debug(f"  read_start_frame : {bani.data.read_start_frame}")
					logging.debug(f"  Local Bones : {num_local_bones}")
					logging.debug(f"  Total Frames: {num_frames}")
					logging.debug(f"  GPU Index:  : {gpu_header_index}")
					logging.debug(f"  Disk Offset : {keys_pos_absolute} to {stream.tell()}")
					# logging.debug(f"  Bone Map    : {channel_map}")

					# Decompress
					quats, locs = self.decompress_keyframes(packed_keys, gpu_header.quantization_info)

					# Read mapping
					bani.read_mapping = {}
					# Map channels to bones
					for local_i, (write_i, read_i) in enumerate(channel_map):
						if write_i < num_global_bones:
							bani.quats[:, write_i] = quats[:, local_i]
							bani.locs[:, write_i] = locs[:, local_i]
							bani.animated_bone_indices.append(write_i)
							bani.read_mapping[write_i] = read_i
				else:
					# Fallback for old titles
					start_frame = bani.data.read_start_frame
					end_frame = start_frame + num_frames
					bani.quats[:], bani.locs[:] = self.decompress_keyframes(all_packed_keys[start_frame:end_frame], self.data.quantization_info)
					bani.animated_bone_indices = list(range(num_global_bones))

	def get_header_alignment(self):
		alignment = int(math.ceil(self.data.num_bones / 16) * 16)
		return alignment

	def read_keys_bytes(self, stream):
		start_of_keys = stream.tell()
		keys_bytes = stream.read()
		stream.seek(start_of_keys)
		return keys_bytes

	def init_uncompressed_arrays(self, bani, num_frames, num_bones):
		# Initialize output array to Identity transforms (for non-animated bones)
		bani.locs = np.zeros((num_frames, num_bones, 3), dtype=np.float32)
		bani.quats = np.zeros((num_frames, num_bones, 4), dtype=np.float32)
		bani.quats[:, :, 0] = 1.0

	def read_packed_keys(self, stream, num_frames, num_bones):
		packed_keys = np.empty(dtype=BanisFile.dt_packed, shape=(num_frames, num_bones))
		# packed_keys = np.empty(dtype=np.uint16, shape=(num_frames, num_bones, 6))
		stream.readinto(packed_keys)
		return packed_keys

	def save(self, filepath):
		# if self.context.version >= 7:
		# 	raise NotImplementedError("Saving Version 7+ banis files is not yet implemented.")

		self.data.bytes_per_bone = self.data.num_bones * self.data.bytes_per_frame
		self.data.num_frames = 0
		frame_offset = 0
		for bani in self.anims:
			self.data.num_frames += bani.data.num_frames
			bani.data.read_start_frame = frame_offset
			frame_offset += bani.data.num_frames
		
		all_packed_keys = []
		if self.context.version < 7:
			# Reassemble the whole array as floats and quantize in one sweep
			quats_all = np.vstack([bani.quats for bani in self.anims])
			locs_all = np.vstack([bani.locs for bani in self.anims])
			packed_keys = self.compress_keyframes(quats_all, locs_all, self.data.quantization_info)
			all_packed_keys.append(packed_keys)
		else:
			# Quantize each bani individually
			bone_channels_offset = len(self.anims)
			for i, (bani, gpu_header, channel_bones, channel_bones_lod) in enumerate(
					zip(
						sorted(self.anims, key=lambda ba: ba.data.gpu_header_index), self.data.gpu_anim_headers.data, self.data.channel_bones.data, self.data.channel_bones_lod.data)):
				packed_keys = self.compress_keyframes(bani.quats, bani.locs, gpu_header.quantization_info)
				all_packed_keys.append(packed_keys)
				bani_header = bani.data
				# bani_header.gpu_header_index = i  # todo - add back in once rest works
				bani_header.gpu_header_offset = bani_header.gpu_header_index * self.get_header_alignment()
				# todo quats is not actually reduced bone count here!
				# gpu_header.packed_offset_bones.num_bones = bani_header.num_bones = bani.quats.shape[1]
				gpu_header.packed_offset_bones.bone_channels_offset = bone_channels_offset
				# outliers in guests
				if bani_header.num_bones in (48, 95):
					bone_channels_offset -= 1
				bone_channels_offset += int(math.ceil(bani_header.num_bones * 2 / 16))
			print("save")

			for i, gpu_header in enumerate(reversed(self.data.gpu_anim_headers.data)):
				gpu_header.keyframes_offset = bone_channels_offset + i + 1

			for bani in sorted(self.anims, key=lambda ba: ba.data.gpu_header_index):
				bani_header = bani.data
				gpu_header = self.data.gpu_anim_headers.data[bani_header.gpu_header_index]
				print(
					f"gpu_header_index = {bani_header.gpu_header_index}, gpu_header_offset = {bani_header.gpu_header_offset}, num_bones = {bani_header.num_bones}, "
					f"bone_channels_offset = {gpu_header.packed_offset_bones.bone_channels_offset}, keyframes_offset = {gpu_header.keyframes_offset}")
			# todo
			# channel_bones =
			# channel_bones_lod =

			self.data.keys_size = sum(len(packed_keys) for packed_keys in all_packed_keys)

		with open(filepath, "wb") as stream:
			# Write headers
			self.write_fields(stream, self)
			# Write quantized keyframe data
			for packed_keys in all_packed_keys:
				stream.write(packed_keys.tobytes())


	@staticmethod
	def set_quantization_params(locs, quantization_info):
		quantization_info.bias = float(np.min(locs))
		loc_max = float(np.max(locs))
		if loc_max - quantization_info.bias > 1e-8:
			quantization_info.scale = (loc_max - quantization_info.bias) / 65535.0
		else:
			quantization_info.scale = 1.0


if __name__ == "__main__":
	b = BanisFile()
	# b.load("C:/Users/arnfi/Desktop/animation.baniset7b77b17d.banis")
	b.load("C:/Users/arnfi/Desktop/GUESTS_af.banisetfc27d51a.banis")
	b.save("C:/Users/arnfi/Desktop/GUESTS_af.banisetfc27d51a222.banis")
	# print(b)