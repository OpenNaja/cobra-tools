import os

import bpy
import mathutils

from generated.formats.ms2.compounds.packing_utils import unpack_swizzle
from generated.formats.spl.compounds.SplRoot import SplRoot


def unpack(v, s):
	return mathutils.Vector(unpack_swizzle([i * s for i in (v.x, v.y, v.z)]))


def save(filepath=""):
	# get selected curve ob
	ob = bpy.context.object
	curve_data = ob.data
	if ob.type != "CURVE":
		raise AttributeError(f"Can only export curve objects")
	# export
	# in_dir, spl_name = os.path.split(filepath)
	# spl_basename, ext = os.path.splitext(spl_name)
	#
	# spl_root = SplRoot.from_xml_file(filepath, None)
	#
	# # create the Curve Datablock
	# curve_data = bpy.data.curves.new(spl_basename, type='CURVE')
	# curve_data.dimensions = '3D'
	# curve_data.resolution_u = 12
	#
	# # map coords to spline
	# polyline = curve_data.splines.new('BEZIER')
	# spline_data = spl_root.spline_data.data
	# # one key exists in the newly created curve
	# polyline.bezier_points.add(len(spline_data.keys)-1)
	# # https://docs.blender.org/api/current/bpy.types.BezierSplinePoint.html?highlight=bezier#bpy.types.BezierSplinePoint
	# for key, bezier in zip(spline_data.keys, polyline.bezier_points):
	#     # x, y, z = coord
	#     bezier.co = unpack(key.pos, spline_data.scale)
	#     bezier.handle_left = bezier.co + unpack(key.handle_left, key.handle_scale)
	#     bezier.handle_right = bezier.co + unpack(key.handle_right, key.handle_scale)
	#
	# # create Object
	# ob = bpy.data.objects.new(spl_basename, curve_data)
	# # maybe add it to bezier.co instead?
	# ob.location = unpack(spline_data.offset, 1.0)
	# # attach to scene and validate context
	# scene = bpy.context.scene
	# scene.collection.objects.link(ob)

	spl_header = SplRoot(context=object())
	SplRoot.to_xml_file(spl_header, filepath)
	return f"Finished SPL export",
