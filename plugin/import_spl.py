import os

import bpy
import mathutils

from generated.formats.ms2.structs.packing_utils import unpack_swizzle
from generated.formats.spl.structs.SplRoot import SplRoot


def unpack(v, s):
    return mathutils.Vector(unpack_swizzle([i * s for i in (v.x, v.y, v.z)]))


def load(reporter, filepath=""):
    in_dir, spl_name = os.path.split(filepath)
    spl_basename, ext = os.path.splitext(spl_name)

    spl_root = SplRoot.from_xml_file(filepath, None)

    # create the Curve Datablock
    b_cu = bpy.data.curves.new(spl_basename, type='CURVE')
    b_cu.dimensions = '3D'
    b_cu.resolution_u = 12

    # map coords to spline
    b_spline = b_cu.splines.new('BEZIER')
    spline_data = spl_root.spline_data.data
    # one key exists in the newly created curve
    b_spline.bezier_points.add(len(spline_data.keys)-1)
    # https://docs.blender.org/api/current/bpy.types.BezierSplinePoint.html?highlight=bezier#bpy.types.BezierSplinePoint
    for key, bezier in zip(spline_data.keys, b_spline.bezier_points):
        bezier.co = unpack(key.pos, spline_data.scale)
        bezier.handle_left = bezier.co + unpack(key.handle_left, key.handle_scale)
        bezier.handle_right = bezier.co + unpack(key.handle_right, key.handle_scale)

    # create Object
    b_ob = bpy.data.objects.new(spl_basename, b_cu)
    # maybe add it to bezier.co instead?
    b_ob.location = unpack(spline_data.offset, 1.0)
    # attach to scene and validate context
    scene = bpy.context.scene
    scene.collection.objects.link(b_ob)

    reporter.show_info(f"Imported {spl_basename}")
