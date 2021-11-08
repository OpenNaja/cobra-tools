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
	return None


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


def comb_common():
	context = bpy.context
	ob = context.object
	if not ob:
		raise AttributeError("No object in context")
	# particle edit mode has to be entered so that hair strands are generated
	# otherwise the non-eval ob's particle count is 0
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
		raise IndexError(
			f"Mesh has {len(vertices)} vertices, while particle system has {num_particles}. "
			f"Adjust the particle system's vertex count and try again.")
	# tangents have to be pre-calculated
	# this will also calculate loop normal
	me.calc_tangents()
	return me, ob_eval, particle_modifier_eval, particle_system, particle_system_eval


def vcol_to_comb():
	me, ob_eval, particle_modifier_eval, particle_system, particle_system_eval = comb_common()
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
			num_hair_keys = len(particle_eval.hair_keys)
			for hair_key_index in range(num_hair_keys):
				hair_key = particle.hair_keys[hair_key_index]
				hair_key.co_object_set(ob_eval, particle_modifier_eval, particle_eval, root.lerp(tip, hair_key_index/(num_hair_keys-1)))

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
			num_hair_keys = len(particle_eval.hair_keys)

			root = particle.hair_keys[0].co_object(ob_eval, particle_modifier_eval, particle_eval)
			tip = particle.hair_keys[num_hair_keys - 1].co_object(ob_eval, particle_modifier_eval, particle_eval)

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
