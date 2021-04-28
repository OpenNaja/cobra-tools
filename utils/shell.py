import bpy
import bmesh
import numpy as np
import mathutils

from . import matrix_util

# gauged from the average of grey wolf
# X_SCALE = 3.79
# x scale is variable per animal
# Y_SCALE = 1.82
X_START = -16.0
Y_START = 1.00049


def copy_ob(src_obj):
	new_obj = src_obj.copy()
	new_obj.data = src_obj.data.copy()
	new_obj.name = src_obj.name + "_copy"
	new_obj.animation_data_clear()
	bpy.context.scene.collection.objects.link(new_obj)
	bpy.context.view_layer.objects.active = new_obj
	return new_obj


def ob_processor_wrapper(func):
	msgs = ["Creating fins...", ]
	for lod_i in range(6):
		lod_group_name = f"LOD{lod_i}"
		coll = get_collection(lod_group_name)
		# src_ob = get_ob_from_lod_and_flags(coll, flags=[885, 821, 1013, ])
		# trg_ob = get_ob_from_lod_and_flags(coll, flags=[565, ])
		src_obs = [ob for ob in coll.objects if is_shell(ob)]
		trg_obs = [ob for ob in coll.objects if is_fin(ob)]
		if src_obs and trg_obs:
			msgs.append(func(src_obs[0], trg_obs[0]))
	return msgs


def create_fins_wrapper():
	return ob_processor_wrapper(build_fins)


def gauge_uv_scale_wrapper():
	return ob_processor_wrapper(gauge_uv_factors)


def get_collection(name):
	for coll in bpy.data.collections:
		if name in coll.name:
			return coll


def get_ob_from_lod_and_flags(coll, flags=(565,)):
	if coll:
		for ob in coll.objects:
			if "flag" in ob and ob["flag"] in flags:
				return ob


def build_fins(src_ob, trg_ob):
	try:
		uv_scale_x = src_ob["uv_scale_x"]
		uv_scale_y = src_ob["uv_scale_y"]
	except:
		raise AttributeError(f"{src_ob.name} has no UV scale properties. Run 'Gauge UV Scale' first!")

	lod_group_name = matrix_util.get_lod(src_ob)
	ob = copy_ob(src_ob)
	me = ob.data
	# transfer the material
	me.materials[0] = trg_ob.data.materials[0]
	# rename new object
	trg_name = trg_ob.name
	trg_ob.name += "dummy"
	ob.name = trg_name
	# delete old target
	bpy.data.objects.remove(trg_ob, do_unlink=True)

	# set up copy of normals from src mesh
	mod = ob.modifiers.new('DataTransfer', 'DATA_TRANSFER')
	mod.object = src_ob
	mod.use_loop_data = True
	mod.data_types_loops = {"CUSTOM_NORMAL", }

	# needed for custom normals
	me.use_auto_smooth = True
	# create uv1 layer for fins
	me.uv_layers.new(name="UV1")
	# Get a BMesh representation
	bm = bmesh.new()  # create an empty BMesh
	bm.from_mesh(me)  # fill it in from a Mesh
	edges_start_a = bm.edges[:]
	faces = bm.faces[:]
	bm.faces.ensure_lookup_table()
	# Extrude and create geometry on side 'b'
	normals = [v.normal for v in bm.verts]
	ret = bmesh.ops.extrude_edge_only(bm, edges=edges_start_a)
	geom_extrude = ret["geom"]
	verts_extrude = [ele for ele in geom_extrude if isinstance(ele, bmesh.types.BMVert)]

	# move each extruded verts out across the surface normal
	for v, n in zip(verts_extrude, normals):
		v.co += (n * 0.00001)

	# now delete all old faces, but only faces
	# We have to pass these as ints
	# DEL_VERTS = 1 DEL_EDGES = 2 DEL_ONLYFACES = 3 DEL_EDGESFACES = 4 DEL_FACES = 5 DEL_ALL = 6 DEL_ONLYTAGGED = 7
	bmesh.ops.delete(bm, geom=faces, context="FACES_ONLY")

	# build uv1 coords
	build_uv(ob, bm, uv_scale_x, uv_scale_y)

	# Finish up, write the bmesh back to the mesh
	bm.to_mesh(me)
	bm.free()  # free and prevent further access

	# remove fur_length vgroup
	for vg_name in ("fur_length", "fur_width"):
		if vg_name in ob.vertex_groups:
			vg = ob.vertex_groups[vg_name]
			ob.vertex_groups.remove(vg)
	ob["flag"] = 565

	# remove the particle system, since we no longer have a fur length vertex group
	for mod in ob.modifiers:
		if mod.type == "PARTICLE_SYSTEM":
			ob.modifiers.remove(mod)

	# only set the lod index here so that hiding it does not mess with any operators applied above
	matrix_util.to_lod(ob, None, lod=lod_group_name)

	return f'Generated fin geometry {trg_name} from {src_ob.name}'


def get_face_ring(face):
	strip = [face, ]
	for i in range(10):
		# get linked faces
		best_face = get_best_face(strip[-1])
		if best_face:
			strip.append(best_face)
		else:
			break
	return strip


def get_best_face(current_face):
	link_faces = [f for e in current_face.edges for f in e.link_faces if not f.tag and f is not current_face]
	# print(len(link_faces), len(set(link_faces)))
	if link_faces:
		# get the face whose orientation is most similar
		dots = [(abs(current_face.normal.dot(f.normal)), f) for f in link_faces]
		dots.sort(key=lambda x: x[0])
		# dot product = 0 -> vectors are orthogonal
		# we need parallel normals
		best_face = dots[-1][1]
		best_face.tag = True
		return best_face


def build_uv(ob, bm, uv_scale_x, uv_scale_y):
	# get vertex group index
	# this is stored in the object, not the BMesh
	group_index = ob.vertex_groups["fur_length"].index
	# print(group_index)

	psys_fac = ob.particle_systems[0].settings.hair_length

	# only ever one deform weight layer
	dvert_lay = bm.verts.layers.deform.active

	# get uv 1
	uv_lay = bm.loops.layers.uv["UV1"]

	for face_a in bm.faces:
		if not face_a.tag:
			ring = get_face_ring(face_a)
			# store the x position
			x_pos_dic = {}
			for face in ring:
				# update X coords
				length = face.edges[0].calc_length() * uv_scale_x
				# print(x_pos_dic)
				ind = face.loops[0].vert.index
				# print("ind", ind)
				if ind in x_pos_dic:
					# print("0 in, index", ind)
					left = (0, 3)
					right = (1, 2)
				else:
					# print("1 in, index", ind2)
					left = (1, 2)
					right = (0, 3)
				# fall back to start if top left vertex hasn't been keyed in the dict
				x_0 = x_pos_dic.get(face.loops[left[0]].vert.index, X_START)
				# left edges
				for i in left:
					loop = face.loops[i]
					loop[uv_lay].uv.x = x_0
					# print("left", loop.vert.index, x_0)
					x_pos_dic[loop.vert.index] = x_0
				# right edge
				for i in right:
					loop = face.loops[i]
					loop[uv_lay].uv.x = x_0 + length
					# print("right", loop.vert.index, x_0 + length)
					x_pos_dic[loop.vert.index] = x_0 + length

				# update Y coords
				# top edge
				for loop in face.loops[:2]:
					loop[uv_lay].uv.y = Y_START
				# lower edge
				for loop in face.loops[2:]:
					vert = loop.vert

					dvert = vert[dvert_lay]

					if group_index in dvert:
						weight = dvert[group_index]
						loop[uv_lay].uv.y = Y_START - (weight * psys_fac * uv_scale_y)
	print("Finished UV generation")


def gauge_uv_factors(src_ob, trg_ob):
	print(f"Gauging UV scale for {trg_ob.name}")
	vg = src_ob.vertex_groups["fur_length"]
	psys = src_ob.particle_systems[0]
	hair_length = psys.settings.hair_length

	# populate a KD tree with all verts from the base (shells) mesh
	src_me = src_ob.data
	size = len(src_me.vertices)
	kd = mathutils.kdtree.KDTree(size)
	for i, v in enumerate(src_me.vertices):
		kd.insert(v.co, i)
	kd.balance()

	x_facs = []
	y_facs = []
	trg_me = trg_ob.data
	for i, p in enumerate(trg_me.polygons):
		# print(p)
		base = []
		top = []
		for loop_index in p.loop_indices:
			uvs = [(layer.data[loop_index].uv.x, 1 - layer.data[loop_index].uv.y) for layer in trg_me.uv_layers]
			# print(uvs)
			if uvs[1][1] < 0:
				base.append(loop_index)
			else:
				top.append(loop_index)

		if len(base) == 2:
			# print(base)
			uv_verts = [trg_me.uv_layers[1].data[loop_index].uv.x for loop_index in base]
			uv_len = abs(uv_verts[1] - uv_verts[0])
			# print(uv_len)
			loops = [trg_me.loops[loop_index] for loop_index in base]
			me_verts = [trg_me.vertices[loop.vertex_index].co for loop in loops]
			v_len = (me_verts[1] - me_verts[0]).length
			# print(v_len)
			# print("Fac", uv_len/v_len)
			if v_len:
				x_facs.append(uv_len / v_len)

		if base and top:
			uv_verts = [trg_me.uv_layers[1].data[loop_index].uv.y for loop_index in (base[0], top[0])]
			uv_height = abs(uv_verts[1] - uv_verts[0])
			# print(uv_height)

			# find the closest vert on base shell mesh
			loop = trg_me.loops[base[0]]
			find_co = trg_me.vertices[loop.vertex_index].co
			co, index, dist = kd.find(find_co)
			vert = src_me.vertices[index]
			for vertex_group in vert.groups:
				vgroup_name = src_ob.vertex_groups[vertex_group.group].name
				if vgroup_name == "fur_length":
					base_fur_length = vertex_group.weight * hair_length
					if base_fur_length:
						y_facs.append(uv_height / base_fur_length)
				# if vgroup_name == "fur_width":
				# 	base_fur_width = vertex_group.weight
		# print("Close to center:", co, index, dist, find_co)
	#    if i == 20:
	#        break
	uv_scale_x = np.mean(x_facs)
	uv_scale_y = np.mean(y_facs)
	src_ob["uv_scale_x"] = uv_scale_x
	src_ob["uv_scale_y"] = uv_scale_y
	# print(base_fur_width, uv_scale_x/base_fur_width)
	return f"Found UV scale ({uv_scale_x}, {uv_scale_y})"


def is_fin(ob):
	return "_fur_fin" in ob.data.materials[0].name.lower()


def is_shell(ob):
	return "_fur_shell" in ob.data.materials[0].name.lower()

