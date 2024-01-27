import logging

import bpy
import numpy as np

from plugin.utils.object import ensure_visible
from plugin.utils.shell import is_shell, is_fin, copy_ob


def create_lods(mdl2_coll):
	"""Automatic LOD generator by NDP. Generates LOD objects and automatically decimates them for LOD0-LOD5"""
	msgs = []
	logging.info(f"Generating LOD objects")
	scene = bpy.context.scene

	with ensure_visible():
		shape_keyed = []
		decimated = []
		# for mdl2_coll in scene.collection.children:
		# Make list of all LOD collections
		lod_collections = get_lod_collections(mdl2_coll)
		# Setup default lod ratio values
		lod_ratios = np.linspace(1.0, 0.05, num=len(lod_collections))

		# Deleting old LODs
		for lod_coll in lod_collections[1:]:
			for ob in lod_coll.objects:
				# delete old target
				bpy.data.objects.remove(ob, do_unlink=True)

		for lod_index, (lod_coll, ratio) in enumerate(zip(lod_collections, lod_ratios)):
			if lod_index > 0:
				for ob_index, ob in enumerate(lod_collections[0].objects):
					# additional skip condition for JWE2, as shell is separate from base fur here
					if scene.cobra.game == "Jurassic World Evolution 2":
						if is_shell(ob) and lod_index > 1:
							continue
					# check if we want to copy this one
					if is_fin(ob) and lod_index > 1:
						continue
					obj1 = copy_ob(ob, lod_coll)
					obj1.name = f"{mdl2_coll.name}_ob{ob_index}_L{lod_index}"
					b_me = obj1.data

					# Can't create automatic LODs for models that have shape keys
					if ob.data.shape_keys:
						shape_keyed.append(ob)
					else:
						decimated.append(ob)
						if len(b_me.polygons) > 3:
							# Decimating duplicated object
							decimate = obj1.modifiers.new("Decimate", 'DECIMATE')
							decimate.ratio = ratio

					# remove additional shell material from LODs after LOD1
					if is_shell(ob) and lod_index > 1:
						# toggle the flag on the bitfield to maintain the other bits, but fins seems to be always 565
						b_me["flag"] = 565
						# flag = ModelFlag.from_value(b_me["flag"])
						# flag.repeat_tris = True
						# flag.fur_shells = False
						# b_me["flag"] = int(flag)
						# remove shell material
						b_me.materials.pop(index=1)
	if decimated:
		msgs.append(f"{len(decimated)} LOD objects generated successfully")
	if shape_keyed:
		msgs.append(
			f"Can't create automatic LODs for {len(shape_keyed)} models with shape keys. Decimate those manually")
	return msgs


def get_lod_collections(mdl2_coll):
	lod_collections = [col for col in mdl2_coll.children if "_L" in col.name]
	return lod_collections
