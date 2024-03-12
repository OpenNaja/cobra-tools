import logging

import bpy
import mathutils
import bmesh
from mathutils import Vector, Quaternion, Matrix

from plugin.modules_import.armature import set_transform4, append_armature_modifier
from plugin.modules_import.collision import parent_to
from plugin.utils.matrix_util import vectorisclose
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


def apply_armature_all():
	# Check if the active object is a valid armature
	if bpy.context.active_object.type != 'ARMATURE':
		# Object is not an armature. Cancelling.
		return f"No armature selected.",

	# Get the armature
	b_armature_ob = bpy.context.object
	apply_pose_to_meshes(b_armature_ob)
	bpy.ops.pose.armature_apply()
	return ()


def add_hitcheck_to_mdl2(obj, collection, parent):
	""" Creates a hitcheck bounding volume box """

	# get the bounding box of the original object
	bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
	edges = [(0, 1), (0, 3), (0, 4), (1, 5), (3, 7), (2, 1), (2, 6), (2, 3), (4, 5), (4, 7), (7, 6), (5, 6)]

	mesh_name = obj.name + "_PhysicsVolume"
	hitcheck_me = bpy.data.meshes.new(mesh_name)
	hitcheck_me.from_pydata(bbox_corners, edges, [])

	# Create all the mesh data
	bm = bmesh.new()
	bm.from_mesh(hitcheck_me)
	bm.to_mesh(hitcheck_me)
	bm.free()

	hitcheck_ob = create_ob(bpy.context.scene, mesh_name, hitcheck_me, coll=collection)

	# rotate
	hitcheck_ob.rotation_euler[2] = 1.5708

	# center
	x = (bbox_corners[4][0] + bbox_corners[0][0]) / 2  # invert x axis
	y = (bbox_corners[3][1] + bbox_corners[0][1]) / -2
	z = (bbox_corners[2][2] + bbox_corners[0][2]) / 2
	vec_loc = Vector((y, x, z))
	hitcheck_ob.location = hitcheck_ob.location + vec_loc

	# Assign parent joint
	hitcheck_ob.parent = parent

	bpy.context.view_layer.objects.active = hitcheck_ob
	bpy.ops.rigidbody.object_add()

	hitcheck_ob.rigid_body.type = 'PASSIVE'
	hitcheck_ob.rigid_body.collision_shape = 'BOX'
	hitcheck_ob.rigid_body.mesh_source = 'BASE'

	hitcheck_ob.cobra_coll.flag = 'STATIC'

	hitcheck_ob.cobra_coll.classification_jwe2 = 'Prop'
	hitcheck_ob.cobra_coll.surface_jwe2 = 'PropWooden'

	hitcheck_ob.cobra_coll.classification_pz = 'Scenery'
	hitcheck_ob.cobra_coll.surface_pz = 'Wood'


def setup_rig(add_armature=True, add_physics=True):
	b_ob = bpy.context.active_object
	scene = bpy.context.scene
	name = b_ob.name

	# create collections
	mdl2_coll = create_collection(name, scene.collection)
	lod_coll = create_collection(f"{name}_L0", mdl2_coll)
	# move b_ob to L0 collection
	for coll in b_ob.users_collection:
		coll.objects.unlink(b_ob)
	lod_coll.objects.link(b_ob)

	# rename b_ob to the right lod (just cosmetic)
	b_ob.name += '_ojb0_L0'
	if add_armature:
		# create armature
		armature_name = f"{name}_Armature"
		b_armature_data = bpy.data.armatures.new(armature_name)
		b_armature_data.display_type = 'STICK'
		b_armature_ob = create_ob(scene, armature_name, b_armature_data, coll=mdl2_coll)
		b_armature_ob.show_in_front = True

		# make armature editable and create bones
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		bone_name = "def_c_root_joint"
		b_edit_bone = b_armature_data.edit_bones.new(bone_name)
		b_edit_bone["long_name"] = bone_name
		# identity transform in ms2 space
		b_edit_bone.head = (0, 0, 0)
		b_edit_bone.tail = (1, 0, 0)
		b_edit_bone.roll = 0.0
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

		# weight paint mesh to bone
		b_ob.vertex_groups.new(name=bone_name)
		b_ob.vertex_groups[bone_name].add(list(range(len(b_ob.data.vertices))), 1.0, 'REPLACE')
		# link to armature, only after mirror so the order is good and weights are mirrored
		append_armature_modifier(b_ob, b_armature_ob)

		if add_physics:
			joint_coll = create_collection(f"{name}_joints", mdl2_coll)
			# add physics joint
			b_joint = create_ob(scene, f"{name}_Physics_Joint", None, coll=joint_coll)
			parent_to(b_armature_ob, b_joint, bone_name)

			# create hitcheck object
			add_hitcheck_to_mdl2(b_ob, joint_coll, b_joint)
	return ()


def generate_rig_edit(**kwargs):
	"""Automatic rig edit generator by NDP. Detects posed bones and automatically generates nodes and offsets them."""
	# Initiate logging
	msgs = []
	# logging.info(f"-------------------------------------------------------------")
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
			msgs.append(f"Warning: {str(p_bone.name)} had scale transforms. Reset scale for all bones and try again.")
			return msgs

		# We check for NODE bones with transforms and skip them.
		if (not vectorisclose(p_bone.location, VEC3_0, errortolerance) or not vectorisclose(
				p_bone.scale, VEC3_1, errortolerance) or not vectorisclose(
				Vector(p_bone.rotation_quaternion), VEC4_1, errortolerance)) and p_bone.name.startswith(
				"NODE_"):
			# Ignore posed NODE bones and proceed to the next, their offsets can be applied directly.
			editnumber = editnumber + 1
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
		set_transform4(bonenode_matrix_local, bonenode)

		# Restore length
		bonenode.length = nodelength

		# Node completed. Log number of edits.
		editnumber = editnumber + 1
		# Node creation complete
		logging.info(f"created node: {bonenode.name}")
	# logging.info(f"node matrix:")
	# logging.info(f"{bonenode.matrix}")

	bpy.ops.object.mode_set(mode='POSE')

	# Creating node groups to delete

	if mergenodes:
		# Checking for duplicates to merge
		logging.info(f"creating node_groups to merge")
		# Initiate list
		node_list = []

		# We create a list of all NODES
		for p_bone in b_armature_ob.pose.bones:
			if p_bone.name.startswith("NODE_"):
				node_list.append(p_bone)

		# Create NODE parent dictionary
		node_groups = {}

		# Create and sort NODE groups, we create a dictionary with a tuple of: parent,rounded matrix as the key. This way we can group identical nodes.
		for p_bone in node_list:
			# We create a rounded matrix to create leeway for miniscule variation
			rounded_matrix = tuple(tuple(round(element, 5) for element in row) for row in p_bone.bone.matrix_local)
			# logging.info(f"node matrix: {p_bone.bone.matrix_local}")
			# logging.info(f"rounded matrix: {rounded_matrix}")

			# We use the parent and rounded matrix as a key to sort all identical nodes into groups
			keytuple = (p_bone.parent, rounded_matrix)
			if keytuple in node_groups:
				node_groups[keytuple].append(p_bone)
			else:
				node_groups[keytuple] = [p_bone]

		# Log node groups
		for nodegroup in node_groups:
			logging.info(f"node group: {nodegroup}")
			for node in node_groups[nodegroup]:
				logging.info(f"node: {node.name}")

		# store number of deleted nodes
		deletednodes = 0

		# Merge node groups
		for nodegroup in node_groups:
			# Rename NODE to indicate it owns more than one bone
			if len(node_groups[nodegroup]) > 1:
				# Renaming to be more descriptive
				if not node_groups[nodegroup][0].parent:
					node_groups[nodegroup][0].name = f"NODE_{len(node_groups[nodegroup])}GROUP_ROOTNODE"
				else:
					node_groups[nodegroup][
						0].name = f"NODE_{len(node_groups[nodegroup])}GROUP_{node_groups[nodegroup][0].parent.name}"

			# Log group organization
			# logging.info(f"first node: {node_groups[nodegroup][0].name}")
			# logging.info(f"first child: {node_groups[nodegroup][0].children[0].name}")

			# Delete all extra nodes
			for node in node_groups[nodegroup]:
				if node != node_groups[nodegroup][0]:
					# logging.info(f"secondary node: {node.name}")
					# logging.info(f"secondary child: {node.children[0].name}")

					# Switch to edit mode to edit the parents
					bpy.ops.object.mode_set(mode='EDIT')

					# Reparent duplicate basebones to the first node
					b_armature_ob.data.edit_bones.get(node.children[0].name).parent = b_armature_ob.data.edit_bones.get(
						node_groups[nodegroup][0].name)

					# Delete the duplicate nodes
					deletednodes = deletednodes + 1
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
		msgs.append(
			f"Warning: Total amount of bones exceeds 254 after rig edit, game will crash. Please undo, reduce the number of edits, and try again.")
		return msgs

	# Return count of succesfull rig edits
	msgs.append(f"{editnumber} rig edits generated succesfully")
	return msgs


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


def convert_scale_to_loc():
	"""Automatically convert scaled bones into equivalent visual location transforms"""
	# Function for converting scale to visual location transforms in pose mode
	# Initiate logging
	msgs = []
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

	if editnumber > 0:
		msgs.append(f"Moved {editnumber} bones to their visual locations and reset scales")
	else:
		msgs.append(f"No bones required movement.")

	# Return to original mode
	bpy.ops.object.mode_set(mode=original_mode)

	return msgs
