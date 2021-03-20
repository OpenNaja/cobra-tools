import bpy


def find_modifier_for_particle_system(object, particle_system):
	for modifier in object.modifiers:
		if modifier.type != "PARTICLE_SYSTEM":
			continue
		if modifier.particle_system == particle_system:
			return modifier
	return None


def mesh_to_hair(depsgraph, mesh_object, hair_object, particle_system):
	particle_modifier = find_modifier_for_particle_system(hair_object, particle_system)

	hair_object_eval = hair_object.evaluated_get(depsgraph)
	particle_modifier_eval = hair_object_eval.modifiers[particle_modifier.name]
	particle_system_eval = particle_modifier_eval.particle_system

	mesh = mesh_object.data
	vertices = mesh.vertices

	num_particles = len(particle_system.particles)
	vertex_index = 0
	for particle_index in range(num_particles):
		particle = particle_system.particles[particle_index]
		particle_eval = particle_system_eval.particles[particle_index]
		num_hair_keys = len(particle_eval.hair_keys)
		for hair_key_index in range(num_hair_keys):
			co = vertices[vertex_index].co
			hair_key = particle.hair_keys[hair_key_index]
			hair_key.co_object_set(hair_object_eval, particle_modifier_eval, particle_eval, co)
			vertex_index += 1


def mesh_to_hair_test():
	context = bpy.context
	hair_object = bpy.data.objects["Plane"]
	particle_system = hair_object.particle_systems["ParticleSettings"]
	mesh_object = bpy.data.objects["Plane-ParticleSettings"]

	depsgraph = context.evaluated_depsgraph_get()

	mesh_object_eval = mesh_object.evaluated_get(depsgraph)

	mesh_to_hair(depsgraph, mesh_object_eval, hair_object, particle_system)


# mesh_to_hair_test()


def add_psys(ob):
	name = "hair"
	ps_mod = ob.modifiers.new(name, 'PARTICLE_SYSTEM')
	psys = ob.particle_systems[ps_mod.name]
	psys.settings.count = len(ob.data.vertices)
	psys.settings.type = 'HAIR'
	psys.settings.emit_from = 'VERT'
	psys.settings.use_emit_random = False
	psys.settings.hair_length = 1.0
	psys.vertex_group_length = "fur_length"
	psys.settings.hair_step = 1
	psys.settings.display_step = 1
