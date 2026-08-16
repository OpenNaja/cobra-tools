import logging
from math import radians

import bpy
import mathutils
from mathutils import Vector, Quaternion, Matrix

from plugin.modules_export.armature import get_armature
from plugin.modules_import.armature import set_transform, append_armature_modifier
from plugin.modules_import.collision import parent_to, box_from_extents, box_from_dimensions, set_b_collider
from plugin.utils.blender_util import vectorisclose
from plugin.utils.object import create_ob, create_collection

VEC3_0 = mathutils.Vector((0, 0, 0))
VEC3_1 = mathutils.Vector((1, 1, 1))
VEC4_1 = mathutils.Vector((1, 0, 0, 0))


def apply_pose_to_meshes(b_armature_ob):
	logging.info(f"Applying armature modifiers of children objects")
	# Go over every object in the scene
	for ob in bpy.data.objects:
		# Check if they are parented to the armature, are a mesh, and have modifiers
		if ob.parent == b_armature_ob and ob.type == 'MESH' and ob.modifiers:
			with bpy.context.temp_override(object=ob):
				for modifier in ob.modifiers:
					if modifier.type == 'ARMATURE':
						# Apply the armature modifier
						bpy.ops.object.modifier_copy(modifier=modifier.name)
						bpy.ops.object.modifier_apply(modifier=modifier.name)


def apply_armature_all(reporter):
	# Check if the active object is a valid armature
	if bpy.context.active_object.type != 'ARMATURE':
		# Object is not an armature. Cancelling.
		return f"No armature selected.",

	# Get the armature
	b_armature_ob = bpy.context.object
	apply_pose_to_meshes(b_armature_ob)
	bpy.ops.pose.armature_apply()


def add_hitcheck_to_mdl2(obj, collection, parent):
	""" Creates a hitcheck bounding volume box with predefined physics response """

	# get the bounding box of the original object
	bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
	x, y, z = obj.dimensions
	hitcheck_ob, b_me = box_from_dimensions(f"{obj.name}_PhysicsVolume", (y, x, z), collection)
	# this corresponds to identity rotation matrix in ms2 collider
	hitcheck_ob.rotation_euler = (0, 0, 0)

	# set center
	x = (bbox_corners[4][0] + bbox_corners[0][0]) / 2  # invert x axis
	y = (bbox_corners[3][1] + bbox_corners[0][1]) / -2
	z = (bbox_corners[2][2] + bbox_corners[0][2]) / 2
	hitcheck_ob.location = (y, x, z)

	set_b_collider(hitcheck_ob, bounds_type="BOX", display_type="BOX")
	# Assign parent joint
	hitcheck_ob.parent = parent
	# collision data
	hitcheck_ob.cobra_coll.flag = 'STATIC'
	hitcheck_ob.cobra_coll.classification_jwe2 = 'Prop'
	hitcheck_ob.cobra_coll.surface_jwe2 = 'PropWooden'
	hitcheck_ob.cobra_coll.classification_pz = 'Scenery'
	hitcheck_ob.cobra_coll.surface_pz = 'Wood'


def split_object_by_material(obj):
	with bpy.context.temp_override(selected_objects=[obj], object=obj, active_object=obj):
		# Edit Mode, separate and back to object mode
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.separate(type='MATERIAL')
		bpy.ops.object.mode_set(mode='OBJECT')	

def validate_object_to_mdl2(obj):
	""" Check current object data, like num of polys etc.."""
	pass


def comform_object_to_mdl2(obj):
	""" Check and add object requirements, like missing flags etc """
	if bpy.context.scene.cobra.game == "Planet Zoo":

		# 'default' properties for scenery -  TODO: move this to a default setup function
		obj.data['flag'] = 513
		obj.data['unk_f0'] = 0.0
		obj.data['unk_f1'] = 0.0

		# Add a second UV layer if missing, rename them 
		if len(obj.data.uv_layers):
			obj.data.uv_layers[0].name = 'UV0'
		if len(obj.data.uv_layers) > 1:
			obj.data.uv_layers[1].name = 'UV1'
		if len(obj.data.uv_layers) == 1:
			obj.data.uv_layers.new(name='UV1')

	elif bpy.context.scene.cobra.game == "Jurassic World 2":
		return f"Game not supported.",
	else:
		return f"Game not supported.",

	# split materials, rename new objects
	pass


def setup_rig(reporter, move_collections=True, add_armature=True, add_physics=True):
	b_ob = bpy.context.active_object
	scene = bpy.context.scene
	name = b_ob.name
	bone_name = "def_c_root_joint"

	# validate object before starting
	validate_object_to_mdl2(b_ob)

	# get or create collections
	mdl2_coll = create_collection(name, scene.collection)
	if move_collections:
		# move it to L0 collection
		lod_coll = create_collection(f"{name}_L0", mdl2_coll)
		move_to_collection(b_ob, lod_coll)
		src_coll = scene.collection
	else:
		src_coll = mdl2_coll
		lod_coll = b_ob.users_collection[0]
	# rename b_ob to the right lod (mostly cosmetic)
	for i, ob in enumerate(lod_coll.objects):
		ob.name = f"{name}_ob{i}_L{lod_coll.name[-1]}"

	# Add a default render flag custom property to the collection,
	# 0 for scenery most of the games, 4 for PZ scenery.
	# TODO: probably need to move this to a better scene/render flag/mesh flags setup
	mdl2_coll['render_flag'] = 0
	if scene.cobra.game == 'Planet Zoo':
		mdl2_coll['render_flag'] = 4

	# ensure the object/mesh has the right valid data 
	comform_object_to_mdl2(b_ob)

	if add_armature:
		# see if an armature exists in the source collection
		b_armature_ob = get_armature(src_coll.objects)
		if b_armature_ob:
			move_to_collection(b_armature_ob, mdl2_coll)
		else:
			# create armature
			armature_name = f"{name}_Armature"
			b_armature_data = bpy.data.armatures.new(armature_name)
			b_armature_data.display_type = 'STICK'
			b_armature_ob = create_ob(scene, armature_name, b_armature_data, coll=mdl2_coll)
			b_armature_ob.show_in_front = True

			# make armature editable and create bones
			bpy.ops.object.mode_set(mode='EDIT', toggle=False)
			b_edit_bone = b_armature_data.edit_bones.new(bone_name)
			b_edit_bone["long_name"] = bone_name
			# identity transform in ms2 space
			b_edit_bone.head = (0, 0, 0)
			b_edit_bone.tail = (1, 0, 0)
			b_edit_bone.roll = 0.0
			bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

		# weight paint mesh to bone
		if bone_name not in b_ob.vertex_groups:
			b_ob.vertex_groups.new(name=bone_name)
			b_ob.vertex_groups[bone_name].add(list(range(len(b_ob.data.vertices))), 1.0, 'REPLACE')
			append_armature_modifier(b_ob, b_armature_ob)

		if add_physics:
			joint_coll = create_collection(f"{name}_joints", mdl2_coll)
			if not joint_coll.objects:
				# add physics joint
				b_joint = create_ob(scene, f"{name}_Physics_Joint", None, coll=joint_coll)
				parent_to(b_armature_ob, b_joint, bone_name)
				b_joint.rotation_euler = (0, 0, 0)

				# create hitcheck object
				add_hitcheck_to_mdl2(b_ob, joint_coll, b_joint)

	# mdl2 require objects to have only one material
	split_object_by_material(b_ob)


def move_to_collection(b_ob, target_coll):
	for coll in b_ob.users_collection:
		coll.objects.unlink(b_ob)
	target_coll.objects.link(b_ob)


def generate_rig_edit(reporter, **kwargs):
	"""Automatic rig edit generator by NDP. Detects posed bones and automatically generates nodes and offsets them."""
	logging.info(f"generating rig edit from pose")

	# Function settings
	mergenodes = kwargs.get('mergenodes', True)
	applyarmature = kwargs.get('applyarmature', False)
	errortolerance = 0.0001

	# Log settings
	logging.info(f"function settings:")
	logging.info(f"merge identical nodes = {mergenodes}")
	logging.info(f"apply armature modifiers = {applyarmature}")
	logging.info(f"error tolerance = {errortolerance}")

	b_armature_ob = get_active_armature()

	# Apply armature modifiers of children objects
	if applyarmature:
		apply_pose_to_meshes(b_armature_ob)
	# Store current mode
	original_mode = bpy.context.mode
	# it doesn't recognize edit_armature as a valid mode to switch to so we change it to just edit. Blender moment
	if original_mode == 'EDIT_ARMATURE':
		original_mode = 'EDIT'

	# Store number of edits done
	editnumber = 0

	# Force Switch to pose mode.
	bpy.ops.object.mode_set(mode='POSE')

	# Creating list of posed bones and storing data
	# Initiate dictionary of matrix data
	posebone_data = {}

	# We iterate over every pose bone and detetect which ones have been posed, and create  a list of them.
	logging.info(f"evaluating posed bones:")
	for p_bone in b_armature_ob.pose.bones:
		# We check if vectors have  miniscule transforms, and just consider them rounding errors and clear them.
		# Check location
		if vectorisclose(p_bone.location, VEC3_0, errortolerance) and p_bone.location != VEC3_0:
			# Warn the user
			logging.info(f"{p_bone.name} had miniscule location transforms, assuming it is an error and clearing")
			# Clear transforms
			p_bone.location = VEC3_0

		# Check rotation
		if vectorisclose(Vector(p_bone.rotation_quaternion), VEC4_1, errortolerance) and Vector(
				p_bone.rotation_quaternion) != VEC4_1:
			# Warn the user
			logging.info(f"{p_bone.name} had miniscule rotation transforms, assuming it is an error and clearing")
			# Clear rotation
			p_bone.rotation_quaternion = Quaternion((1, 0, 0, 0))

		# Check scale
		if vectorisclose(p_bone.scale, VEC3_1, errortolerance) and p_bone.scale != VEC3_1:
			# Warn the user
			logging.info(f"{p_bone.name} had miniscule scale transforms, assuming it is an error and clearing")
			# Clear scale
			p_bone.scale = VEC3_1

		# Check if any bones have major scale transform, and warn the user.
		if not vectorisclose(p_bone.scale, VEC3_1, errortolerance):
			logging.info(
				f"{p_bone.name} had scale. Value = {repr(p_bone.scale)}, difference: {(p_bone.scale - VEC3_1).length}")
			reporter.show_warning(f"{p_bone.name} had scale transforms. Reset scale for all bones and try again.")
			return

		# We check for NODE bones with transforms and skip them.
		if (not vectorisclose(p_bone.location, VEC3_0, errortolerance) or not vectorisclose(
				p_bone.scale, VEC3_1, errortolerance) or not vectorisclose(
			Vector(p_bone.rotation_quaternion), VEC4_1, errortolerance)) and p_bone.name.startswith(
			"NODE_"):
			# Ignore posed NODE bones and proceed to the next, their offsets can be applied directly.
			editnumber += 1
			logging.info(f"rig edit number {editnumber}")
			logging.info(f"NODE with offsets detected. Applying offsets directly.")
			continue

		# We append any remaining bones that have been posed.
		if (not vectorisclose(p_bone.location, VEC3_0, errortolerance) or not vectorisclose(p_bone.scale, VEC3_1,
																							errortolerance) or not vectorisclose(
			Vector(p_bone.rotation_quaternion), VEC4_1, errortolerance)):
			# bonebase values
			logging.info(f"p_bone: {p_bone.name}")
			# logging.info(f"p_bone head (global rest):        {p_bone.bone.head_local}")
			# logging.info(f"p_bone head (global pose):        {p_bone.head}")
			# logging.info(f"p_bone head (+difference):        {p_bone.head - p_bone.bone.head_local}")
			if not p_bone.parent:
				posebone_data[p_bone.name] = [p_bone.matrix.copy(), p_bone.bone.matrix_local.copy(), Matrix(
					((0.0, 1.0, 0.0, 0.0), (-1.0, 0.0, 0.0, 0.0), (0.0, 0.0, 1.0, 0.0), (0.0, 0.0, 0.0, 1.0)))]
			else:
				posebone_data[p_bone.name] = [p_bone.matrix.copy(), p_bone.bone.matrix_local.copy(),
											  p_bone.parent.bone.matrix_local.copy()]

	# Apply pose as rest pose
	bpy.ops.pose.armature_apply()

	# Creating the nodes
	# We switch to edit mode to use edit bones, as they do not exist outside of edit mode.
	# Switch to edit mode
	bpy.ops.object.mode_set(mode='EDIT')

	for bone_name, (base_posed, base_armature_space, parent_armature_space) in posebone_data.items():
		# Get edit bone
		bonebase = b_armature_ob.data.edit_bones.get(bone_name)

		if not bonebase.parent:
			logging.info(f"{bonebase.name} has no parent, creating a blank node")
			# Create the node
			bonenode = b_armature_ob.data.edit_bones.new(f"NODE_{bone_name}")

			bonenode.matrix = Matrix(
				((0.0, 1.0, 0.0, 0.0), (-1.0, 0.0, 0.0, 0.0), (0.0, 0.0, 1.0, 0.0), (0.0, 0.0, 0.0, 1.0)))

			# Does length matter? It was just dissapearing for some reason
			bonenode.length = 1

			# Set parent of bonebase to bonenode
			bonebase.parent = bonenode

		# Set the parent
		boneparent = bonebase.parent

		# Detect if the bone already has a node.
		if boneparent.name.startswith("NODE_"):
			logging.info(f"{bone_name} has a pre-existing NODE. Using it instead.")
			bonenode = bonebase.parent

		else:
			# Set the parent
			boneparent = bonebase.parent

			# Creating the node bone
			bonenode = b_armature_ob.data.edit_bones.new(f"NODE_{bone_name}")

			# Set parent of bonenode to boneparent
			bonenode.parent = boneparent

			# Set parent of bonebase to bonenode
			bonebase.parent = bonenode

			# Copy parent length to node
			bonenode.length = boneparent.length

		# Define the matrix
		bonenode_matrix_local = base_posed @ (base_armature_space.inverted() @ parent_armature_space)
		# logging.info(f"calculated node matrix")
		# logging.info(f"{bonenode_matrix_local}")

		# Remember length
		nodelength = bonenode.length

		# Set node matrix
		# bonenode.matrix = bonenode_matrix_local
		set_transform(bonenode_matrix_local, bonenode)

		# Restore length
		bonenode.length = nodelength

		# Node completed. Log number of edits.
		editnumber += 1
		# Node creation complete
		logging.info(f"created node: {bonenode.name}")
	# logging.info(f"node matrix:")
	# logging.info(f"{bonenode.matrix}")

	bpy.ops.object.mode_set(mode='POSE')

	# Creating node groups to delete duplicates to merge
	if mergenodes:
		logging.info(f"creating node_groups to merge")

		# create a list of all NODES
		node_list = [p_bone for p_bone in b_armature_ob.pose.bones if p_bone.name.startswith("NODE_")]

		# Create NODE parent dictionary
		node_groups = {}

		# create and sort NODE groups
		# create a dictionary with a tuple of: parent,rounded matrix as the key. This way we can group identical nodes
		for p_bone in node_list:
			# create a rounded matrix to create leeway for miniscule variation
			rounded_matrix = tuple(tuple(round(element, 5) for element in row) for row in p_bone.bone.matrix_local)

			# use the parent and rounded matrix as a key to sort all identical nodes into groups
			parent_name = p_bone.parent.name if p_bone.parent else "ROOTNODE"
			keytuple = (parent_name, rounded_matrix)
			if keytuple not in node_groups:
				node_groups[keytuple] = []
			node_groups[keytuple].append(p_bone)

		# Log node groups
		for (parent_name, rounded_matrix), nodegroup in node_groups.items():
			logging.debug(f"node group: {parent_name} {rounded_matrix}")
			for node in nodegroup:
				logging.debug(f"node: {node.name}")

		# store number of deleted nodes
		deletednodes = 0

		# Merge node groups
		for (parent_name, rounded_matrix), nodegroup in node_groups.items():
			# Rename NODE to indicate it owns more than one bone
			if len(nodegroup) > 1:
				# Renaming to be more descriptive
				nodegroup[0].name = f"NODE_{len(nodegroup)}GROUP_{parent_name}"

			# Log group organization
			# logging.info(f"first node: {nodegroup[0].name}")
			# logging.info(f"first child: {nodegroup[0].children[0].name}")

			# Delete all extra nodes
			for node in nodegroup:
				if node != nodegroup[0] and node.children:
					# logging.info(f"secondary node: {node.name}")
					# logging.info(f"secondary child: {node.children[0].name}")

					# Switch to edit mode to edit the parents
					bpy.ops.object.mode_set(mode='EDIT')

					# Reparent duplicate basebones to the first node
					b_armature_ob.data.edit_bones.get(node.children[0].name).parent = b_armature_ob.data.edit_bones.get(
						nodegroup[0].name)

					# Delete the duplicate nodes
					deletednodes += 1
					b_armature_ob.data.edit_bones.remove(b_armature_ob.data.edit_bones.get(node.name))

					# Switch back to pose mode
					bpy.ops.object.mode_set(mode='POSE')

		# Report amount of deleted nodes
		if deletednodes > 0:
			logging.info(f"merged {deletednodes} nodes into node groups")
	# Node groups completed

	# Switch back to original mode.
	bpy.ops.object.mode_set(mode=original_mode)

	# Finalize
	logging.info(f"total number of edits: {editnumber}")
	totalnodes = len([p_bone for p_bone in b_armature_ob.pose.bones if p_bone.name.startswith("NODE_")])
	totalbones = len(b_armature_ob.pose.bones)
	logging.info(f"total nodes: {totalnodes}")
	logging.info(f"total bones: {totalbones}")

	if totalbones > 254:
		reporter.show_warning(
			f"Total amount of bones exceeds 254 after rig edit, game will crash. Please undo, reduce the number of edits, and try again.")
	else:
		reporter.show_info(f"{editnumber} rig edits generated succesfully")


def get_active_armature():
	b_armature_ob = bpy.context.active_object
	if not b_armature_ob:
		raise AttributeError(f"No object selected.")
	# Check if the active object is a valid armature
	if b_armature_ob.type != 'ARMATURE':
		# Object is not an armature. Cancelling.
		raise AttributeError(f"No armature selected.")
	logging.info(f"armature: {b_armature_ob.name}")
	return b_armature_ob


def convert_scale_to_loc(reporter):
	"""Automatically convert scaled bones into equivalent visual location transforms"""
	# Function for converting scale to visual location transforms in pose mode
	logging.info(f"converting scale transforms to visual location")

	# Store current mode
	original_mode = bpy.context.mode
	# it doesn't recognize edit_armature as a valid mode to switch to so we change it to just edit. Blender moment
	if original_mode == 'EDIT_ARMATURE':
		original_mode = 'EDIT'
	# Set to pose mode
	bpy.ops.object.mode_set(mode='POSE')

	b_armature_ob = get_active_armature()

	# Initiate logging variable
	editnumber = 0

	# Initiate list of any bones that are not at their armaturespace rest location
	posebone_list = []
	posebone_data = {}

	# We get a list of all bones not in their rest positions in armaturespace
	for p_bone in b_armature_ob.pose.bones:
		posebone_rotation = p_bone.rotation_quaternion.copy()

		p_bone.rotation_quaternion = (1, 0, 0, 0)
		bpy.context.view_layer.update()

		# We copy all data in case we need parent data
		posebone_data[p_bone] = [p_bone.bone.head_local.copy(), p_bone.head.copy(), p_bone.location.copy(),
								 posebone_rotation]
		posebone_list.append(p_bone)
		logging.info(f"{p_bone.name} rest pos: {p_bone.bone.head_local}")
		logging.info(f"{p_bone.name} pose pos: {p_bone.head}")

	# Clear scale of all bones
	for p_bone in b_armature_ob.pose.bones:
		p_bone.scale = VEC3_1
		p_bone.location = VEC3_0

	# Clear scale and set location
	logging.info(f"Setting location of pose bones:")
	for p_bone in posebone_list:
		logging.info(f"posed bone: {p_bone}")
		# Update positions
		bpy.context.view_layer.update()

		if p_bone.parent:
			# Bone_rest offset from Parent_rest
			rest_offset = posebone_data[p_bone][0] - posebone_data[p_bone.parent][0]

			# Bone_pose offset from Parent_pose
			pose_offset = posebone_data[p_bone][1] - posebone_data[p_bone.parent][1]

			calc_offset = pose_offset - rest_offset

			p_bone.matrix.translation = p_bone.matrix.translation + calc_offset

		else:
			p_bone.matrix.translation = p_bone.matrix.translation + (
					posebone_data[p_bone][1] - posebone_data[p_bone][0])

		editnumber = editnumber + 1

	for p_bone in posebone_list:
		p_bone.rotation_quaternion = posebone_data[p_bone][3]

	# Return to original mode
	bpy.ops.object.mode_set(mode=original_mode)

	if editnumber > 0:
		reporter.show_info(f"Moved {editnumber} bones to their visual locations and reset scales")
	else:
		reporter.show_info(f"No bones required movement")


def iter_bones_parents_first(b_armature_ob):
	"""Yield pose bones so a bone always follows its parent.

	Setting pose_bone.matrix is resolved against the parent's current state, so a child
	written before its parent gets the wrong result.
	"""
	done = set()
	def visit(p_bone):
		if p_bone.name in done:
			return
		if p_bone.parent is not None:
			visit(p_bone.parent)
		done.add(p_bone.name)
		yield_list.append(p_bone)
	yield_list = []
	for p_bone in b_armature_ob.pose.bones:
		visit(p_bone)
	return yield_list


def transfer_animation_to_original(b_ctrl, b_orig, frame_start=None, frame_end=None):
	"""Bake the control rig's pose onto the original rig, correcting for rest differences.

	The two rigs share bone heads and directions but not rolls, so their rest matrices
	differ by a rotation about each bone's own axis. Deformation is
	`pose_matrix @ rest_matrix.inverted()`, so matching deformation means

		M_orig = M_ctrl @ L_ctrl.inverted() @ L_orig

	A COPY_TRANSFORMS constraint sets `M_orig = M_ctrl`, dropping the
	`L_ctrl.inverted() @ L_orig` term and twisting every mirrored bone by its full roll
	delta - measured at 51.57 degrees on a 0.9 rad roll difference, visible at rest
	before any animation. That is why constraints are not used to link the two rigs.

	Run this before exporting: clips are stored relative to each bone's rest
	orientation, so the animation has to land on the original rolls to be correct in
	game.

	Returns (frames_baked, bones_baked).
	"""
	scene = bpy.context.scene
	frame_start = scene.frame_start if frame_start is None else frame_start
	frame_end = scene.frame_end if frame_end is None else frame_end

	corrections = {}
	for name, b_bone in b_orig.data.bones.items():
		ctrl_bone = b_ctrl.data.bones.get(name)
		if ctrl_bone is not None:
			corrections[name] = ctrl_bone.matrix_local.inverted() @ b_bone.matrix_local
	if not corrections:
		raise ValueError(f"{b_ctrl.name} and {b_orig.name} share no bone names")

	if b_orig.animation_data is None:
		b_orig.animation_data_create()
	if b_orig.animation_data.action is None:
		b_orig.animation_data.action = bpy.data.actions.new(f"{b_orig.name}_baked")

	ordered = [p_bone for p_bone in iter_bones_parents_first(b_orig) if p_bone.name in corrections]
	view_layer = bpy.context.view_layer
	frames = 0
	for frame in range(int(frame_start), int(frame_end) + 1):
		scene.frame_set(frame)
		for p_bone in ordered:
			p_bone.matrix = b_ctrl.pose.bones[p_bone.name].matrix @ corrections[p_bone.name]
			# resolve this bone before its children read it
			view_layer.update()
		for p_bone in ordered:
			p_bone.keyframe_insert(data_path="location", frame=frame)
			if p_bone.rotation_mode == 'QUATERNION':
				p_bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)
			else:
				p_bone.keyframe_insert(data_path="rotation_euler", frame=frame)
			p_bone.keyframe_insert(data_path="scale", frame=frame)
		frames += 1
	return frames, len(ordered)


def bind_meshes_to_rig(b_armature_ob, b_target_ob):
	"""Move every mesh deformed by b_armature_ob over to b_target_ob.

	Retargets the Armature modifier and reparents, keeping each mesh's world
	transform. Equivalent to applying the original armature modifier and reparenting
	the mesh to the new rig by hand, but non-destructive: applying bakes whatever pose
	the rig happens to be in into the mesh data, which silently ruins the model if the
	rig was not at rest.

	Rebinding is safe even though the duplicate's rolls differ. Skinning is driven by
	`pose_matrix @ rest_matrix.inverted()`, so at rest the two cancel out regardless of
	roll, and once posed the deformation is correct relative to the new rest. Bone heads
	are identical in both rigs, and vertex groups bind by bone name.

	Returns (meshes_reparented, modifiers_retargeted).
	"""
	reparented = modifiers_retargeted = 0
	for b_ob in list(b_armature_ob.children):
		if b_ob.type != 'MESH':
			continue
		# only follow meshes this rig actually deforms. A mesh parented to the armature
		# without an armature modifier is a prop or a collider proxy, and giving it one
		# would start deforming geometry that is meant to stay rigid
		matching = [modifier for modifier in b_ob.modifiers
					if modifier.type == 'ARMATURE' and modifier.object == b_armature_ob]
		if not matching:
			continue
		for modifier in matching:
			modifier.object = b_target_ob
			modifiers_retargeted += 1
		matrix_world = b_ob.matrix_world.copy()
		b_ob.parent = b_target_ob
		b_ob.matrix_world = matrix_world
		reparented += 1
	return reparented, modifiers_retargeted


def generate_mirror_rig(b_armature_ob, bind_mesh=True, suffix="_ctrl"):
	"""Build a duplicate of b_armature_ob whose .L/.R bones are true mirrors.

	Cobra's MS2 import gives matching left/right bones mirrored HEAD positions but not
	mirrored orientations, so blender's X-Axis Mirror applies a pose transform along
	the wrong local axis - move the left wrist right and the right wrist goes right
	too. Measured on a JWE3 rig: 35 of 71 pairs had y/z axis errors up to 1.9.

	The fix cannot be applied to the rig you export. MS2 export writes each bone's
	matrix_local verbatim, so re-rolling changes the skeleton that ships. Instead this
	mirrors a DUPLICATE: animate on the duplicate with working symmetry, then bake back
	with transfer_animation_to_original before export.

	The two rigs are deliberately NOT linked by constraints. COPY_TRANSFORMS copies world
	orientation, which carries the rest-roll difference with it, so it twists every
	mirrored bone on the original by its full roll delta the moment it is added - 51.57
	degrees on a 0.9 rad difference, at rest. See transfer_animation_to_original.

	Bone heads are never modified - they are what the mesh is skinned to. Only tails
	and rolls change, which is all the local axes depend on.

	With bind_mesh, the meshes are moved onto the control rig so the model deforms from
	the rig you are actually animating, instead of watching the original follow along
	through constraints. See bind_meshes_to_rig for why re-rolled bones still deform
	correctly.

	Beware on export: get_armature() picks the *selected* armature when a collection
	holds more than one, and the control rig gets linked into the original's
	collections. Exporting with the control rig selected therefore ships its re-rolled
	bones. Select the original, or bake to it and delete the control rig first.

	Returns (control_object, pairs_fixed, constraints_added, meshes_bound).
	"""
	scene = bpy.context.scene
	name = f"{b_armature_ob.name}{suffix}"

	b_ctrl = b_armature_ob.copy()
	b_ctrl.data = b_armature_ob.data.copy()
	b_ctrl.name = b_ctrl.data.name = name
	b_ctrl.animation_data_clear()
	for coll in b_armature_ob.users_collection:
		coll.objects.link(b_ctrl)

	# mirror tails and rolls on the duplicate
	previous_active = bpy.context.view_layer.objects.active
	bpy.context.view_layer.objects.active = b_ctrl
	bpy.ops.object.mode_set(mode='EDIT')
	edit_bones = b_ctrl.data.edit_bones
	pairs_fixed = 0
	for b_left in edit_bones:
		if not b_left.name.endswith(".L"):
			continue
		b_right = edit_bones.get(f"{b_left.name[:-2]}.R")
		if b_right is None:
			continue
		wanted_tail = Vector((-b_left.tail.x, b_left.tail.y, b_left.tail.z))
		# negating roll is NOT a general mirror - it only happens to work for some bone
		# orientations and twists the rest (seen on deinosuchus legs). Instead mirror the
		# left bone's z axis across X and let blender solve the roll that best matches it.
		wanted_z = Vector((-b_left.z_axis.x, b_left.z_axis.y, b_left.z_axis.z))
		if (b_right.tail - wanted_tail).length < 1e-4 and (b_right.z_axis - wanted_z).length < 1e-4:
			continue
		b_right.tail = wanted_tail
		b_right.align_roll(wanted_z)
		pairs_fixed += 1
	bpy.ops.object.mode_set(mode='OBJECT')

	# deform the model from the control rig rather than through the original
	meshes_bound = 0
	if bind_mesh:
		meshes_bound, _ = bind_meshes_to_rig(b_armature_ob, b_ctrl)

	bpy.context.view_layer.objects.active = previous_active
	return b_ctrl, pairs_fixed, meshes_bound


def remove_mirror_rig_constraints(b_armature_ob):
	"""Strip the COPY_TRANSFORMS constraints an earlier Generate Mirror Rig added.

	They twist every mirrored bone by its roll delta, so a rig that has them is visibly
	broken until they are removed. Returns the number removed.
	"""
	removed = 0
	for p_bone in b_armature_ob.pose.bones:
		for constraint in list(p_bone.constraints):
			if constraint.type == 'COPY_TRANSFORMS' and constraint.name == "Cobra Mirror Rig":
				p_bone.constraints.remove(constraint)
				removed += 1
	return removed
