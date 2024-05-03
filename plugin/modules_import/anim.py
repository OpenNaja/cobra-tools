import logging

import bpy


class Animation:

	def __init__(self):
		self.fps = 30

	@staticmethod
	def get_b_interp_from_n_interp(n_ipol):
		if n_ipol in (NifFormat.KeyType.LINEAR_KEY, NifFormat.KeyType.XYZ_ROTATION_KEY):
			return "LINEAR"
		elif n_ipol == NifFormat.KeyType.QUADRATIC_KEY:
			return "BEZIER"
		elif n_ipol == 0:
			# guessing, not documented in nif.xml
			return "CONSTANT"
		# NifLog.warn(f"Unsupported interpolation mode ({n_ipol}) in nif, using quadratic/bezier.")
		return "BEZIER"

	def create_action(self, b_obj, action_name):
		""" Create or retrieve action and set it as active on the object. """
		if action_name in bpy.data.actions:
			b_action = bpy.data.actions[action_name]
			# clear and overwrite existing keys
			b_action.fcurves.clear()
		else:
			b_action = bpy.data.actions.new(action_name)
			b_action.use_fake_user = True
		# could probably skip this test and create always
		if not b_obj.animation_data:
			b_obj.animation_data_create()
		# set as active action on object
		b_obj.animation_data.action = b_action
		return b_action

	def create_fcurves(self, action, dtype, drange, flags=None, n_bone=None, n_shapekey=None, n_constraint=None):
		""" Create fcurves in action for desired conditions. """
		# armature pose bone animation
		if n_bone:
			if n_constraint:
				fcurves = [
					action.fcurves.new(data_path=f'pose.bones["{n_bone}"].constraints["{n_constraint}"].{dtype}', index=i)
					for i in drange]
			else:
				fcurves = [
					action.fcurves.new(data_path=f'pose.bones["{n_bone}"].{dtype}', index=i, action_group=n_bone)
					for i in drange]
		# shapekey pose bone animation
		elif n_shapekey:
			fcurves = [
				action.fcurves.new(data_path=f'key_blocks["{n_shapekey}"].{dtype}', index=0,)
			]
		else:
			# Object animation (non-skeletal) is lumped into the "LocRotScale" action_group
			if dtype in ("rotation_euler", "rotation_quaternion", "location", "scale"):
				action_group = "LocRotScale"
			# Non-transformaing animations (eg. visibility or material anims) use no action groups
			else:
				action_group = ""
			fcurves = [action.fcurves.new(data_path=dtype, index=i, action_group=action_group) for i in drange]
		if flags:
			self.set_extrapolation(self.get_extend_from_flags(flags), fcurves)
		return fcurves

	@staticmethod
	def get_extend_from_flags(flags):
		if flags & 6 == 4:  # 0b100
			return "CONSTANT"
		elif flags & 6 == 0:  # 0b000
			return "CYCLIC"

		NifLog.warn("Unsupported cycle mode in nif, using clamped.")
		return "CONSTANT"

	@staticmethod
	def get_extend_from_cycle_type(cycle_type):
		return ("CYCLIC", "REVERSE", "CONSTANT")[cycle_type]

	@staticmethod
	def set_extrapolation(extend_type, fcurves):
		if extend_type == "CONSTANT":
			for fcurve in fcurves:
				fcurve.extrapolation = 'CONSTANT'
		elif extend_type == "CYCLIC":
			for fcurve in fcurves:
				fcurve.modifiers.new('CYCLES')
		# don't support reverse for now, not sure if it is even possible in blender
		else:
			NifLog.warn("Unsupported extrapolation mode, using clamped.")
			for fcurve in fcurves:
				fcurve.extrapolation = 'CONSTANT'

	def add_keys(self, b_action, key_type, key_range, flags, samples, keys, interp, n_bone=None, n_key=None, n_constraint=None):
		"""
		Create needed fcurves and add a list of keys to an action.
		"""
		# samples = [round(t * self.fps) for t in times]
		assert len(samples) == len(keys)
		ipo = None
		# get interpolation enum representation
		# ipo = bpy.types.Keyframe.bl_rna.properties['interpolation'].enum_items[interp].value
		interpolations = [ipo for _ in range(len(samples))]
		# import the keys
		try:
			fcurves = self.create_fcurves(b_action, key_type, key_range, flags, n_bone, n_key, n_constraint)
			if len(key_range) == 1:
				# flat key - make it zippable
				key_per_fcurve = [keys]
			else:
				key_per_fcurve = zip(*keys)
			for fcurve, fcu_keys in zip(fcurves, key_per_fcurve):
				# add new points
				fcurve.keyframe_points.add(count=len(fcu_keys))
				# populate points with keys for this curve
				fcurve.keyframe_points.foreach_set("co", [x for co in zip(samples, fcu_keys) for x in co])
				if ipo:
					fcurve.keyframe_points.foreach_set("interpolation", interpolations)
				# update
				fcurve.update()
		except RuntimeError:
			# blender throws F-Curve ... already exists in action ...
			logging.warning(f"Could not add fcurve '{key_type}' to '{b_action.name}', already added before?")

	def add_key(self, fcurves, frame, key, interp):
		"""
		Add a key (len=n) to a set of fcurves (len=n) at the given frame. Set the key's interpolation to interp.
		"""
		# frame = round(t * self.fps)
		for fcurve, k in zip(fcurves, key):
			fcurve.keyframe_points.insert(frame, k)#.interpolation = interp

	# import animation groups
	def import_text_keys(self, n_block, b_action):
		"""Gets and imports a NiTextKeyExtraData"""
		if isinstance(n_block, NifFormat.NiControllerSequence):
			txk = n_block.text_keys
		else:
			txk = n_block.find(block_type=NifFormat.NiTextKeyExtraData)
		self.import_text_key_extra_data(txk, b_action)

	def import_text_key_extra_data(self, txk, b_action):
		"""Stores the text keys as pose markers in a blender action."""
		if txk and b_action:
			for key in txk.text_keys:
				newkey = key.value.decode().replace('\r\n', '/').rstrip('/')
				frame = round(key.time * self.fps)
				marker = b_action.pose_markers.new(newkey)
				marker.frame = frame

	def set_frames_per_second(self, roots):
		"""Scan all blocks and set a reasonable number for fps to this class and the scene."""
		# find all key times
		key_times = []
		for root in roots:
			for kfd in root.tree(block_type=NifFormat.NiKeyframeData):
				key_times.extend(key.time for key in kfd.translations.keys)
				key_times.extend(key.time for key in kfd.scales.keys)
				key_times.extend(key.time for key in kfd.quaternion_keys)
				key_times.extend(key.time for key in kfd.xyz_rotations[0].keys)
				key_times.extend(key.time for key in kfd.xyz_rotations[1].keys)
				key_times.extend(key.time for key in kfd.xyz_rotations[2].keys)

			for kfi in root.tree(block_type=NifFormat.NiBSplineInterpolator):
				if not kfi.basis_data:
					# skip bsplines without basis data (eg bowidle.kf in Oblivion)
					continue
				key_times.extend(
					point * (kfi.stop_time - kfi.start_time)
					/ (kfi.basis_data.num_control_points - 2)
					for point in range(kfi.basis_data.num_control_points - 2))

			for uv_data in root.tree(block_type=NifFormat.NiUVData):
				for uv_group in uv_data.uv_groups:
					key_times.extend(key.time for key in uv_group.keys)

		# not animated, return a reasonable default
		if not key_times:
			return

		# calculate fps
		key_times = sorted(set(key_times))
		fps = self.fps
		lowest_diff = sum(abs(int(time * fps + 0.5) - (time * fps)) for time in key_times)

		# for test_fps in range(1,120): #disabled, used for testing
		for test_fps in [20, 24, 25, 30, 35]:
			diff = sum(abs(int(time * test_fps + 0.5) - (time * test_fps)) for time in key_times)
			if diff < lowest_diff:
				lowest_diff = diff
				fps = test_fps
		NifLog.info(f"Animation estimated at {fps} frames per second.")
		self.fps = fps
		bpy.context.scene.render.fps = fps
		bpy.context.scene.frame_set(0)