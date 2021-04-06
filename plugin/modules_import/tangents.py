from plugin.helpers import mesh_from_data
from plugin.import_mdl2 import eval_me
from utils.shell import get_ob_from_lod_and_flags


def visualize_tangents(name, verts, normals, tangents):
	out_verts = []
	out_faces = []
	v_len = 0.01
	for i, (v, n, t) in enumerate(zip(verts, normals, tangents)):
		out_verts.append(v)
		out_verts.append(v+v_len*n)
		out_verts.append(v+v_len*t)
		out_faces.append((i * 3, i*3 + 1, i * 3 + 2))
	return mesh_from_data(f"{name}_Tangents", out_verts, out_faces, wireframe=False)


def create_tangents():

	for lod_i in range(6):
		lod_group_name = "LOD" + str(lod_i)
		src_ob = get_ob_from_lod_and_flags(lod_group_name, flags=[885, 821, 1013, ])
		trg_ob = get_ob_from_lod_and_flags(lod_group_name, flags=[565, ])

		eval_ob_src, me_src = eval_me(src_ob)
		eval_ob_trg, me_trg = eval_me(trg_ob)

		# tangents have to be pre-calculated
		# this will also calculate loop normal
		me_trg.calc_tangents()
		me_src.calc_tangents()
		# calc_tangents(me)

		kd = fill_kd_tree(me_src)
		# stores values retrieved from blender, will be packed into array by pyffi
		verts = []
		normals = []
		tangents = []

		uv = me_trg.uv_layers[0].data
		# loop faces and collect unique and repeated vertices
		for face in me_trg.polygons:
			# loop over face loop to get access to face corner data (normals, uvs, vcols, etc)
			for loop_index in face.loop_indices:
				b_loop = me_trg.loops[loop_index]
				b_vert = me_trg.vertices[b_loop.vertex_index]

				uv_co = uv[b_loop.index].uv.to_3d()
				co, index, dist = kd.find(uv_co)
				src_tangent = me_src.loops[index].tangent
				# get the vectors
				verts.append(b_vert.co)
				tangents.append(src_tangent)
				normals.append(b_loop.normal)
		ob2, me2 = visualize_tangents(trg_ob.name+"Gen", verts, normals, tangents)


def fill_kd_tree(me):
	size = len(me.loops)
	kd = mathutils.kdtree.KDTree(size)
	uv_layer = me.uv_layers[0].data
	for i, loop in enumerate(me.loops):
		kd.insert(uv_layer[loop.index].uv.to_3d(), i)
	kd.balance()
	return kd


def calc_tangents_custom(me):
	# See "Tangent Space Calculation" at http://www.terathon.com/code/tangent.html
	# for v in me.vertices:
	# 	v.tangent = mathutils.Vector((0.0, 0.0, 0.0))
	# 	v.bitangent = mathutils.Vector((0.0, 0.0, 0.0))
	# for (v0, v1, v2) in me.tris:
	# 	dco1 = v1.coord - v0.coord
	# 	dco2 = v2.coord - v0.coord
	# 	duv1 = v1.uv - v0.uv
	# 	duv2 = v2.uv - v0.uv
	# 	tangent = dco2 * duv1.y - dco1 * duv2.y
	# 	bitangent = dco2 * duv1.x - dco1 * duv2.x
	# 	if dco2.cross(dco1).dot(bitangent.cross(tangent)) < 0:
	# 		tangent.negate()
	# 		bitangent.negate()
	# 	v0.tangent += tangent
	# 	v1.tangent += tangent
	# 	v2.tangent += tangent
	# 	v0.bitangent += bitangent
	# 	v1.bitangent += bitangent
	# 	v2.bitangent += bitangent
	# for v in self.verts:
	# 	v.tangent = v.tangent - v.normal * v.tangent.dot(v.normal)
	# 	v.tangent.normalize()
	# 	if v.normal.cross(v.tangent).dot(v.bitangent) < 0:
	# 		v.bitangent = -1.0
	# 	else:
	# 		v.bitangent = 1.0

	tangents = [mathutils.Vector((0.0, 0.0, 0.0)) for _ in range(len(me.loops))]
	bitangents = [mathutils.Vector((0.0, 0.0, 0.0)) for _ in range(len(me.loops))]
	# loop faces and collect unique and repeated vertices
	for face in me.polygons:
		assert len(face.loop_indices) == 3
		# loop over face loop to get access to face corner data (normals, uvs, vcols, etc)
		l0, l1, l2 = [me.loops[loop_index] for loop_index in face.loop_indices]
		# get vert coords
		v0 = me.vertices[l0.vertex_index]
		v1 = me.vertices[l1.vertex_index]
		v2 = me.vertices[l2.vertex_index]
		dco1 = v1.co - v0.co
		dco2 = v2.co - v0.co

		uv = me.uv_layers[0].data
		duv1 = uv[l1.index].uv - uv[l0.index].uv
		duv2 = uv[l2.index].uv - uv[l0.index].uv
		tangent = dco2 * duv1.y - dco1 * duv2.y
		bitangent = dco2 * duv1.x - dco1 * duv2.x
		if dco2.cross(dco1).dot(bitangent.cross(tangent)) < 0:
			tangent.negate()
			bitangent.negate()
		for loop_index in face.loop_indices:
			tangents[loop_index] += tangent
			bitangents[loop_index] += bitangent
	for tangent in tangents:
		tangent.normalize()
		# v.tangent = v.tangent - v.normal * v.tangent.dot(v.normal)
		# for loop_index in face.loop_indices:
		# 	b_loop = me.loops[loop_index]
		# 	b_vert = me.vertices[b_loop.vertex_index]
		#
		# 	b_loop.tangent = mathutils.Vector((0.0, 0.0, 0.0))
		# 	b_loop.bitangent = mathutils.Vector((0.0, 0.0, 0.0))
		# 	# # get the vectors
		# 	# position = b_vert.co
		# 	# tangent = b_loop.tangent
		# 	# normal = b_loop.normal
		# 	# uvs = [(layer.data[loop_index].uv.x, 1 - layer.data[loop_index].uv.y) for layer in me.uv_layers]