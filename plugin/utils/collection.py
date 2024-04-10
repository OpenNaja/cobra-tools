import bpy
from collections import defaultdict

# adapted from
# https://blender.stackexchange.com/questions/157828/how-to-duplicate-a-certain-collection-using-python


def copy_objects(from_col, to_col, linked, dupe_lut, replacer, share_materials, share_rig):
	# behavior differs for meshes in _Lx collection
	if "_L" in from_col.name:
		for ob in from_col.objects:
			dupe = ob.copy()
			dupe.name = replacer(ob.name)
			if not linked and ob.data:
				dupe.data = dupe.data.copy()
				dupe.data.name = replacer(ob.data.name)
				# use LUT for mats to only duplicate once per run
				if dupe.type == "MESH" and not share_materials:
					for i, mat in enumerate(dupe.data.materials):
						# find previously copied material
						if mat in dupe_lut:
							copy_mat = dupe_lut[mat]
						else:
							copy_mat = mat.copy()
							# fallback to name_copy if replacer changes nothing
							new_name = replacer(mat.name)
							if new_name != mat.name:
								copy_mat.name = new_name
							else:
								copy_mat.name = f"{mat.name}_copy"
							dupe_lut[mat] = copy_mat
						# update material slot
						dupe.data.materials[i] = copy_mat
			to_col.objects.link(dupe)
			dupe_lut[ob] = dupe
	else:
		# everything that is not visible lod geometry (armature, joints, hitchecks)
		for ob in from_col.objects:
			if share_rig:
				to_col.objects.link(ob)
			else:
				dupe = ob.copy()
				dupe.name = replacer(ob.name)
				if ob.data:
					dupe.data = dupe.data.copy()
					dupe.data.name = replacer(ob.data.name)
				to_col.objects.link(dupe)
				dupe_lut[ob] = dupe


def copy(parent, collection, linked=False, replacer=None, share_materials=True, share_rig=True):
	assert parent != collection
	dupe_lut = defaultdict(lambda: None)

	def _copy(parent, collection, linked=False):
		cc = bpy.data.collections.new(replacer(collection.name))
		# copy all custom properties over
		for k, v in collection.items():
			cc[k] = v
		copy_objects(collection, cc, linked, dupe_lut, replacer, share_materials, share_rig)

		for c in collection.children:
			_copy(cc, c, linked)

		parent.children.link(cc)

	_copy(parent, collection, linked)

	# fix links to original objects to point to copies instead
	for ob, dupe in tuple(dupe_lut.items()):
		if isinstance(ob, bpy.types.Object):
			if dupe.rigid_body_constraint:
				dupe.rigid_body_constraint.object1 = dupe_lut[ob.rigid_body_constraint.object1]
				dupe.rigid_body_constraint.object2 = dupe_lut[ob.rigid_body_constraint.object2]
			for modifier in dupe.modifiers:
				if modifier.type == "ARMATURE":
					modifier.object = dupe_lut[modifier.object]
			parent = dupe_lut[ob.parent]
			if parent:
				dupe.parent = parent
