import bpy
import bmesh

from . import matrix_util

def copy_ob(src_obj):
	new_obj = src_obj.copy()
	new_obj.data = src_obj.data.copy()
	new_obj.name = src_obj.name+"_copy"
	new_obj.animation_data_clear()
	bpy.context.scene.collection.objects.link(new_obj)
	bpy.context.view_layer.objects.active = new_obj
	return new_obj


def strip_shells_wrapper(shell_count=6):
	for ob in bpy.context.selected_objects:
		if ob.type == "MESH":
			strip_shells(ob, shell_count)

	
def create_fins_wrapper():
	msgs = []
	for lod_i in range(6):
		lod_group_name = "LOD"+str(lod_i)
		src_ob = get_ob_from_lod_and_flags(lod_group_name, flags=[885, 821, 1013, ])
		trg_ob = get_ob_from_lod_and_flags(lod_group_name, flags=[565, ])
		if src_ob and trg_ob:
			msgs.append(build_fins(src_ob, trg_ob))
	return msgs


def strip_shells(ob, shell_count=6):

	if "add_shells" in ob:
		if ob["add_shells"] == 5:
			raise AttributeError(f"Model {ob.name} has 'add_shells' set to 5 - can not remove shells from a mesh that has none")
	me = ob.data
	# Get a BMesh representation
	bm = bmesh.new()	 # create an empty BMesh
	bm.from_mesh(me)	 # fill it in from a Mesh

	sixth = (len(bm.faces)//shell_count)-1
	for i, face in enumerate(bm.faces):
		if i > sixth:
			bm.faces.remove(face)

	# Finish up, write the bmesh back to the mesh
	bm.to_mesh(me)
	bm.free()	 # free and prevent further access
	ob["add_shells"] = shell_count-1

	success = '\nFinished Shell generation'
	print(success)


def get_ob_from_lod_and_flags(lod_group_name, flags=[565, ]):
	for coll in bpy.data.collections:
		if lod_group_name in coll.name:
			for ob in coll.objects:
				if ob["flag"] in flags:
					return ob


def build_fins(src_ob, trg_ob):

	lod_group_name = matrix_util.get_lod(src_ob)
	ob = copy_ob(src_ob)

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
	mod.data_types_loops = { "CUSTOM_NORMAL", }

	me = ob.data
	# needed for custom normals
	me.use_auto_smooth = True
	# Get a BMesh representation
	bm = bmesh.new()	 # create an empty BMesh
	bm.from_mesh(me)	 # fill it in from a Mesh
	edges_start_a = bm.edges[:]
	faces = bm.faces[:]
	bm.faces.ensure_lookup_table()
	# Extrude and create geometry on side 'b'
	normals = [v.normal for v in bm.verts]
	ret = bmesh.ops.extrude_edge_only( bm, edges=edges_start_a)
	geom_extrude = ret["geom"]
	verts_extrude = [ele for ele in geom_extrude if isinstance(ele, bmesh.types.BMVert)]
	
	# move each extruded verts out across the surface normal
	for v, n in zip(verts_extrude, normals):
		v.co += (n*0.00001)

	# now delete all old faces, but only faces
	# We have to pass these as ints
	# DEL_VERTS = 1 DEL_EDGES = 2 DEL_ONLYFACES = 3 DEL_EDGESFACES = 4 DEL_FACES = 5 DEL_ALL = 6 DEL_ONLYTAGGED = 7
	bmesh.ops.delete(bm, geom=faces, context="FACES_ONLY")
	
	# build uv1 coords
	build_uv(ob, bm)

	# Finish up, write the bmesh back to the mesh
	bm.to_mesh(me)
	bm.free()	 # free and prevent further access

	# remove fur_length vgroup
	fl = "fur_length"
	if fl in ob.vertex_groups:
		vg = ob.vertex_groups[fl]
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
		current_face = strip[-1]
		current_face.tag = True
		link_faces = [f for e in current_face.edges for f in e.link_faces if f not in strip and not f.tag]
		if link_faces:
			# get the face whose orientation is most similar
			dots = [ (abs(current_face.normal.dot(f.normal)), f) for f in link_faces]
			dots.sort( key=lambda x:x[0])
			best_face = dots[-1][1]
			strip.append(best_face)
	return strip
	
def build_uv(ob, bm):
	
	# get vertex group index
	# this is stored in the object, not the BMesh
	group_index = ob.vertex_groups["fur_length"].index
	# print(group_index)

	# only ever one deform weight layer
	dvert_lay = bm.verts.layers.deform.active
	
	#get uv 1
	uv_lay = bm.loops.layers.uv["UV1"]
	# print(uv_lay)
		
	# face = bm.select_history.active
	for face in bm.faces:
		if not face.tag:
			ring = get_face_ring(face)
			
			# initial xpos for this strip of faces
			x_0 = 0
			for face in ring:
				
				# update X coords
				length = face.edges[0].calc_length()*6
				# left edges
				for loop in (face.loops[0],face.loops[3]):
					loop[uv_lay].uv.x = -16.0 + x_0
				# right edge
				for loop in (face.loops[1],face.loops[2]):
					loop[uv_lay].uv.x = -16.0 + x_0 + length
				x_0 += length
				
				# update Y coords
				# top edge
				for loop in face.loops[:2]:
					loop[uv_lay].uv.y = 1.00049
				# lower edge
				for loop in face.loops[2:]:
					vert = loop.vert
					
					dvert = vert[dvert_lay]

					if group_index in dvert:
						weight = dvert[group_index]
						loop[uv_lay].uv.y = 1-(weight*2)
			
	print("Finished UV generation")
	
if __name__ == "__main__":

	src_ob = bpy.data.objects["gray_wolf_male.mdl2_LOD0_model22"]
	build_fins(src_ob)
	src_ob = bpy.data.objects["gray_wolf_male.mdl2_LOD1_model23"]
	build_fins(src_ob)
