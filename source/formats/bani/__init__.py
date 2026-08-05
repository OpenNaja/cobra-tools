from generated.formats.bani.structs.BanisInfoHeader import BanisInfoHeader
from generated.io import IoFile
import os
import struct
import logging

import math
import numpy as np


class BaniContext(object):
	def __init__(self):
		self.version = 0
		self.user_version = 0

	def __repr__(self):
		return f"{self.version} | {self.user_version}"


class BanisFile(BanisInfoHeader, IoFile):

	dt_packed = np.dtype([
		("rot_raw", np.uint16, (3,)),
		("loc_raw", np.uint16, (3,)),
	])

	dt_float = np.dtype([
		("quat", np.float32, (4,)),
		("loc", np.float32, (3,)),
	])

	def __init__(self):
		super().__init__(BaniContext())

	def decompress_keyframes(self, rot_raw, loc_raw, scale, bias):
		"""Applies the Smallest-3 decompression, de-quantization"""
		c0 = rot_raw[:, :, 0] & 0x7FFF
		c1 = rot_raw[:, :, 1] & 0x7FFF
		c2 = rot_raw[:, :, 2] & 0x7FFF

		MAGIC_SCALE = 0.00004315927
		MAGIC_BIAS = 0.7071067

		# Remap [0, 32767] to [-0.7071067, 0.7071067]
		v0 = c0 * MAGIC_SCALE - MAGIC_BIAS
		v1 = c1 * MAGIC_SCALE - MAGIC_BIAS
		v2 = c2 * MAGIC_SCALE - MAGIC_BIAS
		
		sq_sum = v0**2 + v1**2 + v2**2
		w = np.sqrt(np.clip(1.0 - sq_sum, 0.0, 1.0))
		
		drop_idx = ((rot_raw[:, :, 0] >> 14) & 2) | ((rot_raw[:, :, 1] >> 15) & 1)
		
		quats = np.empty(rot_raw.shape[:-1] + (4,), dtype=np.float32)
		m0 = (drop_idx == 0); quats[m0] = np.stack((v2[m0], w[m0], v0[m0], v1[m0]), axis=-1)
		m1 = (drop_idx == 1); quats[m1] = np.stack((v2[m1], v0[m1], w[m1], v1[m1]), axis=-1)
		m2 = (drop_idx == 2); quats[m2] = np.stack((v2[m2], v0[m2], v1[m2], w[m2]), axis=-1)
		m3 = (drop_idx == 3); quats[m3] = np.stack((w[m3], v0[m3], v1[m3], v2[m3]), axis=-1)

		# Force invalid padding bytes to be clean Identity Quaternions
		quats[sq_sum > 1.0] = [1.0, 0.0, 0.0, 0.0]
		
		# De-quantize translation
		loc_game = loc_raw.astype(np.float32)
		loc_game = (loc_game * scale) + bias

		return quats, loc_game

	def compress_keyframes(self, quats, loc_game, scale, bias):
		"""Reverses the Smallest-3 decompression and quantization"""
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
		MAGIC_SCALE = 0.00004315927
		MAGIC_BIAS = 0.7071067
		
		c0 = np.clip(np.round((v0 + MAGIC_BIAS) / MAGIC_SCALE), 0, 32767).astype(np.uint16)
		c1 = np.clip(np.round((v1 + MAGIC_BIAS) / MAGIC_SCALE), 0, 32767).astype(np.uint16)
		c2 = np.clip(np.round((v2 + MAGIC_BIAS) / MAGIC_SCALE), 0, 32767).astype(np.uint16)

		# Pack the 2-bit drop_idx into the MSBs (bit 15) of c0 and c1
		# drop_idx bit 1 goes to c0; drop_idx bit 0 goes to c1
		c0_packed = c0 | ((drop_idx >> 1) << 15).astype(np.uint16)
		c1_packed = c1 | ((drop_idx & 1) << 15).astype(np.uint16)
		c2_packed = c2

		rot_raw = np.stack((c0_packed, c1_packed, c2_packed), axis=-1)

		# Compress translation
		if scale > 1e-8:
			loc_raw_float = (loc_game - bias) / scale
		else:
			loc_raw_float = np.zeros_like(loc_game)
			
		loc_raw = np.clip(np.round(loc_raw_float), 0, 65535).astype(np.uint16)

		return rot_raw, loc_raw

	def load(self, filepath):
		self.file = filepath
		self.dir, self.basename = os.path.split(filepath)
		self.path_no_ext = os.path.splitext(self.file)[0]

		with open(filepath, "rb") as stream:
			# Read standard headers
			self.read_fields(stream, self)

			is_pc2 = self.context.version >= 7
			
			self.parsed_gpu_headers = []
			self.parsed_gpu_channels = []

			if is_pc2:
				# ==========================================
				# FILE ALIGNMENT DIAGNOSTICS
				# ==========================================
				pos_after_header = stream.tell()
				metadata_gap_size = self.data.gpu_anim_headers_size + self.data.channel_bones_size + self.data.channel_bones_lod_size
				keys_start_pos = pos_after_header + metadata_gap_size
				stream.seek(0, os.SEEK_END)
				eof_pos = stream.tell()
				keys_size = self.data.keys_size
				
				logging.debug("\n[DEBUG] --- FILE ALIGNMENT DIAGNOSTICS ---")
				logging.debug(f"  EOF Position       : {eof_pos}")
				logging.debug(f"  Pos after header   : {pos_after_header}")
				logging.debug(f"  Keys Start Pos     : {keys_start_pos}")
				logging.debug(f"  Expected Keys Size : {keys_size}")
				logging.debug(f"  Header gpu_anim_headers_size     : {self.data.gpu_anim_headers_size}")
				logging.debug(f"  Header channel_bones_size   : {self.data.channel_bones_size}")
				logging.debug(f"  Header channel_bones_lod_size   : {self.data.channel_bones_lod_size}")
				logging.debug(f"  Metadata Gap Size  : {metadata_gap_size}")

				# Rewind to header end
				stream.seek(pos_after_header)

				# ==========================================
				# BINARY READING
				# ==========================================
				# Read GPU Headers
				gpu_headers = stream.read(self.data.gpu_anim_headers_size)
				for i in range(self.data.bani_count):
					offset = i * 16
					scale, bias, packed_offset, keyframes_offset = struct.unpack_from("<ffII", gpu_headers, offset)
					
					num_bones = packed_offset >> 24
					relative_channels_chunk = packed_offset & 0x00FFFFFF
					
					current_pos = pos_after_header + offset
					channels_absolute_pos = current_pos + (relative_channels_chunk * 16)
					
					self.parsed_gpu_headers.append({
						"scale": scale,
						"bias": bias,
						"num_bones": num_bones,
						"channels_pos": channels_absolute_pos,
						"keyframes_offset": keyframes_offset
					})
				
				# Read GPU Channels
				for b_data in self.parsed_gpu_headers:
					stream.seek(b_data["channels_pos"])
					num_bones = b_data["num_bones"]
					
					bone_map_bytes = stream.read(num_bones * 2)
					
					bone_map = []
					for b_idx in range(num_bones):
						out_idx, read_idx = struct.unpack_from("<BB", bone_map_bytes, b_idx * 2)
						bone_map.append((out_idx, read_idx))

					self.parsed_gpu_channels.append(bone_map)

				# TODO: Skip LOD Channel for now

				stream.seek(keys_start_pos)
				# PC2 keys are read directly from disk below
			else:
				# For older versions, read directly into a structured array
				keys_packed = np.empty(dtype=BanisFile.dt_packed, shape=(self.data.num_frames, self.data.num_bones))
				stream.readinto(keys_packed)

		global_num_bones = self.data.num_bones

		for anim_idx, bani in enumerate(self.anims):
			num_frames = bani.data.num_frames
			# Parse animation mode
			if is_pc2:
				bani.anim_mode = (bani.data.anim_flags >> 16) & 0xFFFF
			else:
				bani.anim_mode = 5  # Default for older titles

			# Initialize output array to Identity transforms (for non-animated bones)
			bani.keys = np.empty((num_frames, global_num_bones), dtype=BanisFile.dt_float)
			bani.keys["quat"] = [1.0, 0.0, 0.0, 0.0]
			bani.keys["loc"] = [0.0, 0.0, 0.0]
			bani.animated_bone_indices = []

			if is_pc2:
				# Use the GPU index stored in the CPU header
				b_data_idx = bani.data.gpu_buffer_index
				b_data = self.parsed_gpu_headers[b_data_idx]
				b_map = self.parsed_gpu_channels[b_data_idx]
				
				num_local_bones = b_data["num_bones"]
				scale = b_data["scale"]
				bias = b_data["bias"]
				keyframes_offset = b_data["keyframes_offset"]
				# Expose scale and bias to Blender
				bani.scale = scale
				bani.bias = bias
				
				# Calculate absolute keys offset using the corrected GPU index
				current_pos = pos_after_header + (b_data_idx * 16)
				keys_base_disk_offset = current_pos + (keyframes_offset * 16)
				# Skip currently unread LOD channels
				keys_base_disk_offset += self.data.channel_bones_lod_size
				keys_pos_absolute = int(keys_base_disk_offset + (bani.data.read_start_frame * 12))
				
				# Read keys from disk
				with open(self.file, "rb") as f:
					f.seek(keys_pos_absolute)
					expected_bytes = num_frames * num_local_bones * 12
					anim_raw_bytes = f.read(expected_bytes)

				anim_keys_raw = np.frombuffer(anim_raw_bytes, dtype=BanisFile.dt_packed).reshape((num_frames, num_local_bones))
				
				# --- DEBUG LOGGING: START ---
				logging.debug(f"\n[DEBUG] --- Animation {anim_idx}: {bani.name} ---")
				logging.debug(f"  Scale       : {scale:.10f}")
				logging.debug(f"  Bias        : {bias:.10f}")
				logging.debug(f"  Local Bones : {num_local_bones}")
				logging.debug(f"  Total Frames: {num_frames}")
				logging.debug(f"  GPU Index:  : {b_data_idx}")
				logging.debug(f"  Disk Offset : {keys_pos_absolute} to {keys_pos_absolute + expected_bytes}")
				logging.debug(f"  Bone Map    : {b_map}")

				#if num_local_bones > 0 and num_frames > 0:
				#	logging.debug("  [Frame 0 Raw Hex]")
				#	for local_i in range(num_local_bones):
				#		r_raw = anim_keys_raw["rot_raw"][0, local_i]
				#		l_raw = anim_keys_raw["loc_raw"][0, local_i]
				#		global_i = b_map[local_i]
				#		
				#		logging.debug(f"    Curve {local_i:02d} -> Maps to Target Bone {global_i:02d}")
				#		logging.debug(f"      Rot: [{r_raw[0]:04X}, {r_raw[1]:04X}, {r_raw[2]:04X}]  Loc: [{l_raw[0]:04X}, {l_raw[1]:04X}, {l_raw[2]:04X}]")

				## Debug for specific anims
				#if anim_idx == 95 and num_frames > 0:
				#	logging.debug(f"Scale: {scale}, Bias: {bias}")
				#	for f in range(min(8, num_frames)):
				#		logging.debug(f"Animation 0, Frame {f}")
				#		for local_i in range(min(25, num_local_bones)):
				#			global_i, read_i = b_map[local_i]
				#			l_raw = anim_keys_raw["loc_raw"][f, local_i]
				#			l_float = locs[f, local_i]
				#			logging.debug(f"  Local Curve {local_i:02d} -> Global Bone {global_i:02d} -> Read {read_i:02d}")
				#			logging.debug(f"    Hex Loc:   [{l_raw[0]:04X}, {l_raw[1]:04X}, {l_raw[2]:04X}]")
				#			logging.debug(f"    Float Loc: [{l_float[0]:.6f}, {l_float[1]:.6f}, {l_float[2]:.6f}] meters")
				## --- DEBUG LOGGING: END ---

				# Decompress
				quats, locs = self.decompress_keyframes(anim_keys_raw["rot_raw"], anim_keys_raw["loc_raw"], scale, bias)

				# Read mapping
				bani.read_mapping = {}
				# Map channels to bones
				for local_i in range(num_local_bones):
					write_i, read_i = b_map[local_i]
					if write_i < global_num_bones:
						bani.keys["quat"][:, write_i] = quats[:, local_i]
						bani.keys["loc"][:, write_i] = locs[:, local_i]
						bani.animated_bone_indices.append(write_i)
						bani.read_mapping[write_i] = read_i
			else:
				# Fallback for old titles
				start_frame = bani.data.read_start_frame
				end_frame = start_frame + num_frames
				
				anim_keys_raw = keys_packed[start_frame:end_frame]
				quats, locs = self.decompress_keyframes(
					anim_keys_raw["rot_raw"], anim_keys_raw["loc_raw"],
					self.data.loc_scale, self.data.loc_min
				)
				
				bani.scale = self.data.loc_scale
				bani.bias = self.data.loc_min
				bani.keys["quat"] = quats
				bani.keys["loc"] = locs
				bani.animated_bone_indices = list(range(global_num_bones))
	
	def save(self, filepath):
		if self.context.version >= 7:
			raise NotImplementedError("Saving Version 7+ banis files is not yet implemented.")

		self.num_anims = len(self.anims)
		offset = 0
		self.data.num_frames = 0

		for bani in self.anims:
			bani.data.num_frames = len(bani.keys)
			self.data.num_frames += bani.data.num_frames
			bani.data.read_start_frame = offset
			offset += bani.data.num_frames

		# Assume all animations have the same bone count in Version < 7
		_num_frames, self.data.num_bones = self.anims[0].keys.shape
		self.data.bytes_per_frame = 12
		self.data.bytes_per_bone = self.data.num_bones * self.data.bytes_per_frame

		# Reassemble the whole array as floats
		quats_all = np.empty((self.data.num_frames, self.data.num_bones, 4), dtype=np.float32)
		locs_all = np.empty((self.data.num_frames, self.data.num_bones, 3), dtype=np.float32)

		for bani in self.anims:
			start = bani.data.read_start_frame
			end = start + bani.data.num_frames
			quats_all[start:end] = bani.keys["quat"]
			locs_all[start:end] = bani.keys["loc"]

		# Calculate translation scale and bias to spread range across 0 - 65535
		self.data.loc_min = float(np.min(locs_all))
		loc_max = float(np.max(locs_all))
		if loc_max - self.data.loc_min > 1e-8:
			self.data.loc_scale = (loc_max - self.data.loc_min) / 65535.0
		else:
			self.data.loc_scale = 1.0

		# Compress
		rot_raw, loc_raw = self.compress_keyframes(quats_all, locs_all, self.data.loc_scale, self.data.loc_min)
		
		# Pack into the final uint16 structured array
		keys_packed = np.empty((self.data.num_frames, self.data.num_bones), dtype=BanisFile.dt_packed)
		keys_packed["rot_raw"] = rot_raw
		keys_packed["loc_raw"] = loc_raw

		with open(filepath, "wb") as stream:
			# Write headers
			self.write_fields(stream, self)
			# Write keyframes
			stream.write(keys_packed.tobytes())
