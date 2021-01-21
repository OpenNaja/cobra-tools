import bpy
import time


def mesh_from_data(name, verts, faces, wireframe=True):
	me = bpy.data.meshes.new(name)
	start_time = time.time()
	me.from_pydata(verts, [], faces)
	print(f"from_pydata() took {time.time()-start_time:.2f} seconds for {len(verts)} verts")
	me.update()
	ob = create_ob(name, me)
	# if wireframe:
	# 	ob.draw_type = 'WIRE'
	return ob, me


def create_ob(ob_name, ob_data):
	ob = bpy.data.objects.new(ob_name, ob_data)
	bpy.context.scene.collection.objects.link(ob)
	bpy.context.view_layer.objects.active = ob
	return ob
