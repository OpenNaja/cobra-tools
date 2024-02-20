import logging

import bpy

from generated.formats.ms2.bitfields.ModelFlag import ModelFlag
from plugin.utils.object import ensure_visible, create_collection
from plugin.utils.shell import is_shell, is_fin, copy_ob


def update_lods(reporter, mdl2_coll, levels):
	"""Automatic LOD generator by NDP. Generates LOD objects and automatically decimates them for LOD0-LOD5"""
	logging.info(f"Generating LOD objects")
	scene = bpy.context.scene
	with ensure_visible():
		# get all current LOD collections
		lod_collections = get_lod_collections(mdl2_coll)
		if lod_collections:
			# delete old LOD objects
			for lod_coll in lod_collections[1:]:
				for ob in lod_coll.objects:
					bpy.data.objects.remove(ob)
				bpy.data.collections.remove(lod_coll)
		else:
			reporter.show_warning("Found no existing LODs")
			# create _L0 collection and put any mesh children of mdl2_coll in it
			lod0 = create_collection(f"{mdl2_coll.name}_L0", mdl2_coll)
			for ob in mdl2_coll.objects:
				if ob.type == "MESH":
					mdl2_coll.objects.unlink(ob)
					lod0.objects.link(ob)
		# get or create the lod collections
		lod_collections = [create_collection(f"{mdl2_coll.name}_L{lod_i}", mdl2_coll) for lod_i in range(len(levels))]
		for lod_index, lod_coll in enumerate(lod_collections):
			level = levels[lod_index]
			lod_coll["distance"] = level.distance
			if lod_index == 0:
				continue
			for ob_index, ob in enumerate(lod_collections[0].objects):
				# JWE2 - shell is separate from base fur
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
					reporter.show_warning(
						f"Can't create automatic LODs for model with shape keys. Decimate manually")
				else:
					reporter.show_info(f"Generated LOD object")
					if len(b_me.polygons) > 3:
						# Decimating duplicated object
						decimate = obj1.modifiers.new("Decimate", 'DECIMATE')
						decimate.ratio = (4 / len(b_me.vertices)) ** (1 / level.ratio)

				# remove additional shell material from LODs after LOD1
				if is_shell(ob) and lod_index > 1:
					# toggle the flag on the bitfield to maintain the other bits, but fins seems to be always 565
					# b_me["flag"] = 565
					flag = ModelFlag.from_value(b_me["flag"])
					flag.repeat_tris = True
					flag.num_shells = 0
					b_me["flag"] = int(flag)
					# remove shell material
					b_me.materials.pop(index=1)


def get_lod_collections(mdl2_coll):
	lod_collections = [col for col in mdl2_coll.children if "_L" in col.name]
	return lod_collections
