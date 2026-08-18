import logging

import bpy
from bpy_extras import anim_utils


def get_rna_path(dtype, n_bone=None, n_shapekey=None, n_constraint=None, n_node_input=None):
	if n_bone:
		if n_constraint:
			return f'pose.bones["{n_bone}"].constraints["{n_constraint}"].{dtype}'
		else:
			return f'pose.bones["{n_bone}"].{dtype}'
	elif n_shapekey:
		return f'key_blocks["{n_shapekey}"].{dtype}'
	elif n_node_input:
		return f'nodes["{dtype}"].inputs[{n_node_input}].default_value'
	else:
		return dtype


class Animation:

	def __init__(self):
		self.fps = 30

	def create_action(self, b_obj, action_name):
		""" Create or retrieve action and set it as active on the object. """
		if not b_obj:
			raise AttributeError(f"No object to import '{action_name}' onto")
		if action_name in bpy.data.actions:
			b_action = bpy.data.actions[action_name]
			# clear and overwrite existing keys
			self.get_data(b_action).fcurves.clear()
		else:
			b_action = bpy.data.actions.new(action_name)
			b_action.use_fake_user = True
		# could probably skip this test and create always
		if not b_obj.animation_data:
			b_obj.animation_data_create()
		# set as active action on object
		b_obj.animation_data.action = b_action
		# https://developer.blender.org/docs/release_notes/4.4/python_api/#slotted-actions
		if bpy.app.version >= (4, 4, 0):
			if not b_action.slots:
				slot = b_action.slots.new(id_type='OBJECT', name=b_obj.name)
				b_obj.animation_data.action_slot = slot
		self.stash(b_obj, b_action)
		return b_action

	def stash(self, b_ob, b_action):
		# Simulate stash :
		# * add a track
		# * add an action on track
		# * lock & mute the track
		# * remove active action from object
		tracks = b_ob.animation_data.nla_tracks
		new_track = tracks.new(prev=None)
		new_track.name = b_action.name
		strip = new_track.strips.new(b_action.name, 0, b_action)
		new_track.lock = True
		new_track.mute = True

	def create_fcurves(self, action, dtype, drange, flags=None, n_bone=None, n_shapekey=None, n_constraint=None, n_node_input=None):
		""" Create fcurves in action for desired conditions. """
		rna_path = get_rna_path(dtype, n_bone, n_shapekey, n_constraint, n_node_input)

		if bpy.app.version >= (5, 0, 0):
			action_slot = action.slots[0]
			def create_fcurve(*args, **kwargs):
				kwargs["group_name"] = kwargs.pop("action_group")
				channelbag = anim_utils.action_ensure_channelbag_for_slot(action, action_slot)
				return channelbag.fcurves.ensure(*args, **kwargs)
		else:
			def create_fcurve(*args, **kwargs):
				return action.fcurves.new(*args, **kwargs)

		# armature pose bone animation
		if n_bone:
			if n_constraint:
				fcurves = [create_fcurve(data_path=rna_path, index=i) for i in drange]
			else:
				fcurves = [create_fcurve(data_path=rna_path, index=i, action_group=n_bone) for i in drange]
		# shapekey pose bone animation
		elif n_shapekey:
			fcurves = [create_fcurve(data_path=rna_path, index=0)]
		else:
			# Object animation (non-skeletal) is lumped into the "LocRotScale" action_group
			if dtype in ("rotation_euler", "rotation_quaternion", "location", "scale"):
				action_group = "LocRotScale"
			# Non-transforming animations (eg. visibility or material anims) use no action groups
			else:
				action_group = ""
			fcurves = [create_fcurve(data_path=rna_path, index=i, action_group=action_group) for i in drange]
		return fcurves

	def get_data(self, b_action):
		if bpy.app.version >= (5, 0, 0):
			action_slot = b_action.slots[0]
			channelbag = anim_utils.action_ensure_channelbag_for_slot(b_action, action_slot)
			return channelbag
		else:
			return b_action

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
			logging.warning("Unsupported extrapolation mode, using clamped.")
			for fcurve in fcurves:
				fcurve.extrapolation = 'CONSTANT'

	def add_keys(self, b_action, key_type, key_range, flags, frames, keys, interp, n_bone=None, n_shapekey=None, n_constraint=None):
		"""
		Create needed fcurves and add a list of keys to an action.
		"""
		# samples = [round(t * self.fps) for t in times]
		assert len(frames) == len(keys)
		ipo = None
		# get interpolation enum representation
		# ipo = bpy.types.Keyframe.bl_rna.properties['interpolation'].enum_items[interp].value
		interpolations = [ipo for _ in range(len(frames))]
		# import the keys
		try:
			fcurves = self.create_fcurves(b_action, key_type, key_range, flags, n_bone, n_shapekey, n_constraint)
			if len(key_range) == 1:
				# flat key - make it zippable
				key_per_fcurve = [keys]
			else:
				key_per_fcurve = zip(*keys)
			for fcurve, fcu_keys in zip(fcurves, key_per_fcurve):
				# add new points
				fcurve.keyframe_points.add(count=len(fcu_keys))
				# populate points with keys for this curve
				fcurve.keyframe_points.foreach_set("co", [x for co in zip(frames, fcu_keys) for x in co])
				if ipo:
					fcurve.keyframe_points.foreach_set("interpolation", interpolations)
				# update
				fcurve.update()
		except RuntimeError:
			# blender throws F-Curve ... already exists in action ...
			logging.warning(f"Could not add fcurve '{get_rna_path(key_type, n_bone, n_shapekey, n_constraint)}' to '{b_action.name}', already added before?")

	def add_key(self, fcurves, frame, key, interp):
		"""
		Add a key (len=n) to a set of fcurves (len=n) at the given frame. Set the key's interpolation to interp.
		"""
		# frame = round(t * self.fps)
		for fcurve, k in zip(fcurves, key):
			fcurve.keyframe_points.insert(frame, k)#.interpolation = interp
