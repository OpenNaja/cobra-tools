import bpy
import mathutils
import math
import logging

from plugin.utils.matrix_util import evaluate_mesh

# a bit of safety to avoid breaking normalization
FAC = 1.9


def find_modifier_for_particle_system(b_ob, particle_system):
	for modifier in b_ob.modifiers:
		if modifier.type != "PARTICLE_SYSTEM":
			continue
		if modifier.particle_system == particle_system:
			return modifier


def add_psys(ob, model):
	name = "hair"
	ps_mod = ob.modifiers.new(name, 'PARTICLE_SYSTEM')
	psys = ob.particle_systems[ps_mod.name]
	psys.settings.count = len(ob.data.vertices)
	psys.settings.type = 'HAIR'
	psys.settings.emit_from = 'VERT'
	psys.settings.use_emit_random = False
	psys.settings.hair_length = model.fur_length
	psys.vertex_group_length = "fur_length"
	psys.settings.hair_step = 1
	psys.settings.display_step = 1


def comb_common(adjust_psys_count=False, warn=True):
	ob = bpy.context.active_object
	if not ob:
		raise AttributeError("No object in context")
	# particle edit mode has to be entered so that hair strands are generated
	# otherwise the non-eval ob's particle count is 0
	if not ob.particle_systems:
		raise AttributeError(f"No particle system on {ob.name}")
	logging.debug(f"comb_common on object '{ob.name}'")
	bpy.ops.object.mode_set(mode='PARTICLE_EDIT')
	bpy.ops.object.mode_set(mode='OBJECT')
	ob_eval, me_eval = evaluate_mesh(ob)
	me = ob.data
	particle_system = ob.particle_systems[0]
	particle_modifier = find_modifier_for_particle_system(ob, particle_system)
	particle_modifier_eval = ob_eval.modifiers[particle_modifier.name]
	particle_system_eval = ob_eval.particle_systems[0]
	vertices = me.vertices
	num_particles = len(particle_system.particles)
	num_particles2 = len(particle_system_eval.particles)
	assert num_particles == num_particles2
	if not (len(vertices) == num_particles):
		if not adjust_psys_count:
			if warn:
				raise IndexError(
					f"Mesh '{ob.name}' has {len(vertices)} vertices, while particle system has {num_particles}. "
					f"Adjust the particle system's vertex count and try again.")
		else:
			logging.warning(f"Changed {ob.name}'s particle count to {len(vertices)} to match vertices")
			# set particle count on non evaluated mesh, and start over
			bpy.ops.particle.edited_clear()
			particle_system.settings.count = len(vertices)
			return comb_common()
	# tangents have to be pre-calculated
	# this will also calculate loop normal
	me.calc_tangents()
	return me, ob_eval, particle_modifier_eval, particle_system, particle_system_eval


def vcol_to_comb():
	me, ob_eval, particle_modifier_eval, particle_system, particle_system_eval = comb_common(adjust_psys_count=True)
	# loop faces
	vcol_layer = me.vertex_colors[0].data
	for i, face in enumerate(me.polygons):
		# loop over face loop
		for loop_index in face.loop_indices:
			vert = me.loops[loop_index]
			vertex = me.vertices[vert.vertex_index]
			tangent_space_mat = get_tangent_space_mat(vert)
			vcol = vcol_layer[loop_index].color
			r = (vcol[0] - 0.5)*FAC
			# g = (vcol[1] - 0.5)*FAC
			b = (vcol[2] - 0.5)*FAC
			# not sure what this does, kinda random
			# a = (vcol[3] - 0.5)*FAC
			# print((r * r) + (b * b) + (g*g), (b * b) + (r * r))
			try:
				# calculate third component for unit vector
				# z = math.sqrt((r * r) + (b * b) - 1)
				z = math.sqrt(1 - (r * r) - (b * b))
			except:
				# print("EXCEPT", r, b, a, (r * r) + (b * b) - 1)
				z = 0
			# n = math.sqrt((r * r + b * b + z * z))
			# print("normalized", n)
			# this is the raw vector, in tangent space
			# this is like uv, so we do 1-v
			vec = mathutils.Vector((r, -b, z))

			# convert to object space
			hair_direction = tangent_space_mat @ vec
			# print("t+v+g", tangent, vec, dir)
			# print("dir",dir, vec)

			# calculate root and tip of the hair
			root = vertex.co
			tip = vertex.co + (hair_direction * particle_system.settings.hair_length)

			particle = particle_system.particles[vert.vertex_index]
			particle_eval = particle_system_eval.particles[vert.vertex_index]
			set_hair_keys(particle, particle_eval, ob_eval, particle_modifier_eval, root, tip)

	return f"Converted Vertex Color to Combing for {ob_eval.name}",


def comb_to_vcol():
	me, ob_eval, particle_modifier_eval, particle_system, particle_system_eval = comb_common()
	# loop faces
	vcol_layer = me.vertex_colors[0].data
	for i, face in enumerate(me.polygons):
		# loop over face loop
		for loop_index in face.loop_indices:
			vert = me.loops[loop_index]
			tangent_space_mat = get_tangent_space_mat(vert)

			particle = particle_system.particles[vert.vertex_index]
			particle_eval = particle_system_eval.particles[vert.vertex_index]
			root, tip = get_hair_keys(particle, particle_eval, ob_eval, particle_modifier_eval)
			hair_direction = (tip - root).normalized()
			vec = tangent_space_mat.inverted() @ hair_direction
			vcol = vcol_layer[loop_index].color
			vcol[0] = (vec.x/FAC) + 0.5
			vcol[2] = -(vec.y/FAC) + 0.5
	return f"Converted Combing to Vertex Color for {ob_eval.name}",


def get_tangent_space_mat(vert):
	tangent = vert.tangent
	normal = vert.normal
	bitangent = vert.bitangent_sign * normal.cross(tangent)
	tangent_space_mat = mathutils.Matrix((tangent, bitangent, normal)).transposed()
	# print(tangent_space_mat)
	# print(normal, tangent, bitangent)
	return tangent_space_mat


def transfer_hair_combing():
	src_ob = bpy.context.object
	trg_obs = [ob for ob in bpy.context.selected_objects if ob != src_ob]
	logging.info(f"Transferring hair combing from {src_ob.name}, preparing for {len(trg_obs)} targets")
	src_me, src_ob_eval, src_particle_modifier_eval, src_particle_system, src_particle_system_eval = comb_common(adjust_psys_count=False, warn=False)

	# populate a KD tree with all hair key roots
	# these are not guaranteed to match
	size = len(src_particle_system_eval.particles)
	# print(f"Size {size} {src_particle_system_eval.settings.count}")
	kd = mathutils.kdtree.KDTree(size)

	for i, particle in enumerate(src_particle_system_eval.particles):
		root_hair_key = particle.hair_keys[0]
		# print(i, root_hair_key.co)
		kd.insert(root_hair_key.co, i)
	kd.balance()

	for trg_ob in trg_obs:
		logging.info(f"Transferring hair combing from {src_ob.name} to {trg_ob.name}")
		bpy.context.view_layer.objects.active = trg_ob
		trg_me, trg_ob_eval, trg_particle_modifier_eval, trg_particle_system, trg_particle_system_eval = comb_common(adjust_psys_count=True)

		for trg_i, trg_particle in enumerate(trg_particle_system.particles):
			# get the properties of the target particle that we want to change
			trg_particle_eval = trg_particle_system_eval.particles[trg_i]
			trg_root, trg_tip = get_hair_keys(trg_particle, trg_particle_eval, trg_ob_eval, trg_particle_modifier_eval)
			# trg_len = (trg_tip - trg_root).length
			co, src_i, dist = kd.find(trg_root)
			# print(trg_i, co, src_i, dist)
			# now find the best corresponding source particle
			src_particle = src_particle_system.particles[src_i]
			src_particle_eval = src_particle_system_eval.particles[src_i]
			src_root, src_tip = get_hair_keys(src_particle, src_particle_eval, src_ob_eval, src_particle_modifier_eval)
			src_direction = (src_tip - src_root)  # .normalized() * trg_len
			trg_tip = trg_root + src_direction
			# change the target particle
			set_hair_keys(trg_particle, trg_particle_eval, trg_ob_eval, trg_particle_modifier_eval, trg_root, trg_tip)
	return f"Finished hair transfer",


def get_hair_keys(particle, particle_eval, ob_eval, particle_modifier_eval):
	"""Gets the evaluated coordinated for a particle's root and tip"""
	num_hair_keys = len(particle_eval.hair_keys)
	root = particle.hair_keys[0].co_object(ob_eval, particle_modifier_eval, particle_eval)
	tip = particle.hair_keys[num_hair_keys - 1].co_object(ob_eval, particle_modifier_eval, particle_eval)
	return root, tip


def set_hair_keys(particle, particle_eval, ob_eval, particle_modifier_eval, root, tip):
	"""Linearly interpolate coordinates for hair keys of particle from root to tip"""
	num_hair_keys = len(particle_eval.hair_keys)
	for hair_key_index in range(num_hair_keys):
		hair_key = particle.hair_keys[hair_key_index]
		co = root.lerp(tip, hair_key_index / (num_hair_keys - 1))
		hair_key.co_object_set(ob_eval, particle_modifier_eval, particle_eval, co)