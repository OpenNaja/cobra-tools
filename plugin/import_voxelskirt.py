import os
import time
import bpy
from struct import unpack_from, iter_unpack, calcsize
# from .common_bfb import *
import numpy as np

def generate_mesh(x_verts, y_verts, scale, heights):
	verts=[]
	i=0
	for y in range(y_verts):
		for x in range(x_verts):
			verts.append((x*scale, y*scale, heights[i]-7),)
			i+=1
	quads=[]
	i=0
	for x in range(x_verts-1):
		for y in range(y_verts-1):
			quads.append((i+1,i,i+y_verts,i+y_verts+1))
			i+=1
		i+=1
	return verts, quads

def create_ob(ob_name, ob_data):
	ob = bpy.data.objects.new(ob_name, ob_data)
	bpy.context.scene.collection.objects.link(ob)
	bpy.context.view_layer.objects.active = ob
	return ob

def mesh_from_data(name, verts, faces, wireframe=True):
	me = bpy.data.meshes.new(name)
	me.from_pydata(verts, [], faces)
	me.update()
	ob = create_ob(name, me)
	# if wireframe:
	# 	ob.draw_type = 'WIRE'
	return ob, me


def load(operator, context, filepath = ""):
	starttime = time.clock()
	errors = []
	
	sculpt_settings = bpy.context.scene.tool_settings.sculpt
	sculpt_settings.lock_x = True
	sculpt_settings.lock_y = True
	
	#when no object exists, or when we are in edit mode when script is run
	try: bpy.ops.object.mode_set(mode='OBJECT')
	except: pass
	
	print("\nImporting",os.path.basename(filepath))
	with open(filepath, 'rb') as stream:

		header = stream.read(120)
		info = unpack_from('30I', header)
		print(info)
		x = info[4]
		y = info[6]
		print(x,y)

		heightmap = np.fromfile(stream, dtype=np.float32, count=x*y)
		# print(heightmap)
	verts, quads = generate_mesh(x, y, 1.0, heightmap)
	map_ob, me = mesh_from_data("map", verts, quads, False)
	# for face in me.polygons:
	# 	face.use_smooth = True

	success = 'Finished DAT Import in %.2f seconds\n' %(time.clock()-starttime)
	print(success)
	return errors